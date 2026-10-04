"""Generate a QR code for the Sunita Traders website once it is hosted.
Usage:  python3 make_qr.py https://your-link-here
Output: qr-website.png (QR only) + qr-website-poster.png (print-ready)
"""
import sys
import qrcode

url = sys.argv[1] if len(sys.argv) > 1 else "https://wa.me/917976943373?text=Namaste!%20Mujhe%20Sunita%20Traders%20catalog%20chahiye"
qr = qrcode.QRCode(box_size=12, border=2)
qr.add_data(url)
qr.make(fit=True)
img = qr.make_image(fill_color="#4A0E0E", back_color="white").convert("RGB")
img.save("qr-website.png")
print(f"Saved qr-website.png for: {url}")
