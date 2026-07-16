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


with tempfile.TemporaryDirectory(prefix="tingting-store-layout-") as temp:
    os.environ["APPDATA"] = temp
    os.environ["TINGTING_SKIP_SPLASH"] = "1"
    from tingting_pet.app import TingtingPet

    app = TingtingPet()
    try:
        app.open_store()
        window = app.dialogs["store"]
        window.geometry("820x700+90+50")
        pump(app, 0.6)
        canvas = next(item for item in window._wheel_canvases if item.winfo_ismapped())
        bounds = canvas.bbox("all")
        assert bounds is not None and bounds[2] >= canvas.winfo_width() - 3
        ImageGrab.grab(
            bbox=(window.winfo_x() - 8, window.winfo_y() - 8, window.winfo_x() + window.winfo_width() + 8, window.winfo_y() + window.winfo_height() + 8),
            all_screens=True,
        ).save(ROOT / "qa" / "store-layout.png")
        print("STORE_LAYOUT_CAPTURE_OK")
    finally:
        app.quit()
