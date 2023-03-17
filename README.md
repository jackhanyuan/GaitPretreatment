# GaitPretreatment

Robust Pretreatment Strategy for Gait Recognition, view the paper [here](https://ieeexplore.ieee.org/abstract/document/9926541).

## CAISA-B

Download URL: [CASIA-B](http://www.cbsr.ia.ac.cn/china/Gait%20Databases%20CH.asp).

- Please adjust the raw video file of the CAISA-B dataset to the following format:

```
CASIA-B-video
    001-bg-01-000.avi
    ......
    124-nm-06-180.avi
```

- Silhouette extraction from CAISA-B-Video.

```sh
python CASIA-B.py
```

## OutdoorGait

Download URL: Outdoor-Gait ([Baidu Yun](https://pan.baidu.com/s/1oW6u9olOZtQTYOW_8wgLow) with extract code (tjw0) OR [Google Drive](https://drive.google.com/drive/folders/1XRWq40G3Zk03YaELywxuVKNodul4TziG?usp=sharing)).

- Extracting video from OutdoorGait dataset.

```sh
python frame_to_video.py
```

- Silhouette extraction from OutdoorGait-Video.

```sh
python video_to_silhouette.py
```

- Clean and Augment.

```sh
python pretreatment_OutdoorGait.py
```

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
