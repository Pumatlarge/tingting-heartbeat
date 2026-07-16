from __future__ import annotations

import ctypes
import json
import sys
import traceback

from PIL import Image

from tingting_pet.catalog import ACHIEVEMENTS, FOODS, GIFTS, LOGICAL_ACTIONS, RECOVERY_ITEMS, ROW_INDEX
from tingting_pet.storage import app_dir, default_state


def self_test() -> int:
    from tingting_pet.app import TingtingPet, resource_path

    atlas_path = resource_path("assets/spritesheet.webp")
    action_names = ["wave", "jump", "dance", "think", "work", "review", "sleepy", "walk", "shy", "celebrate"]
    with Image.open(atlas_path) as atlas:
        result = {
            "ok": atlas.size == (1536, 1872) and atlas.mode == "RGBA",
            "atlas": {"path": str(atlas_path), "size": atlas.size, "mode": atlas.mode},
            "foods": len(FOODS),
            "required_foods": all(name in {food["name"] for food in FOODS} for name in ["蒜蓉空心菜", "白灼虾", "香煎牛肉"]),
            "logical_actions": len(LOGICAL_ACTIONS),
            "achievements": len(ACHIEVEMENTS),
            "sprite_rows": len(ROW_INDEX),
            "gifts": len(GIFTS),
            "recovery_items": len(RECOVERY_ITEMS),
            "api_key_default_empty": default_state()["settings"]["api_key_protected"] == "",
            "language_default": default_state()["settings"]["language"] == "zh-CN",
            "heartbeat_icon": resource_path("assets/tingting-heartbeat-icon.png").is_file(),
            "heart_cursor": resource_path("assets/heart.cur").is_file(),
            "action_icons": all(resource_path(f"assets/action-icons/{name}.png").is_file() for name in action_names),
            "desk_sleep": LOGICAL_ACTIONS.get("desk_sleep", {}).get("effect") == "desk_sleep",
            "hit_zones": {
                "hair": TingtingPet._classify_visible_point(0.2, 0.16),
                "face": TingtingPet._classify_visible_point(0.5, 0.2),
                "chest": TingtingPet._classify_visible_point(0.5, 0.4),
                "arms": TingtingPet._classify_visible_point(0.2, 0.4),
                "skirt": TingtingPet._classify_visible_point(0.5, 0.7),
            },
        }
        result["hit_zones_ok"] = all(key == value for key, value in result["hit_zones"].items())
        menu_actions = ["wave", "jump", "dance", "think", "work", "review", "sleepy", "walk", "shy", "celebrate"]
        result["action_effects_unique"] = len({LOGICAL_ACTIONS[name].get("effect", name) for name in menu_actions}) == len(menu_actions)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] and result["required_foods"] and result["api_key_default_empty"] and result["language_default"] and result["heartbeat_icon"] and result["heart_cursor"] and result["action_icons"] and result["desk_sleep"] and result["hit_zones_ok"] and result["action_effects_unique"] else 1


def acquire_single_instance():
    handle = ctypes.windll.kernel32.CreateMutexW(None, False, "Local\\TingtingHeartbeat-83A938C3")
    if ctypes.windll.kernel32.GetLastError() == 183:
        ctypes.windll.user32.MessageBoxW(None, "心动婷婷已经在桌面上啦，请看看系统托盘。\nTingting Heartbeat is already running.", "心动婷婷 / Tingting Heartbeat", 0x40)
        return None
    return handle


def main() -> int:
    if "--self-test" in sys.argv:
        return self_test()
    mutex = acquire_single_instance()
    if mutex is None:
        return 0
    try:
        from tingting_pet.app import TingtingPet

        TingtingPet().run()
        return 0
    except Exception:
        log_path = app_dir() / "crash.log"
        log_path.write_text(traceback.format_exc(), encoding="utf-8")
        ctypes.windll.user32.MessageBoxW(None, f"心动婷婷启动失败 / Tingting Heartbeat failed to start:\n{log_path}", "心动婷婷 / Tingting Heartbeat", 0x10)
        return 1
    finally:
        ctypes.windll.kernel32.CloseHandle(mutex)


if __name__ == "__main__":
    raise SystemExit(main())
