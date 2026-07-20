from __future__ import annotations

import hashlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tingting_pet.updater import UpdateInfo, download_update, is_newer_version, parse_release


class FakeResponse:
    def __init__(self, content: bytes) -> None:
        self.stream = io.BytesIO(content)
        self.headers = {"Content-Length": str(len(content))}

    def read(self, size: int = -1) -> bytes:
        return self.stream.read(size)

    def __enter__(self):
        return self

    def __exit__(self, *_args) -> None:
        return None


class FakeOpener:
    def __init__(self, content: bytes) -> None:
        self.content = content

    def open(self, _request, timeout: float):
        return FakeResponse(self.content)


class UpdaterTests(unittest.TestCase):
    def test_semantic_version_comparison(self) -> None:
        self.assertTrue(is_newer_version("v1.6.0", "1.5.1"))
        self.assertTrue(is_newer_version("1.6.1", "1.6"))
        self.assertFalse(is_newer_version("v1.6.0", "1.6.0"))
        self.assertFalse(is_newer_version("1.5.9", "1.6.0"))
        with self.assertRaises(ValueError):
            is_newer_version("latest", "1.6.0")

    def test_release_parser_prefers_named_installer(self) -> None:
        payload = {
            "tag_name": "v1.7.0",
            "name": "Tingting Heartbeat 1.7.0",
            "body": "New update",
            "html_url": "https://github.com/Pumatlarge/tingting-heartbeat/releases/tag/v1.7.0",
            "assets": [
                {"name": "TingtingHeartbeat.exe", "browser_download_url": "https://github.com/portable.exe", "size": 20, "state": "uploaded"},
                {"name": "TingtingHeartbeat-Setup-v1.7.0.exe", "browser_download_url": "https://github.com/setup.exe", "size": 30, "state": "uploaded", "digest": "sha256:abcd"},
            ],
        }
        info = parse_release(payload)
        self.assertEqual(info.version, "1.7.0")
        self.assertEqual(info.asset_name, "TingtingHeartbeat-Setup-v1.7.0.exe")
        self.assertEqual(info.asset_size, 30)
        self.assertEqual(info.asset_digest, "sha256:abcd")

    def test_download_verifies_size_and_sha256(self) -> None:
        content = b"signed installer bytes"
        info = UpdateInfo(
            version="1.7.0",
            tag_name="v1.7.0",
            title="v1.7.0",
            notes="",
            release_url="https://github.com/Pumatlarge/tingting-heartbeat/releases/tag/v1.7.0",
            asset_name="TingtingHeartbeat-Setup-v1.7.0.exe",
            asset_url="https://github.com/Pumatlarge/tingting-heartbeat/releases/download/v1.7.0/TingtingHeartbeat-Setup-v1.7.0.exe",
            asset_size=len(content),
            asset_digest=f"sha256:{hashlib.sha256(content).hexdigest()}",
        )
        progress: list[tuple[int, int]] = []
        with tempfile.TemporaryDirectory() as temp, patch("tingting_pet.updater.urllib.request.build_opener", return_value=FakeOpener(content)):
            result = download_update(info, progress=lambda done, total: progress.append((done, total)), destination_dir=Path(temp))
            self.assertEqual(result.read_bytes(), content)
        self.assertEqual(progress[-1], (len(content), len(content)))

    def test_download_rejects_non_github_url(self) -> None:
        info = UpdateInfo("1.7.0", "v1.7.0", "v1.7.0", "", "https://example.com", "setup.exe", "https://example.com/setup.exe", 0, None)
        with self.assertRaises(ValueError):
            download_update(info)


if __name__ == "__main__":
    unittest.main()
