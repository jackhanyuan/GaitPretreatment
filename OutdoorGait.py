#! /usr/bin/python3
# coding=utf-8
import os
import sys

WORK_PATH = "."
sys.path.append(WORK_PATH)
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

from OutdoorGait.frame_to_video import datasets_ext_video
from OutdoorGait.video_to_silhouette import person_ext_from_video
from OutdoorGait.pretreatment_OutdoorGait import datasets_to_pkl
from OutdoorGait.rearrange_OutdoorGait import rearrange_dataset_to_casia_test


if __name__ == '__main__':
    image_folder = "OutdoorGait/OutdoorGait-img/images"
    video_folder = "OutdoorGait/OutdoorGait-video/videos"
    silhouette_folder = "OutdoorGait/OutdoorGait-silhouette"
    silhouette_cut_folder = "OutdoorGait/OutdoorGait-silhouette-cut"  # or None
    pkl_folder = "OutdoorGait/OutdoorGait-pkl"

    datasets_ext_video(image_folder, video_folder)
    person_ext_from_video(video_folder, silhouette_folder, frame_resize_threshold=800)
    datasets_to_pkl(silhouette_folder, pkl_folder, silhouette_cut_folder,  img_size=64, clean=True, augment=True, pixel_threshold=800)
    rearrange_dataset_to_casia_test(pkl_folder)
