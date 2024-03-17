import qrcode

qr = qrcode.QRCode(version=3, box_size=20, border=1, error_correction=qrcode.constants.ERROR_CORRECT_H)
data = "ls -al"

qr.add_data(data)

qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")

img.save("qr_code.png")