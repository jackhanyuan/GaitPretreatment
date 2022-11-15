import os
import sys
from tqdm import tqdm
from person_ext.rvm.person_ext import person_ext_rvm

WORK_PATH = "."
os.chdir(WORK_PATH)
print("WORK_PATH:", os.getcwd())
sys.path.append(os.path.dirname(__file__))


def person_ext_from_video():
    INPUT_PATH = "OutdoorGait-video"
    OUTPUT_PATH = "OutdoorGait-video-split"

    print(f"Walk to {INPUT_PATH}")

    id_list = os.listdir(INPUT_PATH)
    id_list.sort()
    for _id in tqdm(id_list):
        video_list = os.listdir(os.path.join(INPUT_PATH, _id))
        video_list.sort()
        for video_name in video_list:
            print(f"\t {video_name}")
            try:
                # 001_scene1_bg_L_090_1.mp4
                split_name = video_name.split(".")[0].split("_")
                _id, _seq_type = split_name[0], "_".join(split_name[1:])
                input_path = os.path.join(INPUT_PATH, _id, video_name)
                silhouette_path = os.path.join(OUTPUT_PATH, _id, _seq_type)
                if not os.path.exists(silhouette_path):
                    person_ext_rvm(input_path, silhouette_path, frame_size_threshold=800)
            except ValueError:
                continue


if __name__ == '__main__':
    person_ext_from_video()
