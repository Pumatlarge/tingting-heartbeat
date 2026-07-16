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


with tempfile.TemporaryDirectory(prefix="tingting-click-light-") as temp:
    os.environ["APPDATA"] = temp
    os.environ["TINGTING_SKIP_SPLASH"] = "1"
    from tingting_pet.app import TingtingPet

    app = TingtingPet()
    try:
        app.root.geometry("+450+220")
        pump(app, 0.3)
        alpha = app.last_rendered_alpha
        bbox = alpha.getbbox()
        assert bbox is not None
        center_x, center_y = (bbox[0] + bbox[2]) // 2, (bbox[1] + bbox[3]) // 2
        point = min(
            (
                (x, y)
                for y in range(bbox[1], bbox[3])
                for x in range(bbox[0], bbox[2])
                if alpha.getpixel((x, y)) >= 24
            ),
            key=lambda item: (item[0] - center_x) ** 2 + (item[1] - center_y) ** 2,
        )
        app.handle_part_click(*point)
        pump(app, 0.18)
        x, y = app.root.winfo_x(), app.root.winfo_y()
        ImageGrab.grab(
            bbox=(x - 12, y - 12, x + app.window_w + 12, y + app.window_h + 12),
            all_screens=True,
        ).save(ROOT / "qa" / "click-light.png")
        print("CLICK_LIGHT_CAPTURE_OK")
    finally:
        app.quit()
