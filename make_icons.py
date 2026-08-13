"""生成粉色可爱风 App 图标：192 / 512 / 180(apple-touch) 三种尺寸。"""
from PIL import Image, ImageDraw, ImageFilter
import math

def make_icon(size):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    S = size
    # 背景圆角矩形（覆盖整图，maskable 安全）
    bg = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    bd = ImageDraw.Draw(bg)
    r = int(S * 0.22)
    bd.rounded_rectangle([0, 0, S, S], radius=r, fill=(255, 158, 196, 255))
    # 叠一层更浅的渐变感（用半透明高光圆）
    hl = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    hd = ImageDraw.Draw(hl)
    hd.ellipse([int(S*0.08), int(S*0.04), int(S*0.92), int(S*0.62)], fill=(255, 209, 232, 120))
    bg = Image.alpha_composite(bg, hl)
    img = bg

    d = ImageDraw.Draw(img)
    cx, cy = S * 0.5, S * 0.52
    petal_len = S * 0.30
    petal_w = S * 0.16
    # 花瓣（6 片）
    for i in range(6):
        ang = math.radians(i * 60 - 90)
        px = cx + math.cos(ang) * petal_len * 0.55
        py = cy + math.sin(ang) * petal_len * 0.55
        pdx = math.cos(ang) * petal_len
        pdy = math.sin(ang) * petal_len
        # 用旋转椭圆画花瓣
        bbox = [px - petal_w/2, py - petal_len/2, px + petal_w/2, py + petal_len/2]
        petal = Image.new("RGBA", (S, S), (0, 0, 0, 0))
        pd = ImageDraw.Draw(petal)
        pd.ellipse(bbox, fill=(255, 255, 255, 235))
        petal = petal.rotate(math.degrees(ang) + 90, center=(px, py))
        img = Image.alpha_composite(img, petal)
    # 花心
    d.ellipse([cx - S*0.13, cy - S*0.13, cx + S*0.13, cy + S*0.13], fill=(255, 111, 165, 255))
    d.ellipse([cx - S*0.075, cy - S*0.075, cx + S*0.075, cy + S*0.075], fill=(255, 224, 238, 255))
    # 柔化一点点
    img = img.filter(ImageFilter.GaussianBlur(0.4))
    return img

for name, sz in [("icon-192.png", 192), ("icon-512.png", 512), ("apple-touch-icon.png", 180)]:
    make_icon(sz).save(name)
    print("saved", name)
