from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

from PIL import ImageGrab

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


with tempfile.TemporaryDirectory(prefix="tingting-ai-settings-capture-") as temp:
    os.environ["APPDATA"] = temp
    os.environ["TINGTING_SKIP_SPLASH"] = "1"
    from tingting_pet.app import TingtingPet

    app = TingtingPet()
    app.root.after(200, app.open_settings)

    def capture() -> None:
        window = app.dialogs["settings"]
        window.geometry("600x740+100+40")
        window.update()
        box = (
            window.winfo_rootx(),
            window.winfo_rooty(),
            window.winfo_rootx() + window.winfo_width(),
            window.winfo_rooty() + window.winfo_height(),
        )
        ImageGrab.grab(bbox=box, all_screens=True).save(ROOT / "qa" / "ai-web-search-setting.png")
        app.quit()

    app.root.after(650, capture)
    app.run()
    print("AI_SETTINGS_CAPTURE_OK")
