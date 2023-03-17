# GaitPretreatment

Robust Pretreatment Strategy for Gait Recognition, view the paper [here](https://ieeexplore.ieee.org/abstract/document/9926541).

## requirements

```sh
pip install -r requirements.txt
```

## CAISA-B

Download URL: [CASIA-B](http://www.cbsr.ia.ac.cn/china/Gait%20Databases%20CH.asp).

- Please adjust the raw video file of the CAISA-B dataset to the following format:

```txt
CASIA-B-video
    001-bg-01-000.avi
    ......
    124-nm-06-180.avi
```

- Extracting silhouettes from CAISA-B-Video using GaitPretreatment. (including RVM, Clean, and Augment)

```sh
python CASIA-B.py
```

## OutdoorGait

Download URL: Outdoor-Gait ([Baidu Yun](https://pan.baidu.com/s/1oW6u9olOZtQTYOW_8wgLow) with extract code (tjw0) OR [Google Drive](https://drive.google.com/drive/folders/1XRWq40G3Zk03YaELywxuVKNodul4TziG?usp=sharing)).

- Please adjust the raw RGB image file of the OutdoorGait dataset to the following format:

```txt
OutdoorGait-img
    images
        001
            scene1_bg_L_090_1
                001.jpg
                ......
            scene1_cl_L_090_1
        002
        ...
```

- Extracting silhouettes from OutdoorGait-img using GaitPretreatment. (including RVM, Clean, and Augment)

```sh
python OutdoorGait.py
```

## Parameters

`img_size`: Image resizing size. Default **64**.

`clean`:  Clean up the unqualified silhouettes using a silhouette classification model. Default **True**.

`augment`: Flip the cleaned silhouette sequence horizontally for data augmentation. Default **True**.

`frame_resize_threshold`: When using RVM preprocessing, in order to speed up the silhouette extraction, images larger than the width of threshold pixels will be scaled to threshold pixels. Default **800** pixels.

`pixel_threshold`: The threshold for finding the upper and lower boundaries of a person when cutting images. (the sum of row pixels is greater than or equal to the threshold pixel). Default **800** pixels.

## Acknowledgement

- [RobustVideoMatting](https://github.com/PeterL1n/RobustVideoMatting)
- [CAISA-B](http://www.cbsr.ia.ac.cn/china/Gait%20Databases%20CH.asp)
- [GaitNet](https://github.com/developfeng/GaitNet)
- [classification-pytorch](https://github.com/bubbliiiing/classification-pytorch)

## Citation

```
@inproceedings{han2022gaitpretreatment,
  title={GaitPretreatment: Robust Pretreatment Strategy for Gait Recognition},
  author={Han, Yuanyuan and Wang, Zhong and Han, Xin and Fan, Xiaoya},
  booktitle={2022 International Conference on Communications, Computing, Cybersecurity, and Informatics (CCCI)},
  pages={1-6},
  year={2022},
  organization={IEEE}
}
```

**Note:**
GaitPretreatment is only used for **academic purposes**.
