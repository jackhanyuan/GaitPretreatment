import os
import shutil
import random
import argparse
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument('--dataset_path', default='OutdoorGait-video-clean-augment-pkl', type=str, help='Rearrange OutdoorGait datasets to probe.')

opt = parser.parse_args()

WORK_PATH = "."
os.chdir(WORK_PATH)
print("WORK_PATH:", os.getcwd())


def rearrange_dataset_to_hid_test():
    INPUT_PATH = opt.dataset_path

    print(f"Walk to {INPUT_PATH}")

    id_list = os.listdir(INPUT_PATH)
    id_list.sort()
    for _id in tqdm(id_list):
        if _id == "probe" or int(_id) < 70:
            continue
        seq_type = os.listdir(os.path.join(INPUT_PATH, _id))
        seq_type.sort()
        length = len(seq_type)

        probe_seq_type = random.sample(seq_type, int(0.65 * length))

        for _seq_type in probe_seq_type:
            src_path = os.path.join(INPUT_PATH, _id, _seq_type)
            dst_path = os.path.join(INPUT_PATH, "probe", _id, _seq_type)

            default_path = os.path.join(src_path, "default")
            pkl_path = os.path.join(src_path, "default", _id + '_' + _seq_type + ".pkl")

            dst_pkl_path = os.path.join(src_path, _id + '_' + _seq_type + ".pkl")

            if os.path.exists(pkl_path):
                shutil.move(pkl_path, dst_pkl_path)
                os.rmdir(default_path)
                shutil.move(src_path, dst_path)


def rearrange_dataset_to_casia_test():
    INPUT_PATH = opt.dataset_path

    print(f"Walk to {INPUT_PATH}")

    id_list = os.listdir(INPUT_PATH)
    id_list.sort()
    for _id in tqdm(id_list):
        if int(_id) < 0:
            continue
        seq_type = os.listdir(os.path.join(INPUT_PATH, _id))
        seq_type.sort()

        for _seq_type in seq_type:
            src_path = os.path.join(INPUT_PATH, _id, _seq_type)
            _seq_type_split = _seq_type.split("_")
            _seq_type_split_type = {"scene1": "-01", "scene2": "-02", "scene3": "-03"}
            dst_path = os.path.join(INPUT_PATH, _id, _seq_type_split[1] + _seq_type_split_type[_seq_type_split[0]])
            os.makedirs(dst_path, exist_ok=True)
            
            default_path = os.path.join(src_path, "default")
            pkl_path = os.path.join(src_path, "default", _id + '_' + _seq_type + ".pkl")
            dst_pkl_path = os.path.join(src_path, _id + '_' + _seq_type + ".pkl")

            if os.path.exists(pkl_path):
                shutil.move(pkl_path, dst_pkl_path)
                os.rmdir(default_path)
                shutil.move(src_path, dst_path)


def rm_default_folder():
    INPUT_PATH = opt.dataset_path

    print(f"Walk to {INPUT_PATH}")

    id_list = os.listdir(INPUT_PATH)
    id_list.sort()
    for _id in tqdm(id_list):
        if int(_id) < 0:
            continue
        seq_type = os.listdir(os.path.join(INPUT_PATH, _id))
        seq_type.sort()

        for _seq_type in seq_type:
            view = os.listdir(os.path.join(INPUT_PATH, _id, _seq_type))
            view.sort()
            for _view in view:
                default_path = os.path.join(INPUT_PATH, _id, _seq_type, _view, 'default')
                src_path = os.path.join(INPUT_PATH, _id, _seq_type, _view, 'default', _id + '_' + _view + ".pkl")
                dst_path = os.path.join(INPUT_PATH, _id, _seq_type, _view)

                if os.path.exists(src_path):
                    shutil.move(src_path, dst_path)
                    os.rmdir(default_path)
                    
                    
def rename_view_folder():
    INPUT_PATH = opt.dataset_path

    print(f"Walk to {INPUT_PATH}")

    id_list = os.listdir(INPUT_PATH)
    id_list.sort()
    for _id in tqdm(id_list):
        if int(_id) < 0:
            continue
        seq_type = os.listdir(os.path.join(INPUT_PATH, _id))
        seq_type.sort()

        for _seq_type in seq_type:
            view = os.listdir(os.path.join(INPUT_PATH, _id, _seq_type))
            view.sort()
            for _view in view:
                src_path = os.path.join(INPUT_PATH, _id, _seq_type, _view)
                dst_path = os.path.join(INPUT_PATH, _id, _seq_type, _view.split("_")[-1])

                if os.path.exists(src_path):
                    os.rename(src_path, dst_path)


if __name__ == '__main__':
    # rearrange_dataset_to_hid_test()
    rearrange_dataset_to_casia_test()
    # rm_default_folder()
    # rename_view_folder()






