import os
import sys
from tqdm import tqdm
from person_ext.rvm.person_ext import person_ext_rvm

WORK_PATH = "."
os.chdir(WORK_PATH)
print("WORK_PATH:", os.getcwd())
sys.path.append(os.path.dirname(__file__))


def person_ext_from_video():
    INPUT_PATH = "CASIA-B-video"
    OUTPUT_PATH = "CASIA-B-video-pkl"

    print(f"Walk to {INPUT_PATH}")

    video_list = os.listdir(INPUT_PATH)
    video_list.sort()
    for video_name in tqdm(video_list):
        try:
            # 001-bg-01-000.avi
            _id, _seq_type_1, _seq_type_2, _view = video_name.split(".")[0].split("-")
            _seq_type = _seq_type_1 + "-" + _seq_type_2
            input_path = os.path.join(INPUT_PATH, video_name)
            silhouette_path = os.path.join(OUTPUT_PATH, _id, _seq_type, _view)
            if not os.path.exists(silhouette_path):
                person_ext_rvm(input_path, silhouette_path, frame_size_threshold=800)
        except ValueError:
            continue


if __name__ == '__main__':
    person_ext_from_video()
