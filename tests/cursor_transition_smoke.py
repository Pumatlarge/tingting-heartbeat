from __future__ import annotations

import ctypes
import os
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


class Point(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]


def pump(app, seconds: float) -> None:
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        app.root.update()
        time.sleep(0.02)


with tempfile.TemporaryDirectory(prefix="tingting-cursor-") as temp:
    os.environ["APPDATA"] = temp
    os.environ["TINGTING_SKIP_SPLASH"] = "1"
    from tingting_pet.app import TingtingPet

    user32 = ctypes.windll.user32
    original = Point()
    user32.GetCursorPos(ctypes.byref(original))
    app = TingtingPet()
    try:
        app.root.geometry("+400+220")
        pump(app, 0.25)
        alpha = app.last_rendered_alpha
        bbox = alpha.getbbox()
        assert bbox is not None
        cx, cy = (bbox[0] + bbox[2]) // 2, (bbox[1] + bbox[3]) // 2
        visible = min(
            ((x, y) for y in range(bbox[1], bbox[3]) for x in range(bbox[0], bbox[2]) if alpha.getpixel((x, y)) >= 24),
            key=lambda point: (point[0] - cx) ** 2 + (point[1] - cy) ** 2,
        )
        user32.SetCursorPos(app.root.winfo_rootx() + visible[0], app.root.winfo_rooty() + app.bubble_h + visible[1])
        pump(app, 0.3)
        assert app.heart_cursor_active
        user32.SetCursorPos(app.root.winfo_rootx() - 40, app.root.winfo_rooty() - 40)
        pump(app, 0.3)
        assert not app.heart_cursor_active
        assert app.canvas.cget("cursor") == "arrow"
        print("CURSOR_TRANSITION_OK")
    finally:
        user32.SetCursorPos(original.x, original.y)
        app.quit()
