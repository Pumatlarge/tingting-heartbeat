from __future__ import annotations

import hashlib
import json
import os
import re
import tempfile
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable
from urllib.parse import urlparse


LATEST_RELEASE_API = "https://api.github.com/repos/Pumatlarge/tingting-heartbeat/releases/latest"
RELEASES_PAGE = "https://github.com/Pumatlarge/tingting-heartbeat/releases"
USER_AGENT = "TingtingHeartbeat-Updater"
INSTALLER_PATTERN = re.compile(r"^TingtingHeartbeat-Setup-v.+\.exe$", re.IGNORECASE)


@dataclass(frozen=True)
class UpdateInfo:
    version: str
    tag_name: str
    title: str
    notes: str
    release_url: str
    asset_name: str | None
    asset_url: str | None
    asset_size: int
    asset_digest: str | None


def _version_key(value: str) -> tuple[int, ...]:
    match = re.fullmatch(r"\s*v?(\d+(?:\.\d+){1,3})\s*", str(value), re.IGNORECASE)
    if not match:
        raise ValueError(f"Unsupported version: {value}")
    return tuple(int(part) for part in match.group(1).split("."))


def normalized_version(value: str) -> str:
    return ".".join(str(part) for part in _version_key(value))


def is_newer_version(candidate: str, current: str) -> bool:
    candidate_key = _version_key(candidate)
    current_key = _version_key(current)
    width = max(len(candidate_key), len(current_key))
    return candidate_key + (0,) * (width - len(candidate_key)) > current_key + (0,) * (width - len(current_key))


def _select_installer(assets: list[dict[str, Any]]) -> dict[str, Any] | None:
    uploaded = [asset for asset in assets if asset.get("state", "uploaded") == "uploaded"]
    for asset in uploaded:
        if INSTALLER_PATTERN.fullmatch(str(asset.get("name", ""))):
            return asset
    for asset in uploaded:
        name = str(asset.get("name", ""))
        if name.lower().endswith(".exe") and any(word in name.lower() for word in ("setup", "installer")):
            return asset
    return None


def parse_release(payload: dict[str, Any]) -> UpdateInfo:
    tag_name = str(payload.get("tag_name", "")).strip()
    version = normalized_version(tag_name)
    asset = _select_installer(list(payload.get("assets") or []))
    release_url = str(payload.get("html_url") or RELEASES_PAGE)
    return UpdateInfo(
        version=version,
        tag_name=tag_name,
        title=str(payload.get("name") or tag_name or f"v{version}"),
        notes=str(payload.get("body") or "").strip(),
        release_url=release_url,
        asset_name=str(asset.get("name")) if asset else None,
        asset_url=str(asset.get("browser_download_url")) if asset else None,
        asset_size=max(0, int(asset.get("size", 0))) if asset else 0,
        asset_digest=str(asset.get("digest")) if asset and asset.get("digest") else None,
    )


def fetch_latest_release(timeout: float = 12.0) -> UpdateInfo:
    request = urllib.request.Request(
        LATEST_RELEASE_API,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": USER_AGENT,
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        payload = json.loads(response.read().decode("utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("GitHub returned an invalid release response")
    return parse_release(payload)


def _trusted_download_url(value: str) -> bool:
    parsed = urlparse(value)
    host = (parsed.hostname or "").lower()
    return parsed.scheme == "https" and (host == "github.com" or host.endswith(".githubusercontent.com"))


class _TrustedRedirectHandler(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if not _trusted_download_url(newurl):
            raise urllib.error.HTTPError(newurl, code, "Untrusted update redirect", headers, fp)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def download_update(
    info: UpdateInfo,
    progress: Callable[[int, int], None] | None = None,
    destination_dir: Path | None = None,
    timeout: float = 30.0,
) -> Path:
    if not info.asset_name or not info.asset_url:
        raise ValueError("This release does not include a Windows installer")
    if Path(info.asset_name).name != info.asset_name or not info.asset_name.lower().endswith(".exe"):
        raise ValueError("The update filename is invalid")
    if not _trusted_download_url(info.asset_url):
        raise ValueError("The update download URL is not hosted by GitHub")

    output_dir = destination_dir or Path(tempfile.gettempdir()) / "TingtingHeartbeatUpdate"
    output_dir.mkdir(parents=True, exist_ok=True)
    output = output_dir / info.asset_name
    partial = output.with_suffix(output.suffix + ".part")
    digest = hashlib.sha256()
    downloaded = 0
    expected = info.asset_size
    opener = urllib.request.build_opener(_TrustedRedirectHandler())
    request = urllib.request.Request(info.asset_url, headers={"User-Agent": USER_AGENT})
    try:
        with opener.open(request, timeout=timeout) as response, partial.open("wb") as target:
            response_size = int(response.headers.get("Content-Length") or 0)
            if expected <= 0:
                expected = response_size
            while True:
                chunk = response.read(1024 * 256)
                if not chunk:
                    break
                target.write(chunk)
                digest.update(chunk)
                downloaded += len(chunk)
                if progress:
                    progress(downloaded, expected)
        if info.asset_size > 0 and downloaded != info.asset_size:
            raise OSError(f"Downloaded {downloaded} bytes, expected {info.asset_size}")
        if info.asset_digest and info.asset_digest.lower().startswith("sha256:"):
            expected_digest = info.asset_digest.split(":", 1)[1].lower()
            if digest.hexdigest().lower() != expected_digest:
                raise OSError("The downloaded update failed SHA-256 verification")
        os.replace(partial, output)
        return output
    except Exception:
        try:
            partial.unlink(missing_ok=True)
        except OSError:
            pass
        raise
