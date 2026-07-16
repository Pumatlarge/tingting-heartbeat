from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def run() -> None:
    with tempfile.TemporaryDirectory(prefix="tingting-smoke-") as temp:
        os.environ["APPDATA"] = temp
        os.environ["TINGTING_SKIP_SPLASH"] = "1"
        from tingting_pet.app import TingtingPet

        app = TingtingPet()
        app.state["coins"] = 2000
        bbox = app.last_rendered_alpha.getbbox()
        assert bbox is not None
        visible_point = next(
            (x, y)
            for y in range(bbox[1], bbox[3])
            for x in range(bbox[0], bbox[2])
            if app.last_rendered_alpha.getpixel((x, y)) >= 24
        )
        app._update_heart_cursor(visible_point[0], app.bubble_h + visible_point[1])
        assert app.heart_cursor_active and app.canvas.cget("cursor") == "none"
        app._update_heart_cursor(0, 0)
        assert not app.heart_cursor_active and app.canvas.cget("cursor") == "arrow"
        app.root.after(300, lambda: app.open_quick_panel(40, 40))
        app.root.after(700, app.open_store)

        def verify_store_wheel() -> None:
            window = app.dialogs["store"]
            window.update()
            canvas = next(item for item in window._wheel_canvases if item.winfo_ismapped())
            before = canvas.yview()
            rootx, rooty = canvas.winfo_rootx() + 20, canvas.winfo_rooty() + 20
            x, y = rootx - window.winfo_rootx(), rooty - window.winfo_rooty()
            canvas.event_generate("<MouseWheel>", x=20, y=20, rootx=rootx, rooty=rooty, delta=-120)
            window.update_idletasks()
            assert canvas.yview() != before, "store mouse wheel did not scroll"

        app.root.after(900, verify_store_wheel)
        app.root.after(1100, lambda: app.purchase("food", "蒜蓉空心菜"))
        app.root.after(1250, lambda: app.feed("蒜蓉空心菜"))
        app.root.after(1450, lambda: app.purchase("gift", "手写信"))
        app.root.after(1600, lambda: app.give_gift("手写信"))
        app.root.after(1850, app.open_actions)
        actions = ["wave", "jump", "dance", "think", "work", "review", "sleepy", "walk", "shy", "celebrate"]
        for index, action in enumerate(actions):
            app.root.after(2100 + index * 260, lambda name=action: app.start_action(name))
        app.root.after(4800, app.open_chat)

        def chat() -> None:
            app.chat_input.insert(0, "今天一起加油")
            app.send_chat()

        app.root.after(5200, chat)
        app.root.after(5700, app.open_statistics)
        app.root.after(6100, app.open_achievements)
        app.root.after(6500, app.open_help)
        app.root.after(6900, app.open_settings)
        app.root.after(7800, app.quit)
        app.run()
        print("GUI_SMOKE_OK")


if __name__ == "__main__":
    run()
