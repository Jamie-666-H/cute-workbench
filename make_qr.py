import qrcode

URL = "https://b5d4529665854d10afe8fefc159c3655.sh3.agentos-app.net"

qr = qrcode.QRCode(
    version=2,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=14,
    border=5,
)
qr.add_data(URL)
qr.make(fit=True)

# 粉色花朵风格二维码：粉色前景 + 白色底，中心放一个 🌸 占位（用白色块留白）
img = qr.make_image(fill_color="#ff5fa2", back_color="#fff5f8").convert("RGB")

# 中心贴一个粉色圆，方便识别（纯装饰，不破坏可扫码性，因 ERROR_CORRECT_H 容错高）
from PIL import Image, ImageDraw

w, h = img.size
cx, cy = w // 2, h // 2
r = int(min(w, h) * 0.13)
overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
d = ImageDraw.Draw(overlay)
d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 222, 235, 255))
d.ellipse([cx - int(r * 0.6), cy - int(r * 0.6), cx + int(r * 0.6), cy + int(r * 0.6)], fill=(255, 159, 196, 255))
img = img.convert("RGBA").copy()
img.alpha_composite(overlay)
img = img.convert("RGB")

img.save("app-qrcode.png")
print("saved", img.size)
