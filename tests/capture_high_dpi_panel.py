from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

from PIL import ImageGrab

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


with tempfile.TemporaryDirectory(prefix="tingting-panel-capture-") as temp:
    os.environ["APPDATA"] = temp
    os.environ["TINGTING_SKIP_SPLASH"] = "1"
    from tingting_pet.app import TingtingPet

    app = TingtingPet()
    app.root.tk.call("tk", "scaling", 2.25)
    app.root.after(250, lambda: app.open_quick_panel(40, 40))

    def capture() -> None:
        panel = app.quick_panel
        panel.update()
        left = panel.winfo_x()
        top = panel.winfo_y()
        right = left + panel.winfo_width()
        bottom = top + panel.winfo_height()
        ImageGrab.grab(bbox=(left, top, right, bottom), all_screens=True).save(ROOT / "qa" / "high-dpi-panel.png")
        app.quit()

    app.root.after(900, capture)
    app.run()
    print("HIGH_DPI_PANEL_CAPTURE_OK")
