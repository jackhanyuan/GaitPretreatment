#! /usr/bin/python3
# coding=utf-8

import os
import sys
import cv2
import numpy as np

img_types = ('.bmp', '.dib', '.png', '.jpg', '.jpeg', '.pbm', '.pgm', '.ppm', '.tif', '.tiff')


# Scale the image equally and fill the black border if it is not enough.
def resize_and_padding(img, target_size):
    size = img.shape
    h, w = size[0], size[1]
    target_h, target_w = target_size[1], target_size[0]

    # Determine the size of the zoom
    scale_h, scale_w = float(h / target_h), float(w / target_w)
    scale = max(scale_h, scale_w)
    new_w, new_h = int(w / scale), int(h / scale)

    # One of the edges is the same size as the target after scaling
    resize_img = cv2.resize(img, (new_w, new_h))

    # Number of pixels to be expanded for the top, bottom, left and right borders of the image respectively
    top = int((target_h - new_h) / 2)
    bottom = target_h - new_h - top
    left = int((target_w - new_w) / 2)
    right = target_w - new_w - left

    # padding to target_w * target_h
    pad_img = cv2.copyMakeBorder(resize_img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=[0, 0, 0])

    return pad_img


def imgs2video(imgs_path, output_dir, target_name, target_size, target_fps, save_padding_img=False):
    if imgs_path:
        if not os.path.isdir(imgs_path):
            print("input is not a directory")
            sys.exit(0)

    if target_fps:
        if not target_fps > 0:
            print('fps should be greater than zero')
            sys.exit(0)

    if target_size:
        if not target_size[0] > 0 and target_size[1] > 0:
            print('resolution should be greater than zero')
            sys.exit(0)

    output_path = output_dir if output_dir else os.path.sep.join([imgs_path, "out"])
    os.makedirs(output_path, exist_ok=True)
    target = os.path.sep.join([output_path, target_name if target_name else "out.mp4"])
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    vw = cv2.VideoWriter(target, fourcc, target_fps, target_size)
    images = os.listdir(imgs_path)
    images.sort()
    count = 0
    for frame_name in images:
        if not (frame_name.lower().endswith(img_types)):
            continue

        try:
            # print(image)
            frame_path = os.path.sep.join([imgs_path, frame_name])
            frame = cv2.imdecode(np.fromfile(frame_path, dtype=np.uint8), cv2.IMREAD_COLOR)  # , cv2.IMREAD_UNCHANGED
            pad_frame = resize_and_padding(frame, target_size)
            # print(pad_frame.shape)

            if save_padding_img:
                # Save the scaled and filled image.
                resize_path = os.path.sep.join([output_dir, "resize"]) if output_dir else os.path.sep.join(
                    [imgs_path, "resize"])
                os.makedirs(resize_path, exist_ok=True)
                resize_name = os.path.sep.join([resize_path, "resize_" + frame_name])
                cv2.imencode(os.path.splitext(frame_name)[-1], pad_frame)[1].tofile(resize_name)

            # Write to video.
            vw.write(pad_frame)
            count += 1

        except Exception as exc:
            print(frame, exc)

    vw.release()
    print('\r\nConvert Success! Total ' + str(count) + ' images be combined into the video at: ' + target + '\r\n')


def datasets_ext_video(input_path, output_path):
    # input_path = "OutdoorGait-img/images"
    # output_path = "OutdoorGait-video/videos"

    print(f"Walk to {input_path}")

    id_list = os.listdir(input_path)
    id_list.sort()
    for _id in id_list:
        seq_type = os.listdir(os.path.join(input_path, _id))
        seq_type.sort()
        for _seq_type in seq_type:
            imgs_path = os.path.join(input_path, _id, _seq_type)
            video_output_path = os.path.join(output_path, _id)
            target_name = _id + "_" + _seq_type + ".mp4"
            target_size = [320, 240]
            target_fps = 25
            print(f"{imgs_path=}")
            print(f"{target_name=}, {target_size=}, {target_fps=}")
            imgs2video(imgs_path, video_output_path, target_name, target_size, target_fps)
