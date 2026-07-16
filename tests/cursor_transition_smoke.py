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
        root_x, root_y = app.root.winfo_rootx(), app.root.winfo_rooty()
        character_target = (root_x + visible[0], root_y + app.bubble_h + visible[1])
        user32.SetCursorPos(*character_target)
        pump(app, 0.5)
        actual = Point()
        user32.GetCursorPos(ctypes.byref(actual))
        assert abs(actual.x - character_target[0]) <= 2 and abs(actual.y - character_target[1]) <= 2, (
            f"pointer moved while approaching the character: target={character_target}, actual=({actual.x}, {actual.y})"
        )
        assert not hasattr(app, "heart_cursor_handle"), "custom cursor runtime is still active"
        assert app.canvas.cget("cursor") == "arrow"

        exits = {
            "left": (root_x - 50, root_y + app.bubble_h + visible[1]),
            "right": (root_x + app.window_w + 50, root_y + app.bubble_h + visible[1]),
            "top": (root_x + visible[0], root_y - 50),
            "bottom": (root_x + visible[0], root_y + app.window_h + 50),
        }
        for direction, target in exits.items():
            user32.SetCursorPos(*character_target)
            pump(app, 0.25)
            actual = Point()
            user32.GetCursorPos(ctypes.byref(actual))
            assert abs(actual.x - character_target[0]) <= 2 and abs(actual.y - character_target[1]) <= 2, f"pointer drifted before {direction} exit"
            user32.SetCursorPos(*target)
            pump(app, 0.5)
            actual = Point()
            user32.GetCursorPos(ctypes.byref(actual))
            assert abs(actual.x - target[0]) <= 2 and abs(actual.y - target[1]) <= 2, (
                f"pointer moved unexpectedly after {direction} exit: target={target}, actual=({actual.x}, {actual.y})"
            )
            assert app.canvas.cget("cursor") == "arrow"
        print("CURSOR_STABILITY_OK")
    finally:
        user32.SetCursorPos(original.x, original.y)
        app.quit()
