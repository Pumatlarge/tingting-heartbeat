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
        from tingting_pet import __version__
        from tingting_pet.app import TingtingPet
        from tkinter import ttk

        app = TingtingPet()
        assert not hasattr(app, "heart_cursor_handle"), "custom cursor runtime must remain disabled"
        assert app.canvas.cget("cursor") == "arrow"
        ex_style = app._main_window_ex_style()
        assert ex_style & 0x00000080, "pet window is not marked as a tool window"
        assert not ex_style & 0x00040000, "pet window still has the taskbar app-window style"
        real_monitor = app._monitor_info_at(app.root.winfo_x(), app.root.winfo_y())
        base_width = app.window_w
        simulated_monitor = dict(real_monitor)
        simulated_monitor["dpi"] = 144
        app._resize_window(keep_position=True, monitor_info=simulated_monitor)
        assert app.scale == app._effective_scale(app.user_scale, 144), "pet scale did not follow monitor DPI"
        assert app.window_w > base_width, "pet did not grow on the higher-DPI monitor"
        app._resize_window(keep_position=True, monitor_info=real_monitor)
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

        original_tk_scaling = float(app.root.tk.call("tk", "scaling"))

        def open_high_dpi_quick_panel() -> None:
            app.root.tk.call("tk", "scaling", 2.25)
            app.open_quick_panel(40, 40)

        app.root.after(300, open_high_dpi_quick_panel)

        def verify_quick_panel() -> None:
            panel = app.quick_panel
            panel.update()
            panel_status = app.panel_status.cget("text")
            assert "🪙" not in panel_status and str(app.state["coins"]) not in panel_status, "quick-panel status still shows coins"
            assert all(str(int(app.state[key])) in panel_status for key in ("hunger", "mood", "energy")), "quick-panel status is missing a care value"
            status_bottom = app.panel_status.winfo_y() + app.panel_status.winfo_height()
            assert status_bottom <= app.panel_status.master.winfo_height(), "quick-panel status is clipped"
            footer = app.quick_panel_footer
            assert footer.winfo_height() >= 28, "quick-panel footer is clipped"
            assert footer.winfo_y() + footer.winfo_height() <= panel.winfo_height(), "quick-panel footer is outside the window"
            monitor = app._monitor_info_at(panel.winfo_x(), panel.winfo_y())
            left, top, right, bottom = monitor["work"]
            assert left <= panel.winfo_x() and panel.winfo_x() + panel.winfo_width() <= right, "quick panel exceeds monitor width"
            assert top <= panel.winfo_y() and panel.winfo_y() + panel.winfo_height() <= bottom, "quick panel exceeds monitor height"
            button_texts = [widget.cget("text") for widget in footer.winfo_children()]
            assert app.bi("退出程序", "Quit") in button_texts, "quick-panel quit button is missing"
            app.root.tk.call("tk", "scaling", original_tk_scaling)

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
            window = app.dialogs["chat"]
            window.update()
            assert not hasattr(app, "chat_session_list") or not app.chat_session_list.winfo_exists(), "legacy chat sidebar is still visible"
            assert app.chat_new_button.winfo_rooty() < app.chat_text.winfo_rooty(), "new-chat button is not in the header"
            assert app.chat_history_button.winfo_rooty() < app.chat_text.winfo_rooty(), "history button is not in the header"
            assert app.chat_input.winfo_rooty() + app.chat_input.winfo_height() <= window.winfo_rooty() + window.winfo_height(), "chat input is outside the window"
            app.chat_input.insert(0, "今天一起加油")
            app.send_chat()

        app.root.after(5200, chat)

        def verify_chat_waiting_state() -> None:
            assert app.chat_busy, "chat did not enter its single-request waiting state"
            assert app.chat_input.cget("state") == "disabled", "chat input stayed enabled during a request"
            assert app.chat_send.cget("state") == "disabled", "chat send button stayed enabled during a request"
            assert "s" in app.chat_send.cget("text"), "chat send button does not show elapsed time"

        app.root.after(5350, verify_chat_waiting_state)

        def verify_chat_features() -> None:
            assert not app.chat_busy, "chat request did not finish"
            assert app.state["chat_sessions"], "chat sessions were not persisted"
            assert len(app.state["chat_sessions"][0]["messages"]) == 2, "chat messages were not saved"
            assert app.chat_input.cget("state") == "normal", "chat input was not re-enabled"
            app._select_all_chat_text()
            app._copy_chat_selection()
            assert "今天一起加油" in app.root.clipboard_get(), "chat text could not be copied"

        app.root.after(5750, verify_chat_features)
        app.root.after(6000, app.open_statistics)
        app.root.after(6400, app.open_achievements)
        app.root.after(6800, app.open_help)
        app.root.after(7200, app.open_settings)

        def verify_enhancement_controls() -> None:
            def descendants(widget):
                result = []
                for child in widget.winfo_children():
                    result.append(child)
                    result.extend(descendants(child))
                return result

            settings = app.dialogs.get("settings")
            achievements = app.dialogs.get("achievements")
            assert settings is not None and settings.winfo_exists(), "settings window is missing"
            assert achievements is not None and achievements.winfo_exists(), "achievements window is missing"
            visible_text = [str(item.cget("text")) for item in descendants(settings) if "text" in item.keys()]
            assert any(f"版本 {__version__}" in value for value in visible_text), "settings version does not match internal version"
            for key in ("statistics", "achievements", "help", "settings"):
                window = app.dialogs.get(key)
                assert window is not None and not bool(window.attributes("-topmost")), f"{key} window stayed topmost"
            assert len([item for item in descendants(settings) if isinstance(item, ttk.Scale)]) >= 2, "opacity slider is missing"
            assert len([item for item in descendants(achievements) if isinstance(item, ttk.Progressbar)]) >= 1, "achievement progress bars are missing"
            original_alpha = float(app.root.attributes("-alpha"))
            app.root.attributes("-alpha", 0.65)
            app.root.update_idletasks()
            assert abs(float(app.root.attributes("-alpha")) - 0.65) < 0.02, "window opacity did not apply"
            app.root.attributes("-alpha", original_alpha)

        app.root.after(7700, verify_enhancement_controls)
        app.root.after(8200, app.quit)
        app.run()
        print("GUI_SMOKE_OK")


if __name__ == "__main__":
    run()
