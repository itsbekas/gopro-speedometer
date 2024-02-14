import cv2
import numpy as np
from speed_gauge import create_speed_gauge, create_needle, create_mask, rotate_needle

def video_title_to_overlay(title, category):
    return "output/{}.{}.mp4".format(title.split(".")[0], category)


img_size = 1024

def create_video(video_config):

    width = img_size
    height = img_size
    fps = video_config["fps"]
    duration = int(video_config["duration"])
    total_frames = duration * fps
    sample_rate = 10 # Hz
    sample_duration = int(fps / sample_rate) # frames

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    output_title = video_title_to_overlay(video_config["title"], "speed")
    out = cv2.VideoWriter(output_title, fourcc, fps, (width, height))

    return out


def create_base_frame():

    width = img_size
    height = img_size
    blue_color = (200, 150, 110) # BGR

    black_frame = np.zeros((height, width, 3), dtype=np.uint8)
    blue_frame = np.full((height, width, 3), blue_color, dtype=np.uint8)

    gauge = create_speed_gauge()
    gauge_mask = create_mask(gauge)
    filtered_gauge = cv2.bitwise_and(gauge, gauge, mask=gauge_mask)

    return black_frame.copy() + filtered_gauge


def create_masked_needle():
    needle = create_needle()
    needle_mask = create_mask(needle)
    return cv2.bitwise_and(needle, needle, mask=needle_mask)


def generate_overlay(metadata):

    video_config = metadata["video_config"]
    gps_data = metadata["gps_data"]

    # placeholder data
    duration = video_config["duration"]
    fps = video_config["fps"]
    sample_rate = 10 # Hz
    real_frames = int(duration * fps)
    sample_size = len(gps_data["speed"])
    total_frames = int(sample_size * (fps / sample_rate) - (fps / sample_rate)) # nr of samples * frames per sample

    out = create_video(video_config)

    base_frame = create_base_frame()
    needle = create_masked_needle()
    
    frame_idx = [x for x in range(total_frames)]
    data_idx = np.linspace(0, total_frames, sample_size)
    spd_data = gps_data["speed"]

    interp_spd = np.interp(frame_idx, data_idx, spd_data)

    max_speed = 14 # m/s (50 km/h)

    for i in range(total_frames):

        if i % 250 == 0:
            print(f"Frame {i}/{total_frames}")

        frame = base_frame + rotate_needle(needle, interp_spd[i], max_speed)

        out.write(frame)

    out.release()
