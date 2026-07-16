from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

from PIL import ImageGrab

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


with tempfile.TemporaryDirectory(prefix="tingting-splash-") as temp:
    os.environ["APPDATA"] = temp
    os.environ.pop("TINGTING_SKIP_SPLASH", None)
    from tingting_pet.app import TingtingPet

    app = TingtingPet()
    assert app.startup_splash is not None
    assert app.root.state() == "withdrawn"

    def capture() -> None:
        splash = app.startup_splash
        x, y = splash.winfo_x(), splash.winfo_y()
        left, top, right, bottom = app._active_monitor_bounds()
        expected_x = left + (right - left - splash.winfo_width()) // 2
        expected_y = top + (bottom - top - splash.winfo_height()) // 2
        assert abs(x - expected_x) <= 1 and abs(y - expected_y) <= 1, (
            f"splash is not centered: actual=({x}, {y}), expected=({expected_x}, {expected_y})"
        )
        ImageGrab.grab(bbox=(x - 12, y - 12, x + splash.winfo_width() + 12, y + splash.winfo_height() + 12), all_screens=True).save(ROOT / "qa" / "startup-splash.png")

    def verify() -> None:
        assert app.startup_splash is None
        assert app.root.state() == "normal"
        app.quit()
        print("STARTUP_SPLASH_OK")

    app.root.after(700, capture)
    app.root.after(2800, verify)
    app.run()
