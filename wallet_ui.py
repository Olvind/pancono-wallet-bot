from PIL import Image, ImageDraw, ImageFont
import qrcode
import os

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")
FONT_PATH = os.path.join(ASSETS_DIR, "arial.ttf")
LOGO_PATH = os.path.join(ASSETS_DIR, "logo.png")

def generate_gradient(width, height, color1=(30,30,60), color2=(70,0,130)):
    base = Image.new('RGB', (width, height), color1)
    top = Image.new('RGB', (width, height), color2)
    mask = Image.new('L', (width, height))
    for y in range(height):
        mask.putpixel((0,y), int(255*y/height))
    mask = mask.resize((width, height))
    base.paste(top, (0,0), mask)
    return base

def generate_wallet_card(address, balance, referral_code):
    width, height = 600, 300
    card = generate_gradient(width, height, (30,30,60), (70,0,130))
    draw = ImageDraw.Draw(card)
    font_large = ImageFont.truetype(FONT_PATH, 28)
    font_small = ImageFont.truetype(FONT_PATH, 20)

    if os.path.exists(LOGO_PATH):
        logo = Image.open(LOGO_PATH).convert("RGBA").resize((60,60))
        card.paste(logo, (520, 20), logo)

    draw.text((30, 30), f"Wallet: {address}", fill=(255,255,255), font=font_large)
    draw.text((30, 90), f"Balance: {balance} PANCA", fill=(255,255,255), font=font_large)
    draw.text((30, 150), f"Referral: {referral_code}", fill=(255,255,255), font=font_small)

    qr = qrcode.QRCode(box_size=3, border=1)
    qr.add_data(address)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    qr_img = qr_img.resize((120,120))
    card.paste(qr_img, (30,180))

    out_path = f"/tmp/{address}.png"
    card.save(out_path)
    return out_path
