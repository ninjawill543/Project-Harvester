import qrcode
import cv2
import numpy as np
import sys


def image_create (input):
    qr = qrcode.QRCode(version=3, box_size=20, border=1, error_correction=qrcode.constants.ERROR_CORRECT_H)
    data = input

    qr.add_data(data)

    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    img.save("qr_code.png")


def video_create ():
    imgfile = "qr_code.png"
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

    vidwriter = cv2.VideoWriter("qr_code.mp4", cv2.VideoWriter_fourcc(*"mp4v"), fps, video_dim)
    for frame in frames:
        vidwriter.write(frame)
    vidwriter.release()



if __name__ == "__main__":
    image_create(sys.argv[1])
    video_create()

