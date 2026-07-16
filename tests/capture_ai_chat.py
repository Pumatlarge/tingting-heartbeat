from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

from PIL import ImageGrab

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


with tempfile.TemporaryDirectory(prefix="tingting-ai-chat-capture-") as temp:
    os.environ["APPDATA"] = temp
    os.environ["TINGTING_SKIP_SPLASH"] = "1"
    from tingting_pet.app import TingtingPet

    app = TingtingPet()
    app.root.after(200, app.open_chat)

    def send_message() -> None:
        chat = app.dialogs["chat"]
        chat.geometry("780x700+80+50")
        app.chat_input.insert(0, "请帮我安排一个轻松又高效的下午。")
        app.send_chat()

    def capture_waiting() -> None:
        chat = app.dialogs["chat"]
        chat.update()
        box = (chat.winfo_rootx(), chat.winfo_rooty(), chat.winfo_rootx() + chat.winfo_width(), chat.winfo_rooty() + chat.winfo_height())
        ImageGrab.grab(bbox=box, all_screens=True).save(ROOT / "qa" / "ai-chat-waiting.png")

    def prepare_history() -> None:
        old_id = app.state["active_chat_id"]
        app._new_chat_session()
        app._select_chat_session_by_id(old_id)

    def capture_history() -> None:
        chat = app.dialogs["chat"]
        chat.update()
        box = (
            chat.winfo_rootx(),
            chat.winfo_rooty(),
            chat.winfo_rootx() + chat.winfo_width(),
            chat.winfo_rooty() + chat.winfo_height(),
        )
        ImageGrab.grab(bbox=box, all_screens=True).save(ROOT / "qa" / "ai-chat-history.png")
        app.quit()

    app.root.after(350, send_message)
    app.root.after(550, capture_waiting)
    app.root.after(1050, prepare_history)
    app.root.after(1300, capture_history)
    app.run()
    print("AI_CHAT_CAPTURE_OK")
