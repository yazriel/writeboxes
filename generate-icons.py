#!/usr/bin/env python3
"""Generate WS icons for WriteBoxes: favicon.ico + manifest PNGs."""
import struct, zlib, os
from PIL import Image, ImageDraw, ImageFont

FONT_PATH = os.path.join(os.path.dirname(__file__), 'NotoSans-Light.ttf')
ICO_SIZES = [16, 24, 32, 48, 64]
PNG_SIZES = [192, 512]


def create_ico(images):
    """Create ICO file from list of PIL Images."""
    entries = []
    all_data = b''
    for img in images:
        w, h = img.size
        rgba = img.convert('RGBA')
        pixels = b''
        for y in range(h - 1, -1, -1):
            for x in range(w):
                r, g, b, a = rgba.getpixel((x, y))
                pixels += struct.pack('BBBB', b, g, r, a)
        and_mask = b'\x00' * (((w + 31) // 32) * 4 * h)
        bmp_header = struct.pack('<IiiHHIIiiII',
            40, w, h * 2, 1, 32, 0,
            len(pixels) + len(and_mask),
            0, 0, 0, 0)
        entry_data = bmp_header + pixels + and_mask
        entries.append((w, h, entry_data))
        all_data += entry_data

    header = struct.pack('<HHH', 0, 1, len(entries))
    dir_size = 6 + len(entries) * 16
    dir_entries = b''
    data_offset = dir_size
    for w, h, entry_data in entries:
        w_byte = 0 if w >= 256 else w
        h_byte = 0 if h >= 256 else h
        dir_entries += struct.pack('<BBBBHHII', w_byte, h_byte, 0, 0, 1, 32, len(entry_data), data_offset)
        data_offset += len(entry_data)
    return header + dir_entries + all_data


def render_text(size, text='WS'):
    """Render 'WS' text on white background, tight horizontal margins."""
    img = Image.new('RGBA', (size, size), (255, 255, 255, 255))
    draw = ImageDraw.Draw(img)
    font_size = int(size * 0.6)
    try:
        font = ImageFont.truetype(FONT_PATH, font_size)
    except OSError:
        font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (size - tw) // 2 - bbox[0]
    y = (size - th) // 2 - bbox[1]
    draw.text((x, y), text, fill=(0, 0, 0, 255), font=font)
    return img


os.makedirs('icon', exist_ok=True)

ico_images = [render_text(s) for s in ICO_SIZES]
with open('icon/favicon.ico', 'wb') as f:
    f.write(create_ico(ico_images))
print(f'Created icon/favicon.ico ({len(ICO_SIZES)} sizes: {ICO_SIZES})')

for sz in PNG_SIZES:
    img = render_text(sz)
    img.save(f'icon/icon-{sz}.png', 'PNG')
    print(f'Created icon/icon-{sz}.png')
