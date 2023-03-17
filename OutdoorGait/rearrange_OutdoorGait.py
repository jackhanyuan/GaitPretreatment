import os
import shutil
from tqdm import tqdm


def rearrange_dataset_to_casia_test(dataset_path):
    INPUT_PATH = dataset_path

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





