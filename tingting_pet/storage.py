from __future__ import annotations

import base64
import ctypes
import json
import os
import sys
import tempfile
import time
from ctypes import wintypes
from datetime import date, datetime, timedelta
from pathlib import Path


APP_NAME = "TingtingDesktopPet"


def app_dir() -> Path:
    root = Path(os.environ.get("APPDATA", Path.home()))
    path = root / APP_NAME
    path.mkdir(parents=True, exist_ok=True)
    return path


def default_state() -> dict:
    return {
        "version": 2,
        "launch_count": 0,
        "companion_seconds": 0,
        "clicks": 0,
        "touch_seconds": 0,
        "chat_seconds": 0,
        "idle_seconds": 0,
        "part_clicks": {},
        "feeds": 0,
        "food_counts": {},
        "gifts_given": 0,
        "gift_counts": {},
        "chats": 0,
        "drag_distance": 0,
        "actions_seen": [],
        "achievements": {},
        "achievement_rewards_claimed": {},
        "flags": {},
        "hunger": 76,
        "mood": 82,
        "energy": 78,
        "care_alert_levels": {"hunger": 0, "mood": 0, "energy": 0},
        "coins": 200,
        "coins_earned": 200,
        "coins_spent": 0,
        "coin_seconds": 0,
        "inventory_food": {},
        "inventory_gift": {},
        "inventory_recovery": {"元气营养包": 1},
        "system_drops": 0,
        "last_feed_at": time.time(),
        "last_gift_at": time.time(),
        "last_save_at": time.time(),
        "next_drop_at": time.time() + 1800,
        "last_open_date": "",
        "streak_days": 0,
        "total_launch_days": 0,
        "position": None,
        "chat_sessions": [],
        "active_chat_id": None,
        "settings": {
            "language": "zh-CN",
            "scale": 0.82,
            "opacity": 1.0,
            "always_on_top": True,
            "start_with_windows": False,
            "api_base": "https://api.openai.com/v1",
            "api_model": "gpt-4.1-mini",
            "api_key_protected": "",
            "web_search_enabled": False,
            "auto_check_updates": True,
        },
    }


def _merge_defaults(target: dict, defaults: dict) -> dict:
    for key, value in defaults.items():
        if key not in target:
            target[key] = value
        elif isinstance(value, dict) and isinstance(target[key], dict):
            _merge_defaults(target[key], value)
    return target


def load_state() -> dict:
    path = app_dir() / "state.json"
    state = default_state()
    if path.exists():
        try:
            loaded = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(loaded, dict):
                state = _merge_defaults(loaded, state)
        except (OSError, ValueError):
            backup = path.with_suffix(f".broken-{datetime.now():%Y%m%d-%H%M%S}.json")
            try:
                path.replace(backup)
            except OSError:
                pass
    _migrate_state(state)
    _record_launch(state)
    return state


def _migrate_state(state: dict) -> None:
    parts = state.setdefault("part_clicks", {})
    legacy_map = {"head": "hair", "left_hand": "arms", "right_hand": "arms", "waist": "chest"}
    for old, new in legacy_map.items():
        if old in parts:
            parts[new] = int(parts.get(new, 0)) + int(parts.pop(old, 0))
    state["coins"] = max(0, int(state.get("coins", 0)))
    state["total_launch_days"] = max(0, int(state.get("total_launch_days", 0)), int(state.get("streak_days", 0)))
    for key in ["inventory_food", "inventory_gift", "inventory_recovery"]:
        state[key] = {name: max(0, int(count)) for name, count in state.get(key, {}).items()}


def _record_launch(state: dict) -> None:
    today = date.today()
    previous_raw = state.get("last_open_date", "")
    try:
        previous = date.fromisoformat(previous_raw) if previous_raw else None
    except ValueError:
        previous = None
    if previous != today:
        state["total_launch_days"] = max(0, int(state.get("total_launch_days", 0))) + 1
        if previous == today - timedelta(days=1):
            state["streak_days"] = max(1, int(state.get("streak_days", 0)) + 1)
        else:
            state["streak_days"] = 1
        state["last_open_date"] = today.isoformat()
    state["launch_count"] = int(state.get("launch_count", 0)) + 1


def save_state(state: dict) -> None:
    state["last_save_at"] = time.time()
    target = app_dir() / "state.json"
    fd, temp_name = tempfile.mkstemp(prefix="state-", suffix=".json", dir=app_dir())
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(state, handle, ensure_ascii=False, indent=2)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, target)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)


class DATA_BLOB(ctypes.Structure):
    _fields_ = [("cbData", wintypes.DWORD), ("pbData", ctypes.POINTER(ctypes.c_byte))]


def _blob(data: bytes) -> tuple[DATA_BLOB, ctypes.Array]:
    buffer = ctypes.create_string_buffer(data)
    return DATA_BLOB(len(data), ctypes.cast(buffer, ctypes.POINTER(ctypes.c_byte))), buffer


def protect_secret(secret: str) -> str:
    if not secret:
        return ""
    raw = secret.encode("utf-8")
    source, source_buffer = _blob(raw)
    entropy, entropy_buffer = _blob(b"TingtingDesktopPet-v1")
    output = DATA_BLOB()
    ok = ctypes.windll.crypt32.CryptProtectData(
        ctypes.byref(source), "Tingting API key", ctypes.byref(entropy), None, None, 0,
        ctypes.byref(output),
    )
    _ = source_buffer, entropy_buffer
    if not ok:
        raise ctypes.WinError()
    try:
        data = ctypes.string_at(output.pbData, output.cbData)
        return base64.b64encode(data).decode("ascii")
    finally:
        ctypes.windll.kernel32.LocalFree(output.pbData)


def unprotect_secret(protected: str) -> str:
    if not protected:
        return ""
    try:
        raw = base64.b64decode(protected)
        source, source_buffer = _blob(raw)
        entropy, entropy_buffer = _blob(b"TingtingDesktopPet-v1")
        output = DATA_BLOB()
        ok = ctypes.windll.crypt32.CryptUnprotectData(
            ctypes.byref(source), None, ctypes.byref(entropy), None, None, 0,
            ctypes.byref(output),
        )
        _ = source_buffer, entropy_buffer
        if not ok:
            return ""
        try:
            return ctypes.string_at(output.pbData, output.cbData).decode("utf-8")
        finally:
            ctypes.windll.kernel32.LocalFree(output.pbData)
    except (ValueError, OSError):
        return ""


def set_start_with_windows(enabled: bool) -> None:
    import winreg

    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE) as key:
        if enabled:
            if getattr(sys, "frozen", False):
                command = f'"{sys.executable}"'
            else:
                entry = Path(sys.argv[0]).resolve()
                command = f'"{sys.executable}" "{entry}"'
            winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, command)
        else:
            try:
                winreg.DeleteValue(key, APP_NAME)
            except FileNotFoundError:
                pass
