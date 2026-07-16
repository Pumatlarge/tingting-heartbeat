from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def descendants(widget):
    for child in widget.winfo_children():
        yield child
        yield from descendants(child)


with tempfile.TemporaryDirectory(prefix="tingting-language-") as temp:
    os.environ["APPDATA"] = temp
    os.environ["TINGTING_SKIP_SPLASH"] = "1"
    from tingting_pet.app import TingtingPet
    from tingting_pet.storage import load_state

    app = TingtingPet()
    assert app.language == "zh-CN"
    app.open_settings()
    window = app.dialogs["settings"]
    window.update()
    combo = next(widget for widget in descendants(window) if widget.winfo_class() == "TCombobox")
    combo.set("English")
    save = next(widget for widget in descendants(window) if widget.winfo_class() == "TButton" and widget.cget("text") == "保存设置")
    save.invoke()
    app.root.update()
    assert app.language == "en"
    assert load_state()["settings"]["language"] == "en"
    app.open_quick_panel(40, 40)
    app.quick_panel.update()
    labels = [str(widget.cget("text")) for widget in descendants(app.quick_panel) if widget.winfo_class() == "Button"]
    assert any("Chat" in label for label in labels)
    app.quit()
    print("LANGUAGE_SWITCH_OK")
