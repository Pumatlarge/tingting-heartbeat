from __future__ import annotations

import os
import sys
import tempfile
import time
from pathlib import Path

from PIL import ImageGrab

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def pump(app, seconds: float) -> None:
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        app.root.update()
        time.sleep(0.02)


def capture(app, name: str) -> None:
    x, y = app.root.winfo_x(), app.root.winfo_y()
    ImageGrab.grab(
        bbox=(x - 16, y - 16, x + app.window_w + 16, y + app.window_h + 16),
        all_screens=True,
    ).save(ROOT / "qa" / name)


def run() -> None:
    with tempfile.TemporaryDirectory(prefix="tingting-bubble-size-") as temp:
        os.environ["APPDATA"] = temp
        os.environ["TINGTING_SKIP_SPLASH"] = "1"
        from tingting_pet.app import TingtingPet

        app = TingtingPet()
        try:
            app.user_scale = 1.35
            app.scale = app._effective_scale(app.user_scale, app.monitor_dpi)
            app._resize_window(keep_position=False)
            app.root.geometry("+420+130")
            app.say("你好呀，我是婷婷。右键可以打开功能中心～")
            pump(app, 0.4)
            capture(app, "bubble-font-welcome.png")

            app.start_action("dance", "想看我穿着这条裙子跳舞吗？")
            pump(app, 0.5)
            capture(app, "bubble-font-dance.png")
            print("BUBBLE_FONT_CAPTURE_OK")
        finally:
            app.quit()


if __name__ == "__main__":
    run()
