#! /usr/bin/python3
# coding=utf-8

import os
import sys
WORK_PATH = "."
os.chdir(WORK_PATH)
print("WORK_PATH:", os.getcwd())
sys.path.append(WORK_PATH)

import cv2
import time
import numpy as np
import argparse
import pickle
from PIL import Image
from model.people_cls.classification import Classification

classfication = Classification()
parser = argparse.ArgumentParser(description='Pretreatment')
parser.add_argument('--img_size', default=64, type=int, help='Image resizing size. Default 64')
parser.add_argument('--augment', default=True, type=bool, help='Image Horizontal Flip Augmented Dataset.')
parser.add_argument('--clean', default=True, type=bool, help='Use RVM to clean up non-compliant silhouettes.')
opt = parser.parse_args()


def clean(img):
    if opt.clean:
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        class_name, probability = classfication.detect_image(img)
        if class_name == 'people' and probability > 0.5:
            return True
        else:
            return False
    return True


def imgs_to_pickle(_id, _seq_type, INPUT_PATH, OUTPUT_PATH, save_cut_img=False, pixel_threshold=800):
    print(f"\t Walk to {INPUT_PATH}.")
    print(f"\t {save_cut_img=} {pixel_threshold=}")
    silhouette_dir = INPUT_PATH
    out_dir = os.path.join(OUTPUT_PATH, _id, _seq_type, "default")
    all_imgs_pkl = os.path.join(out_dir, '{}.pkl'.format(_id + "_" + _seq_type))
    if os.path.exists(all_imgs_pkl):
        print('\t Exists:', all_imgs_pkl)
        return

    count_frame = 0
    all_imgs, flip_imgs = [], []
    frame_list = sorted(os.listdir(silhouette_dir))
    for frame_name in frame_list:
        if frame_name.lower().endswith(('png', 'jpg')):  # filter png files
            frame_path = os.path.join(silhouette_dir, frame_name)

            img = cv2.imread(frame_path, cv2.IMREAD_GRAYSCALE)
            img = cut_img(img, 128, frame_name, pixel_threshold)  # cut img_size is 128, for later clean() function to determine
            img_copy = img

            if img is None:
                print('\t RM:', frame_name)
                os.remove(frame_path)
                continue
            if clean(img):
                # resize
                ratio = img.shape[1] / img.shape[0]
                img = cv2.resize(img, (int(opt.img_size * ratio), opt.img_size), interpolation=cv2.INTER_CUBIC)

                # Save the img
                all_imgs.append(img)
                count_frame += 1

                if save_cut_img:
                    cut_img_path = os.path.sep.join(['people', 'true', "{0:.8f}-".format(time.perf_counter()) + frame_name])
                    cv2.imwrite(cut_img_path, img_copy)

                if opt.augment:
                    flip_img = cv2.flip(img, 1)  # Flip horizontally to expand data
                    flip_imgs.append(flip_img)
                    print('\t augment:', frame_path)

            else:
                print('\t no people:', frame_name)
                # print('\t RM:', frame_name)
                # os.remove(frame_path)
                # cut_img_false_path = os.path.sep.join(['people', 'false', "{0:.8f}-".format(time.perf_counter()) + frame_name])
                # cv2.imwrite(cut_img_false_path, img)

    all_imgs = np.asarray(all_imgs + flip_imgs)

    if count_frame > 0:
        os.makedirs(out_dir, exist_ok=True)
        pickle.dump(all_imgs, open(all_imgs_pkl, 'wb'))
        print(f"\t pkl save path: {all_imgs_pkl}")

    # Warn if the sequence contains less than 5 frames
    if count_frame < 5:
        print('\t Seq:{}, less than 5 valid data.'.format(_id))

    return count_frame


def cut_img(img, img_size, frame_name, pixel_threshold=0):
    # A silhouette contains too little white pixels
    # might be not valid for identification.
    if img is None or img.sum() <= 10000:
        print(f'\t {frame_name} has no data.')
        return None

    # Get the top and bottom point
    y = img.sum(axis=1)
    y_top = (y > pixel_threshold).argmax(axis=0)  # the line pixels more than pixel_threshold, it will be counted
    y_btm = (y > pixel_threshold).cumsum(axis=0).argmax(axis=0)
    img = img[y_top:y_btm + 1, :]

    # As the height of a person is larger than the width,
    # use the height to calculate resize ratio.
    ratio = img.shape[1] / img.shape[0]
    img = cv2.resize(img, (int(img_size * ratio), img_size), interpolation=cv2.INTER_CUBIC)

    # Get the median of x axis and regard it as the x center of the person.
    sum_point = img.sum()
    sum_column = img.sum(axis=0).cumsum()
    x_center = -1
    for i in range(sum_column.size):
        if sum_column[i] > sum_point / 2:
            x_center = i
            break
    if x_center < 0:
        print(f'\t{frame_name} has no center.')
        return None

    # Get the left and right points
    half_width = img_size // 2
    left = x_center - half_width
    right = x_center + half_width
    if left <= 0 or right >= img.shape[1]:
        left += half_width
        right += half_width
        _ = np.zeros((img.shape[0], half_width))
        img = np.concatenate([_, img, _], axis=1)
    img = img[:, left:right].astype('uint8')
    return img


def datasets_to_pkl(input_path, output_path):
    print(f"Walk to {input_path}.")
    id_list = os.listdir(input_path)
    id_list.sort()
    for _id in id_list:
        seq_type = os.listdir(os.path.join(input_path, _id))
        seq_type.sort()
        for _seq_type in seq_type[::1]:
            INPUT_PATH = os.path.join(input_path, _id, _seq_type)
            imgs_to_pickle(_id, _seq_type, INPUT_PATH, output_path)


if __name__ == '__main__':
    input_path = "OutdoorGait-video-split"
    output_path = "OutdoorGait-video-clean-augment-pkl"
    datasets_to_pkl(input_path, output_path)
