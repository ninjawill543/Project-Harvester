import qrcode
import cv2
import numpy as np
import sys
import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import argparse


def encode (input):
    key_hex = b'4326462948404d635166546a576e5a72' #Please change, this is just used for the example!

    data = input
    key = bytes.fromhex(key_hex.decode())
    cipher = AES.new(key, AES.MODE_ECB)

    block_size = 16
    data_padded = data + (block_size - len(data) % block_size) * chr(block_size - len(data) % block_size)

    ciphertext = cipher.encrypt(data_padded.encode())

    encoded_ciphertext = base64.b64encode(ciphertext).decode()

    return(encoded_ciphertext)


def image_create (input):
    qr = qrcode.QRCode(version=3, box_size=20, border=1, error_correction=qrcode.constants.ERROR_CORRECT_H)
    data = input

    qr.add_data(data)

    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    img.save("output/qr_code.png")


def video_create ():
    imgfile = "output/qr_code.png"
    video_dim = (1280, 720)
    fps = 25
    duration = 2.0

    img = cv2.imread(imgfile, cv2.IMREAD_COLOR)
    orig_shape = img.shape[:2]

    side_length = min(orig_shape)

    scale = min(video_dim[0] / orig_shape[1], video_dim[1] / orig_shape[0])

    resized_img = cv2.resize(img, None, fx=scale, fy=scale)

    x_offset = (video_dim[0] - resized_img.shape[1]) // 2
    y_offset = (video_dim[1] - resized_img.shape[0]) // 2

    background = np.ones((video_dim[1], video_dim[0], 3), dtype=np.uint8) * 255

    background[y_offset:y_offset + resized_img.shape[0], x_offset:x_offset + resized_img.shape[1]] = resized_img

    num_frames = int(fps * duration)
    frames = [background] * num_frames

    vidwriter = cv2.VideoWriter("output/qr_code.mp4", cv2.VideoWriter_fourcc(*"mp4v"), fps, video_dim)
    for frame in frames:
        vidwriter.write(frame)
    vidwriter.release()

def remove_image():
    os.remove("output/qr_code.png") 



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert a string to a QR code, that is then converted into a video.")
    parser._action_groups.pop()
    required = parser.add_argument_group('Required arguments')
    optional = parser.add_argument_group('Optional arguments')
    optional.add_argument("--aes", help="Chose aes than cleartext to encrypt message. If chosen, please input your aes hex key on line 12", action="store_true")
    required.add_argument('--string', help="String to convert", required=True)
    args = parser.parse_args()
    if args.aes:
        image_create(encode(args.string))
    else:
        image_create(args.string)
    
    video_create()
    remove_image()

