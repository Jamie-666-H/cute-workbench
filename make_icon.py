import os
from PIL import Image, ImageDraw


def make_icon(path, size=256):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    # 圆角粉色底
    d.rounded_rectangle([14, 14, size - 14, size - 14], radius=58,
                        fill=(255, 111, 165, 255))

    cx, cy = size // 2, size // 2
    petal_r = size * 0.20
    dist = size * 0.17
    # 五个白色花瓣
    for i in range(5):
        ang = -90 + i * 72
        import math
        px = cx + dist * math.cos(math.radians(ang))
        py = cy + dist * math.sin(math.radians(ang))
        d.ellipse([px - petal_r, py - petal_r, px + petal_r, py + petal_r],
                  fill=(255, 255, 255, 255))
    # 花心
    cr = size * 0.16
    d.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=(255, 224, 236, 255))

    # 生成多尺寸 ICO
    img.save(path, sizes=[(256, 256), (128, 128), (64, 64),
                          (48, 48), (32, 32), (16, 16)])
    print("icon saved:", path)


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon.ico")
    make_icon(out)
