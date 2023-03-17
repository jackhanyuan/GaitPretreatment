#! /usr/bin/python3
# coding=utf-8

import os
from model.person_ext.rvm.person_ext import person_ext_rvm


def person_ext_from_video(input_video_folder, output_silhouette_folder, frame_resize_threshold=800):
    print()
    print(f"Walk to {input_video_folder}")

    video_list = os.listdir(input_video_folder)
    video_list.sort()
    for video_name in video_list:
        try:
            # 001-bg-01-000.avi
            _id, _seq_type_1, _seq_type_2, _view = video_name.split(".")[0].split("-")
            _seq_type = _seq_type_1 + "-" + _seq_type_2
            input_path = os.path.join(input_video_folder, video_name)
            silhouette_path = os.path.join(output_silhouette_folder, _id, _seq_type, _view)
            if not os.path.exists(silhouette_path):
                person_ext_rvm(input_path, silhouette_path, frame_resize_threshold=frame_resize_threshold)
        except ValueError:
            continue


if __name__ == '__main__':
    person_ext_from_video("CASIA-B-video", "CASIA-B-silhouette")
