from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

from PIL import ImageGrab

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


with tempfile.TemporaryDirectory(prefix="tingting-english-") as temp:
    os.environ["APPDATA"] = temp
    os.environ["TINGTING_SKIP_SPLASH"] = "1"
    from tingting_pet.storage import default_state, save_state

    state = default_state()
    state["settings"]["language"] = "en"
    save_state(state)

    from tingting_pet.app import TingtingPet

    app = TingtingPet()
    assert app.language == "en"
    assert app.app_title == "Tingting Heartbeat"
    app.root.after(300, lambda: app.open_quick_panel(60, 60))

    def capture_panel() -> None:
        ImageGrab.grab(bbox=(30, 30, 420, 590), all_screens=True).save(ROOT / "qa" / "english-panel.png")
        if app.quick_panel and app.quick_panel.winfo_exists():
            app.quick_panel.destroy()
        app.open_settings()
        app.dialogs["settings"].geometry("600x700+60+40")

    def capture_settings() -> None:
        ImageGrab.grab(bbox=(30, 20, 710, 780), all_screens=True).save(ROOT / "qa" / "english-settings.png")
        settings = app.dialogs.pop("settings", None)
        if settings:
            settings.destroy()
        app.open_store()
        app.dialogs["store"].geometry("820x700+60+40")

    def capture_store() -> None:
        ImageGrab.grab(bbox=(30, 20, 930, 780), all_screens=True).save(ROOT / "qa" / "english-store.png")
        app.quit()

    app.root.after(1300, capture_panel)
    app.root.after(2600, capture_settings)
    app.root.after(3900, capture_store)
    app.run()
    print("ENGLISH_CAPTURE_OK")
