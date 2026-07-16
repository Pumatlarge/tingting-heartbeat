from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path
from types import SimpleNamespace

from PIL import ImageGrab

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


with tempfile.TemporaryDirectory(prefix="tingting-capture-") as temp:
    os.environ["APPDATA"] = temp
    os.environ["TINGTING_SKIP_SPLASH"] = "1"
    from tingting_pet.app import TingtingPet

    app = TingtingPet()
    app.state["coins"] = 888
    app.root.geometry("+420+180")
    app.root.after(300, lambda: app.open_quick_panel(60, 70))

    def capture_panel() -> None:
        ImageGrab.grab(bbox=(30, 40, 730, 620), all_screens=True).save(ROOT / "qa" / "modern-panel.png")
        if app.quick_panel and app.quick_panel.winfo_exists():
            app.quick_panel.destroy()
        app.open_chat()
        chat = app.dialogs.get("chat")
        if chat:
            chat.geometry("680x680+80+60")

    def capture_chat() -> None:
        ImageGrab.grab(bbox=(50, 30, 790, 780), all_screens=True).save(ROOT / "qa" / "modern-chat.png")
        chat = app.dialogs.pop("chat", None)
        if chat:
            chat.destroy()
        app.open_actions()
        actions = app.dialogs.get("actions")
        if actions:
            actions.geometry("590x570+80+60")

    def capture_actions() -> None:
        ImageGrab.grab(bbox=(50, 30, 730, 680), all_screens=True).save(ROOT / "qa" / "action-icons.png")
        actions = app.dialogs.pop("actions", None)
        if actions:
            actions.destroy()
        app.open_achievements()
        achievements = app.dialogs.get("achievements")
        if achievements:
            achievements.geometry("720x650+80+60")

    def capture_achievements() -> None:
        ImageGrab.grab(bbox=(50, 30, 850, 760), all_screens=True).save(ROOT / "qa" / "achievements.png")
        achievements = app.dialogs.pop("achievements", None)
        if achievements:
            achievements.destroy()
        app.open_help()
        help_window = app.dialogs.get("help")
        if help_window:
            help_window.geometry("680x650+80+60")

    def capture_help() -> None:
        ImageGrab.grab(bbox=(50, 30, 790, 760), all_screens=True).save(ROOT / "qa" / "help.png")
        help_window = app.dialogs.pop("help", None)
        if help_window:
            help_window.destroy()
        app.root.geometry("+260+180")
        app.start_action("guard", "这里不可以随便碰啦，请尊重一点。")
        app._move_heart_cursor(SimpleNamespace(x=app.window_w // 2, y=app.bubble_h + app.sprite_h // 2))

    def capture_touch() -> None:
        x, y = app.root.winfo_x(), app.root.winfo_y()
        ImageGrab.grab(bbox=(x - 20, y - 20, x + app.window_w + 20, y + app.window_h + 20), all_screens=True).save(ROOT / "qa" / "heart-cursor-fixed.png")
        app.start_action("desk_sleep", "我在电脑桌前眯一会儿，你回来时轻轻叫醒我吧。")
        app.root.after(2000, capture_pet)

    def capture_pet() -> None:
        x, y = app.root.winfo_x(), app.root.winfo_y()
        ImageGrab.grab(bbox=(x - 20, y - 20, x + app.window_w + 20, y + app.window_h + 20), all_screens=True).save(ROOT / "qa" / "desk-sleep-bubble.png")
        app.quit()

    app.root.after(1300, capture_panel)
    app.root.after(2600, capture_chat)
    app.root.after(3900, capture_actions)
    app.root.after(5200, capture_achievements)
    app.root.after(6500, capture_help)
    app.root.after(7800, capture_touch)
    app.run()
    print("CAPTURE_OK")
