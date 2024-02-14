from PIL import Image, ImageDraw, ImageFont
import numpy as np
import cv2

pre_size = 8192
img_size = 1024

def create_mask(image):
    mask = cv2.inRange(image, (1, 1, 1), (255, 255, 255))
    return mask


def create_speed_gauge():

    size = pre_size
    big_w = size // 16 + size // 32 # width
    small_w = size // 16 # width
    out_w = size // 32 # outline width

    
    gauge = Image.new('RGB', (size, size), (0, 0, 0))
    draw = ImageDraw.Draw(gauge)

    for i in range(135, 420, 30):
        draw.arc((0, 0, size, size), i-1, i+1, fill=(190, 70, 50), width=big_w)
    
    for i in range(150, 405, 30):
        draw.arc((0, 0, size, size), i-1, i+1, fill=(255, 255, 255), width=small_w)

    draw.arc((0, 0, size, size), 134, 406, fill=(255, 255, 255), width=out_w)

    gauge = gauge.resize((img_size, img_size), resample=Image.LANCZOS)

    gauge_np = np.array(gauge)
    gauge_bgr = cv2.cvtColor(gauge_np, cv2.COLOR_RGB2BGR)

    return gauge_bgr


def create_needle():
    
    size = pre_size
    needle_s = size // 2 # size
    needle_o = size // 32 # offset
    needle_l = size // 2 + size // 4 + size // 8 # length

    needle = Image.new('RGB', (size, size), (0, 0, 0))
    draw = ImageDraw.Draw(needle)

    draw.ellipse(
        (
            needle_s - needle_o,
            needle_s - needle_o,
            needle_s + needle_o,
            needle_s + needle_o
        ), fill=(255, 255, 255)
    )

    draw.polygon(
        [
            (needle_s - needle_o, needle_s),
            (needle_s + needle_o, needle_s),
            (needle_s, needle_l)
        ], fill=(255, 255, 255)
    )

    needle = needle.resize((img_size, img_size), resample=Image.LANCZOS)

    needle_np = np.array(needle)
    needle_bgr = cv2.cvtColor(needle_np, cv2.COLOR_RGB2BGR)

    return needle_bgr

def rotate_needle(needle, speed, max_speed):
    
    speed = speed if speed < max_speed else max_speed
    angle = - (45 + (speed / max_speed) * 270)

    needle_center = (img_size // 2, img_size // 2)
    needle_rotated = cv2.warpAffine(
        needle,
        cv2.getRotationMatrix2D(needle_center, angle, 1.0),
        (img_size, img_size)
    )

    return needle_rotated
