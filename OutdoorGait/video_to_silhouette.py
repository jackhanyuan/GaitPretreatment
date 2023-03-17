import os
from model.person_ext.rvm.person_ext import person_ext_rvm


def person_ext_from_video(input_video_folder, output_silhouette_folder, frame_resize_threshold=800):
    # input_video_folder = "OutdoorGait-video/videos"
    # output_silhouette_folder = "OutdoorGait-silhouette"

    print(f"Walk to {input_video_folder}")

    id_list = os.listdir(input_video_folder)
    id_list.sort()
    for _id in id_list:
        video_list = os.listdir(os.path.join(input_video_folder, _id))
        video_list.sort()
        for video_name in video_list:
            print(f"\t {video_name}")
            try:
                # 001_scene1_bg_L_090_1.mp4
                split_name = video_name.split(".")[0].split("_")
                _id, _seq_type = split_name[0], "_".join(split_name[1:])
                input_path = os.path.join(input_video_folder, _id, video_name)
                silhouette_path = os.path.join(output_silhouette_folder, _id, _seq_type)
                if not os.path.exists(silhouette_path):
                    person_ext_rvm(input_path, silhouette_path, frame_resize_threshold=frame_resize_threshold)
            except ValueError:
                continue
