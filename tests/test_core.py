from __future__ import annotations

import struct
import unittest

from PIL import Image

from tingting_pet.app import TingtingPet, resource_path
from tingting_pet.catalog import FOOD_BY_NAME, GIFT_BY_NAME, LOGICAL_ACTIONS, RECOVERY_BY_NAME
from tingting_pet.storage import default_state, protect_secret, unprotect_secret
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
        icon_names = ["wave", "jump", "dance", "think", "work", "review", "sleepy", "walk", "shy", "celebrate"]
        self.assertTrue(all(resource_path(f"assets/action-icons/{name}.png").is_file() for name in icon_names))
        cursor_data = resource_path("assets/heart.cur").read_bytes()
        self.assertEqual(cursor_data[:6], struct.pack("<HHH", 0, 2, 1))
        self.assertGreater(TingtingPet._frame_interval("desk_sleep"), TingtingPet._frame_interval("idle") * 10)

    def test_english_language_defaults_and_catalog_coverage(self) -> None:
        self.assertEqual(default_state()["settings"]["language"], "zh-CN")
        self.assertEqual(text("设置", "en"), "Settings")
        self.assertEqual(len(ACHIEVEMENT_TEXT), 37)
        self.assertGreaterEqual(len(ACTION_LABELS), len(LOGICAL_ACTIONS))
        self.assertIn("蒜蓉空心菜", ITEM_NAMES)

    def test_bubble_text_wraps_to_measured_width(self) -> None:
        class FakeFont:
            @staticmethod
            def measure(text: str) -> int:
                return len(text) * 10

        wrapped = TingtingPet._wrap_bubble_text("这里不可以随便碰啦，请尊重一点。", FakeFont(), 70)
        self.assertGreater(len(wrapped.splitlines()), 1)
        self.assertTrue(all(len(line) <= 7 for line in wrapped.splitlines()))

    def test_heart_cursor_only_activates_on_visible_character_pixels(self) -> None:
        pet = TingtingPet.__new__(TingtingPet)
        pet.bubble_h = 80
        pet.last_rendered_alpha = Image.new("L", (20, 30), 0)
        pet.last_rendered_alpha.putpixel((10, 12), 255)
        self.assertTrue(pet._cursor_over_character(10, 92))
        self.assertFalse(pet._cursor_over_character(9, 92))
        self.assertFalse(pet._cursor_over_character(10, 79))

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
        secret = "test-key-never-package"
        self.assertEqual(unprotect_secret(protect_secret(secret)), secret)

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
