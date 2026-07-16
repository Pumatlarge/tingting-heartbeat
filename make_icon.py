from pathlib import Path
import io
import struct

from PIL import Image, ImageDraw


root = Path(__file__).resolve().parent
icon_source = Image.open(root / "assets" / "tingting-heartbeat-icon.png").convert("RGBA")
canvas = icon_source.resize((256, 256), Image.Resampling.LANCZOS)
canvas.save(root / "assets" / "tingting.ico", sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
print(root / "assets" / "tingting.ico")


def heart_shape(draw: ImageDraw.ImageDraw, offset=(0, 0), color="#df4f78", outline="#ffffff", scale=1) -> None:
    ox, oy = offset
    width = 1.5
    draw.ellipse((ox + 3 * scale, oy + 2 * scale, ox + 17 * scale, oy + 16 * scale), fill=outline)
    draw.ellipse((ox + 13 * scale, oy + 2 * scale, ox + 27 * scale, oy + 16 * scale), fill=outline)
    draw.polygon(((ox + 3 * scale, oy + 9 * scale), (ox + 27 * scale, oy + 9 * scale), (ox + 15 * scale, oy + 29 * scale)), fill=outline)
    inset = width
    draw.ellipse((ox + (3 + inset) * scale, oy + (2 + inset) * scale, ox + (17 - inset) * scale, oy + (16 - inset) * scale), fill=color)
    draw.ellipse((ox + (13 + inset) * scale, oy + (2 + inset) * scale, ox + (27 - inset) * scale, oy + (16 - inset) * scale), fill=color)
    draw.polygon(((ox + (3 + inset) * scale, oy + 9 * scale), (ox + (27 - inset) * scale, oy + 9 * scale), (ox + 15 * scale, oy + (29 - inset) * scale)), fill=color)


cursor_large = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
cursor_draw = ImageDraw.Draw(cursor_large)
# A broad, compact heart reads clearly as a cursor and does not feel vertically stretched.
cursor_draw.ellipse((6, 18, 66, 78), fill="#ffffff")
cursor_draw.ellipse((62, 18, 122, 78), fill="#ffffff")
cursor_draw.polygon(((6, 50), (122, 50), (64, 116)), fill="#ffffff")
cursor_draw.ellipse((12, 24, 65, 75), fill="#df4f78")
cursor_draw.ellipse((63, 24, 116, 75), fill="#df4f78")
cursor_draw.polygon(((12, 52), (116, 52), (64, 108)), fill="#df4f78")
cursor = cursor_large.resize((32, 32), Image.Resampling.LANCZOS)
cursor.save(root / "assets" / "heart-cursor.png")
png_buffer = io.BytesIO()
cursor.save(png_buffer, format="PNG")
png_data = png_buffer.getvalue()
cur_header = struct.pack("<HHH", 0, 2, 1)
cur_entry = struct.pack("<BBBBHHII", 32, 32, 0, 0, 16, 27, len(png_data), 22)
(root / "assets" / "heart.cur").write_bytes(cur_header + cur_entry + png_data)


icons_dir = root / "assets" / "action-icons"
icons_dir.mkdir(parents=True, exist_ok=True)


def base_icon():
    image = Image.new("RGBA", (56, 56), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((2, 2, 53, 53), radius=15, fill="#f6e7ec", outline="#e5bdca", width=2)
    return image, draw


def save_action(name, painter):
    image, draw = base_icon()
    painter(draw)
    image.save(icons_dir / f"{name}.png")


ink = "#84344e"
gold = "#e7ae42"

save_action("wave", lambda d: (d.ellipse((19, 20, 36, 39), fill=ink), d.line((21, 23, 14, 11), fill=ink, width=4), d.line((25, 21, 22, 8), fill=ink, width=4), d.line((30, 21, 31, 8), fill=ink, width=4), d.line((34, 24, 40, 13), fill=ink, width=4)))
save_action("jump", lambda d: (d.polygon(((28, 8), (17, 23), (24, 23), (24, 40), (32, 40), (32, 23), (39, 23)), fill=ink), d.ellipse((12, 43, 44, 48), fill=gold)))
save_action("dance", lambda d: (d.ellipse((13, 34, 22, 43), fill=ink), d.line((21, 37, 21, 14, 37, 10, 37, 30), fill=ink, width=4), d.ellipse((33, 27, 42, 36), fill=ink), d.ellipse((9, 12, 15, 18), fill=gold)))
save_action("think", lambda d: (d.ellipse((13, 12, 42, 34), fill="#ffffff", outline=ink, width=3), d.ellipse((17, 37, 23, 43), fill=ink), d.ellipse((11, 44, 15, 48), fill=ink), d.ellipse((21, 20, 25, 24), fill=gold), d.ellipse((28, 20, 32, 24), fill=gold), d.ellipse((35, 20, 39, 24), fill=gold)))
save_action("work", lambda d: (d.rounded_rectangle((10, 13, 46, 37), radius=3, fill="#ffffff", outline=ink, width=3), d.rectangle((25, 37, 31, 44), fill=ink), d.rounded_rectangle((17, 44, 39, 48), radius=2, fill=ink), d.ellipse((26, 23, 31, 28), fill=gold)))
save_action("review", lambda d: (d.ellipse((10, 9, 36, 35), outline=ink, width=5), d.line((33, 32, 46, 46), fill=ink, width=6), d.line((18, 22, 25, 28, 34, 16), fill=gold, width=3)))
save_action("sleepy", lambda d: (d.ellipse((11, 10, 40, 40), fill=ink), d.ellipse((21, 5, 47, 34), fill="#f6e7ec"), d.line((31, 36, 40, 36, 31, 45, 40, 45), fill=gold, width=3)))
save_action("walk", lambda d: (d.ellipse((16, 9, 28, 25), fill=ink), d.ellipse((30, 28, 42, 44), fill=ink), d.ellipse((12, 28, 20, 37), fill=gold), d.ellipse((38, 10, 45, 20), fill=gold)))
save_action("shy", lambda d: (d.ellipse((13, 13, 43, 43), fill="#ffffff", outline=ink, width=3), d.arc((20, 24, 36, 37), 10, 170, fill=ink, width=3), d.ellipse((17, 27, 23, 31), fill="#e95e88"), d.ellipse((33, 27, 39, 31), fill="#e95e88")))
save_action("celebrate", lambda d: (d.polygon(((28, 7), (33, 20), (47, 21), (36, 30), (40, 44), (28, 36), (16, 44), (20, 30), (9, 21), (23, 20)), fill=gold, outline=ink), d.ellipse((8, 10, 13, 15), fill="#df4f78"), d.ellipse((43, 8, 48, 13), fill="#6e9bc2")))

print(root / "assets" / "heart.cur")
print(icons_dir)
