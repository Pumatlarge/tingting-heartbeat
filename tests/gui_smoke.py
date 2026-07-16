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
        assert not hasattr(app, "heart_cursor_handle"), "custom cursor runtime must remain disabled"
        assert app.canvas.cget("cursor") == "arrow"
        ex_style = app._main_window_ex_style()
        assert ex_style & 0x00000080, "pet window is not marked as a tool window"
        assert not ex_style & 0x00040000, "pet window still has the taskbar app-window style"
        app.state["coins"] = 2000
        bbox = app.last_rendered_alpha.getbbox()
        assert bbox is not None
        center_x, center_y = (bbox[0] + bbox[2]) // 2, (bbox[1] + bbox[3]) // 2
        visible_point = min(
            (
                (x, y)
                for y in range(bbox[1], bbox[3])
                for x in range(bbox[0], bbox[2])
                if app.last_rendered_alpha.getpixel((x, y)) >= 24
            ),
            key=lambda point: (point[0] - center_x) ** 2 + (point[1] - center_y) ** 2,
        )
        app.handle_part_click(*visible_point)
        assert app.click_light_point == (float(visible_point[0]), float(visible_point[1]))
        assert app.click_light_started > 0
        app.say("保持一点礼貌距离，\n我们还是好朋友。\n谢谢你的理解。")

        def verify_bubble_layout() -> None:
            items = app.canvas.find_withtag("bubble")
            text_item = next(item for item in items if app.canvas.type(item) == "text")
            shape_item = next(item for item in items if app.canvas.type(item) == "polygon")
            text_box = app.canvas.bbox(text_item)
            shape_box = app.canvas.bbox(shape_item)
            assert text_box[1] >= shape_box[1] + 6, "bubble text overlaps the top border"
            assert text_box[3] <= shape_box[3] - 8, "bubble text overlaps the bottom/tail"

        app.root.after(300, lambda: app.open_quick_panel(40, 40))

        def verify_quick_panel() -> None:
            panel = app.quick_panel
            panel.update()
            panel_status = app.panel_status.cget("text")
            assert "🪙" not in panel_status and str(app.state["coins"]) not in panel_status, "quick-panel status still shows coins"
            assert all(str(int(app.state[key])) in panel_status for key in ("hunger", "mood", "energy")), "quick-panel status is missing a care value"
            status_bottom = app.panel_status.winfo_y() + app.panel_status.winfo_height()
            assert status_bottom <= app.panel_status.master.winfo_height(), "quick-panel status is clipped"
            footer = panel.winfo_children()[0].winfo_children()[-1]
            assert footer.winfo_height() >= 28, "quick-panel footer is clipped"
            assert footer.winfo_y() + footer.winfo_height() <= panel.winfo_height(), "quick-panel footer is outside the window"
            button_texts = [widget.cget("text") for widget in footer.winfo_children()]
            assert app.bi("退出程序", "Quit") in button_texts, "quick-panel quit button is missing"

        app.root.after(150, verify_bubble_layout)
        app.root.after(500, verify_quick_panel)
        app.root.after(700, app.open_store)

        def verify_store_wheel() -> None:
            window = app.dialogs["store"]
            window.update()
            canvas = next(item for item in window._wheel_canvases if item.winfo_ismapped())
            canvas.update_idletasks()
            content_bounds = canvas.bbox("all")
            assert content_bounds is not None and content_bounds[2] >= canvas.winfo_width() - 3, "store catalog does not fill the canvas width"
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
