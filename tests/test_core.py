from __future__ import annotations

import struct
import unittest
from datetime import date, timedelta
from types import SimpleNamespace

from PIL import Image

from tingting_pet import __version__
from tingting_pet.app import TingtingPet, resource_path
from tingting_pet.catalog import ACHIEVEMENTS, FOOD_BY_NAME, GIFT_BY_NAME, LOGICAL_ACTIONS, RECOVERY_BY_NAME
from tingting_pet.storage import _migrate_state, _record_launch, default_state, protect_secret, unprotect_secret
from tingting_pet.i18n import ACHIEVEMENT_TEXT, ACTION_LABELS, ITEM_NAMES, text


class CoreTests(unittest.TestCase):
    def make_pet(self) -> TingtingPet:
        pet = TingtingPet.__new__(TingtingPet)
        pet.state = default_state()
        pet.settings = pet.state["settings"]
        pet.say = lambda *_args, **_kwargs: None
        pet.save = lambda: None
        pet._refresh_store = lambda: None
        pet.check_achievements = lambda **_kwargs: None
        pet.start_action = lambda *_args, **_kwargs: None
        return pet

    def test_hit_zones(self) -> None:
        samples = {
            "hair": (0.2, 0.16), "face": (0.5, 0.2), "chest": (0.5, 0.4),
            "arms": (0.2, 0.4), "skirt": (0.5, 0.72),
        }
        self.assertEqual({name: TingtingPet._classify_visible_point(*point) for name, point in samples.items()}, {name: name for name in samples})

    def test_action_menu_effects_are_unique(self) -> None:
        names = ["wave", "jump", "dance", "think", "work", "review", "sleepy", "walk", "shy", "celebrate"]
        effects = [LOGICAL_ACTIONS[name].get("effect", name) for name in names]
        self.assertEqual(len(effects), len(set(effects)))

    def test_desktop_sleep_action_and_ui_assets(self) -> None:
        self.assertEqual(LOGICAL_ACTIONS["desk_sleep"]["effect"], "desk_sleep")
        self.assertGreaterEqual(LOGICAL_ACTIONS["desk_sleep"]["duration"], 300)
        self.assertLess(TingtingPet._sprite_scale_for_effect("desk_sleep"), 1.0)
        self.assertEqual(TingtingPet._sprite_scale_for_effect("idle"), 1.0)
        icon_names = ["wave", "jump", "dance", "think", "work", "review", "sleepy", "walk", "shy", "celebrate"]
        self.assertTrue(all(resource_path(f"assets/action-icons/{name}.png").is_file() for name in icon_names))
        cursor_data = resource_path("assets/heart.cur").read_bytes()
        self.assertEqual(cursor_data[:6], struct.pack("<HHH", 0, 2, 1))
        self.assertGreater(TingtingPet._frame_interval("desk_sleep"), TingtingPet._frame_interval("idle") * 10)

    def test_drag_direction_selects_matching_running_row(self) -> None:
        self.assertEqual(TingtingPet._directional_running_row(1), "running-right")
        self.assertEqual(TingtingPet._directional_running_row(-1), "running-left")

    def test_drag_motion_updates_direction_and_restarts_animation(self) -> None:
        class FakeRoot:
            geometry_value = ""

            def geometry(self, value: str) -> None:
                self.geometry_value = value

        pet = TingtingPet.__new__(TingtingPet)
        pet.root = FakeRoot()
        pet.drag_start = (100, 100, 10, 20)
        pet.drag_last_x = 100
        pet.dragged = False
        pet.walk_direction = 1
        pet.frame_cursor = 5
        pet.last_frame_time = 99.0
        pet.window_w = 200
        pet.window_h = 300
        pet._monitor_info_at = lambda *_args: {"work": (0, 0, 1920, 1040)}

        pet._on_drag(SimpleNamespace(x_root=90, y_root=110))
        self.assertTrue(pet.dragged)
        self.assertEqual(pet.walk_direction, -1)
        self.assertEqual((pet.frame_cursor, pet.last_frame_time), (0, 0.0))
        self.assertEqual(pet.root.geometry_value, "+0+30")

        pet._on_drag(SimpleNamespace(x_root=105, y_root=110))
        self.assertEqual(pet.walk_direction, 1)
        self.assertEqual(pet.root.geometry_value, "+15+30")

    def test_english_language_defaults_and_catalog_coverage(self) -> None:
        self.assertRegex(__version__, r"^\d+\.\d+\.\d+$")
        self.assertEqual(default_state()["settings"]["language"], "zh-CN")
        self.assertEqual(text("设置", "en"), "Settings")
        self.assertEqual(len(ACHIEVEMENT_TEXT), len(ACHIEVEMENTS))
        self.assertGreaterEqual(len(ACHIEVEMENTS), 50)
        self.assertGreaterEqual(len(ACTION_LABELS), len(LOGICAL_ACTIONS))
        self.assertIn("蒜蓉空心菜", ITEM_NAMES)

    def test_packaging_versions_match_internal_version(self) -> None:
        installer = resource_path("installer.iss").read_text(encoding="utf-8")
        build_script = resource_path("build-installer.ps1").read_text(encoding="utf-8")
        self.assertIn(f'#define MyAppVersion "{__version__}"', installer)
        self.assertIn(f"[string]$Version = '{__version__}'", build_script)

    def test_bubble_text_wraps_to_measured_width(self) -> None:
        class FakeFont:
            @staticmethod
            def measure(text: str) -> int:
                return len(text) * 10

        wrapped = TingtingPet._wrap_bubble_text("这里不可以随便碰啦，请尊重一点。", FakeFont(), 70)
        self.assertGreater(len(wrapped.splitlines()), 1)
        self.assertTrue(all(len(line) <= 7 for line in wrapped.splitlines()))
        self.assertEqual(TingtingPet._bubble_font_size(0.5), 8)
        self.assertEqual(TingtingPet._bubble_font_size(0.82), 8)
        self.assertEqual(TingtingPet._bubble_font_size(1.0), 9)
        self.assertEqual(TingtingPet._bubble_font_size(1.6), 10)

    def test_multi_monitor_dpi_scale_and_negative_work_area(self) -> None:
        self.assertEqual(TingtingPet._effective_scale(0.82, 96), 0.82)
        self.assertEqual(TingtingPet._effective_scale(0.82, 144), 1.23)
        self.assertEqual(TingtingPet._effective_scale(0.82, 192), 1.64)
        work_area = (-1920, 0, 0, 1040)
        x, y = TingtingPet._clamp_to_work_area(-100, 900, 320, 570, work_area, padding=8)
        self.assertEqual((x, y), (-328, 462))
        self.assertGreaterEqual(x, work_area[0] + 8)
        self.assertLessEqual(x + 320, work_area[2] - 8)
        self.assertGreaterEqual(y, work_area[1] + 8)
        self.assertLessEqual(y + 570, work_area[3] - 8)
        self.assertEqual(TingtingPet._geometry_position(-1800, 24), "+-1800+24")
        self.assertEqual(TingtingPet._clamp_pet_to_work_area(-900, -900, 200, 300, (0, 0, 1920, 1040)), (-100, -150))
        self.assertEqual(TingtingPet._clamp_pet_to_work_area(3000, 2000, 200, 300, (0, 0, 1920, 1040)), (1820, 890))
        self.assertEqual(TingtingPet._quick_panel_dimensions(320, 730, work_area), (320, 730))
        short_work_area = (0, 0, 1280, 650)
        self.assertEqual(TingtingPet._quick_panel_dimensions(410, 900, short_work_area), (410, 634))

    def test_click_light_is_clipped_to_character_alpha(self) -> None:
        image = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
        for y in range(18, 47):
            for x in range(20, 45):
                image.putpixel((x, y), (120, 40, 60, 255))
        before = image.copy()
        result = TingtingPet._compose_click_light(image, (32, 32), 0.25)
        self.assertEqual(result.getchannel("A").tobytes(), before.getchannel("A").tobytes())
        self.assertEqual(result.getpixel((5, 5)), (0, 0, 0, 0))
        self.assertNotEqual(result.getpixel((32, 32)), before.getpixel((32, 32)))

    def test_achievement_reward_can_only_be_claimed_once(self) -> None:
        pet = self.make_pet()
        pet.state["achievements"]["first_meet"] = "2026-07-16 13:00"
        before = pet.state["coins"]
        expected = TingtingPet._achievement_reward("first_meet", 1)
        self.assertEqual(pet._claim_achievement_ids(["first_meet"]), expected)
        self.assertEqual(pet.state["coins"], before + expected)
        self.assertEqual(pet._claim_achievement_ids(["first_meet"]), 0)
        self.assertEqual(pet.state["coins"], before + expected)

    def test_purchase_and_use_food_gift_recovery(self) -> None:
        pet = self.make_pet()
        pet.state["coins"] = 1000
        food = "蒜蓉空心菜"
        gift = "手写信"
        recovery = "元气营养包"
        pet.purchase("food", food)
        self.assertEqual(pet.state["inventory_food"][food], 1)
        pet.feed(food)
        self.assertEqual(pet.state["inventory_food"][food], 0)
        self.assertEqual(pet.state["feeds"], 1)
        pet.purchase("gift", gift)
        pet.give_gift(gift)
        self.assertEqual(pet.state["gifts_given"], 1)
        pet.state["inventory_recovery"][recovery] = 1
        pet.state["energy"] = 10
        pet.use_recovery(recovery)
        self.assertGreater(pet.state["energy"], 10)
        expected_spend = FOOD_BY_NAME[food]["price"] + GIFT_BY_NAME[gift]["price"]
        self.assertEqual(pet.state["coins_spent"], expected_spend)
        self.assertIn(recovery, RECOVERY_BY_NAME)

    def test_api_key_default_and_dpapi_roundtrip(self) -> None:
        self.assertEqual(default_state()["settings"]["api_key_protected"], "")
        self.assertFalse(default_state()["settings"]["web_search_enabled"])
        self.assertTrue(default_state()["settings"]["auto_check_updates"])
        self.assertEqual(default_state()["settings"]["opacity"], 1.0)
        self.assertEqual(default_state()["chat_sessions"], [])
        secret = "test-key-never-package"
        self.assertEqual(unprotect_secret(protect_secret(secret)), secret)

    def test_launch_day_achievements_use_cumulative_days(self) -> None:
        day_metrics = {ach_id: metric for ach_id, _title, _desc, metric, _target in ACHIEVEMENTS if ach_id.startswith("streak_")}
        self.assertTrue(day_metrics)
        self.assertEqual(set(day_metrics.values()), {"total_launch_days"})

        state = default_state()
        state["last_open_date"] = (date.today() - timedelta(days=3)).isoformat()
        _record_launch(state)
        self.assertEqual(state["total_launch_days"], 1)
        self.assertEqual(state["streak_days"], 1)
        _record_launch(state)
        self.assertEqual(state["total_launch_days"], 1)

        legacy = default_state()
        legacy.pop("total_launch_days")
        legacy["streak_days"] = 12
        _migrate_state(legacy)
        self.assertEqual(legacy["total_launch_days"], 12)

    def test_achievement_progress_and_opacity_helpers(self) -> None:
        pet = self.make_pet()
        self.assertIn("2 天 / 7 天", pet._achievement_progress_text("total_launch_days", 2, 7))
        self.assertIn("50%", pet._achievement_progress_text("clicks", 5, 10))
        self.assertEqual(TingtingPet._clamp_opacity(0.1), 0.4)
        self.assertEqual(TingtingPet._clamp_opacity(0.75), 0.75)
        self.assertEqual(TingtingPet._clamp_opacity(2), 1.0)

    def test_thousand_hour_achievement_unlocks(self) -> None:
        achievement = next(item for item in ACHIEVEMENTS if item[0] == "companion_1000h")
        self.assertEqual(achievement[3:], ("companion_seconds", 1000 * 3600))
        pet = self.make_pet()
        pet.state["companion_seconds"] = 1000 * 3600
        TingtingPet.check_achievements(pet, defer_message=True)
        self.assertIn("companion_1000h", pet.state["achievements"])

    def test_care_alert_thresholds_actions_and_recovery_reset(self) -> None:
        pet = self.make_pet()
        alerts = []
        pet.start_action = lambda action, message: alerts.append((action, message))
        pet.last_care_alert_at = 0.0
        self.assertEqual(TingtingPet._care_alert_level(50), 0)
        self.assertEqual(TingtingPet._care_alert_level(49.9), 1)
        self.assertEqual(TingtingPet._care_alert_level(10), 1)
        self.assertEqual(TingtingPet._care_alert_level(9.9), 2)

        pet.state["hunger"] = 49
        self.assertTrue(pet._check_care_alerts(100))
        self.assertEqual(alerts[-1][0], "hungry")
        pet.state["hunger"] = 9
        self.assertTrue(pet._check_care_alerts(110))
        self.assertEqual(alerts[-1][0], "starving")
        pet.state["hunger"] = 80
        self.assertFalse(pet._check_care_alerts(120))
        self.assertEqual(pet.state["care_alert_levels"]["hunger"], 0)

        cases = {"mood": ("lonely", "heartbroken"), "energy": ("tired", "exhausted")}
        now = 130
        for metric, actions in cases.items():
            pet.state[metric] = 49
            self.assertTrue(pet._check_care_alerts(now))
            self.assertEqual(alerts[-1][0], actions[0])
            now += 10
            pet.state[metric] = 9
            self.assertTrue(pet._check_care_alerts(now))
            self.assertEqual(alerts[-1][0], actions[1])
            now += 10

    def test_default_care_alert_levels_start_clear(self) -> None:
        self.assertEqual(default_state()["care_alert_levels"], {"hunger": 0, "mood": 0, "energy": 0})

    def test_mood_decay_accelerates_with_neglect(self) -> None:
        fresh = TingtingPet._mood_decay_per_minute(0)
        six_hours = TingtingPet._mood_decay_per_minute(6)
        one_day = TingtingPet._mood_decay_per_minute(24)
        self.assertGreater(six_hours, fresh)
        self.assertGreater(one_day, six_hours)

    def test_chat_sessions_response_parsing_and_bubble_excerpt(self) -> None:
        pet = self.make_pet()
        session = pet._new_chat_session(render=False)
        session["messages"].append({"role": "user", "content": "请记住这段对话", "created_at": 1.0})
        pet.state["active_chat_id"] = session["id"]
        pet._normalize_chat_sessions()
        self.assertEqual(pet.chat_history[0]["content"], "请记住这段对话")
        self.assertEqual(TingtingPet._api_endpoint("https://api.openai.com/v1/chat/completions", "responses"), "https://api.openai.com/v1/responses")
        response = {"output": [{"type": "message", "content": [{"type": "output_text", "text": "联网回答", "annotations": [{"type": "url_citation", "title": "示例来源", "url": "https://example.com/source"}]}]}]}
        parsed = TingtingPet._extract_responses_text(response)
        self.assertIn("联网回答", parsed)
        self.assertIn("https://example.com/source", parsed)
        excerpt = TingtingPet._bubble_reply_excerpt("这是一段很长的回答，应该只在人物头顶显示简短摘要，剩余内容使用省略号处理。")
        self.assertLessEqual(len(excerpt), 32)
        self.assertTrue(excerpt.endswith("..."))

    def test_premultiplied_resize_preserves_transparency(self) -> None:
        image = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
        for y in range(4, 12):
            for x in range(4, 12):
                image.putpixel((x, y), (160, 40, 60, 255))
        resized = TingtingPet._resize_rgba(image, (64, 64))
        self.assertEqual(resized.getpixel((0, 0)), (0, 0, 0, 0))
        self.assertEqual(resized.getchannel("A").getextrema(), (0, 255))

    def test_blush_marks_stay_on_detected_face(self) -> None:
        atlas = Image.open(resource_path("assets/spritesheet.webp")).convert("RGBA")
        frame = atlas.crop((192, 3 * 208, 384, 4 * 208))
        pet = TingtingPet.__new__(TingtingPet)
        pet.scale = 1.0
        face = TingtingPet._find_face_bbox(frame)
        decorated = pet._decorate_effect(frame, "blush", 1.0)
        changed = []
        for y in range(frame.height):
            for x in range(frame.width):
                if frame.getpixel((x, y)) != decorated.getpixel((x, y)):
                    changed.append((x, y))
        self.assertTrue(changed)
        left, top, right, bottom = face
        self.assertTrue(all(left - 3 <= x <= right + 3 and top <= y <= bottom + 3 for x, y in changed))

    def test_smile_effect_does_not_draw_a_line_across_face_center(self) -> None:
        atlas = Image.open(resource_path("assets/spritesheet.webp")).convert("RGBA")
        frame = atlas.crop((0, 0, 192, 208))
        pet = TingtingPet.__new__(TingtingPet)
        pet.scale = 1.0
        left, _top, right, _bottom = TingtingPet._find_face_bbox(frame)
        center = (left + right) / 2
        decorated = pet._decorate_effect(frame, "smile", 1.0)
        changed = [(x, y) for y in range(frame.height) for x in range(frame.width) if frame.getpixel((x, y)) != decorated.getpixel((x, y))]
        self.assertTrue(changed)
        self.assertTrue(all(abs(x - center) > (right - left) * 0.12 for x, _y in changed))

    def test_guard_effect_adds_no_translucent_block(self) -> None:
        atlas = Image.open(resource_path("assets/spritesheet.webp")).convert("RGBA")
        frame = atlas.crop((4 * 192, 5 * 208, 5 * 192, 6 * 208))
        pet = TingtingPet.__new__(TingtingPet)
        pet.scale = 1.0
        decorated = pet._decorate_effect(frame, "guard", 1.0)
        changed_alpha = [decorated.getpixel((x, y))[3] for y in range(frame.height) for x in range(frame.width) if frame.getpixel((x, y)) != decorated.getpixel((x, y))]
        self.assertTrue(changed_alpha)
        self.assertTrue(all(alpha == 255 for alpha in changed_alpha))


if __name__ == "__main__":
    unittest.main()
