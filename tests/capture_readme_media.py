from __future__ import annotations

import ctypes
import os
import sys
import tempfile
import time
from pathlib import Path

from PIL import Image, ImageDraw, ImageGrab

ROOT = Path(__file__).resolve().parents[1]
MEDIA = ROOT / "docs" / "media"
sys.path.insert(0, str(ROOT))


def pump(app, seconds: float) -> None:
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        app.root.update()
        time.sleep(0.02)


def capture_window(window, destination: Path, margin: int = 0) -> None:
    window.update_idletasks()
    if sys.platform == "win32":
        class Rect(ctypes.Structure):
            _fields_ = [("left", ctypes.c_long), ("top", ctypes.c_long), ("right", ctypes.c_long), ("bottom", ctypes.c_long)]

        user32 = ctypes.windll.user32
        child = int(window.winfo_id())
        parent = int(user32.GetParent(child) or 0)
        rect = Rect()
        handle = parent or child
        if not user32.GetWindowRect(handle, ctypes.byref(rect)):
            raise RuntimeError("Could not read window bounds")
        try:
            visible_rect = Rect()
            if ctypes.windll.dwmapi.DwmGetWindowAttribute(
                ctypes.c_void_p(handle), 9, ctypes.byref(visible_rect), ctypes.sizeof(visible_rect)
            ) == 0:
                rect = visible_rect
        except Exception:
            pass
        left, top, right, bottom = rect.left, rect.top, rect.right, rect.bottom
    else:
        left = window.winfo_x()
        top = window.winfo_y()
        right = left + window.winfo_width()
        bottom = top + window.winfo_height()
    left -= margin
    top -= margin
    right += margin
    bottom += margin
    ImageGrab.grab(bbox=(left, top, right, bottom), all_screens=True).save(destination, optimize=True)


def make_character_demo(app, destination: Path) -> None:
    timeline: list[tuple[Image.Image, str, float, float | None]] = []
    sequences = [
        ("waving", "", 0.0),
        ("jumping", "dance", 0.8),
        ("jumping", "sparkle", 0.6),
    ]
    for row, effect, phase in sequences:
        source_frames = app.frames[row]
        for index in range(6):
            timeline.append((source_frames[index % len(source_frames)], effect, phase + index * 0.18, None))

    idle_frames = app.frames["idle"]
    for index, progress in enumerate((0.0, 0.12, 0.25, 0.42, 0.62, 0.82)):
        timeline.append((idle_frames[index % len(idle_frames)], "", index * 0.16, progress))

    rendered: list[Image.Image] = []
    for source, effect, phase, light_progress in timeline:
        sprite = app._decorate_effect(source.copy(), effect, phase)
        if light_progress is not None:
            sprite = app._compose_click_light(sprite, (sprite.width * 0.5, sprite.height * 0.58), light_progress)
        sprite.thumbnail((245, 270), Image.Resampling.LANCZOS)

        frame = Image.new("RGB", (420, 330), "#fff8f5")
        draw = ImageDraw.Draw(frame)
        draw.rounded_rectangle((18, 18, 402, 312), radius=28, fill="#fffdfb", outline="#efd7df", width=3)
        draw.rounded_rectangle((44, 282, 376, 292), radius=5, fill="#f5e4e9")
        x = (frame.width - sprite.width) // 2
        y = 28 + (270 - sprite.height)
        frame.paste(sprite, (x, y), sprite)
        rendered.append(frame)

    rendered[0].save(
        destination,
        save_all=True,
        append_images=rendered[1:],
        duration=145,
        loop=0,
        optimize=True,
        disposal=2,
    )


def run() -> None:
    MEDIA.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="tingting-readme-media-") as temp:
        os.environ["APPDATA"] = temp
        os.environ["TINGTING_SKIP_SPLASH"] = "1"
        from tingting_pet.app import TingtingPet

        app = TingtingPet()
        try:
            app.state.update({"coins": 888, "hunger": 82, "mood": 96, "energy": 91})

            app.open_quick_panel(70, 55)
            pump(app, 0.7)
            capture_window(app.quick_panel, MEDIA / "feature-center.png")
            app.quick_panel.destroy()
            app.quick_panel = None

            app.open_store()
            store = app.dialogs["store"]
            store.geometry("820x680+80+35")
            pump(app, 0.7)
            capture_window(store, MEDIA / "shop-and-inventory.png")
            app.dialogs.pop("store", None)
            store.destroy()

            app.open_chat()
            chat = app.dialogs["chat"]
            chat.geometry("700x650+110+45")
            pump(app, 0.7)
            capture_window(chat, MEDIA / "chat.png")
            app.dialogs.pop("chat", None)
            chat.destroy()

            app.settings["language"] = "en"
            app.open_store()
            store = app.dialogs["store"]
            store.geometry("820x680+80+35")
            pump(app, 0.6)
            capture_window(store, MEDIA / "shop-and-inventory-en.png")
            app.dialogs.pop("store", None)
            store.destroy()

            app.open_chat()
            chat = app.dialogs["chat"]
            chat.geometry("700x650+110+45")
            pump(app, 0.6)
            capture_window(chat, MEDIA / "chat-en.png")

            make_character_demo(app, MEDIA / "tingting-demo.gif")
        finally:
            app.quit()

    print("README_MEDIA_CAPTURE_OK")


if __name__ == "__main__":
    run()
