#! /usr/bin/python3
# coding=utf-8

import os
import cv2
import numpy as np
import pickle
from PIL import Image
from model.person_cls.classification import Classification

classfication = Classification()


def clean_img(img, clean):
    if clean:
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        class_name, probability = classfication.detect_image(img)
        if class_name == 'people' and probability > 0.5:
            return True
        else:
            return False
    return True


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


def imgs_to_pickle(_id, _seq_type, silhouette_path, pkl_path, silhouette_cut_path=None, img_size=64, clean=True, augment=True, pixel_threshold=0):
    print()
    print(f"\t Walk to {silhouette_path}.")
    print(f"\t {img_size=} {clean=} {augment=} {pixel_threshold=}")

    all_imgs_pkl = os.path.join(pkl_path, '{}.pkl'.format(_id + "_" + _seq_type))
    if os.path.exists(all_imgs_pkl):
        print('\t Exists:', all_imgs_pkl)
        return
    if silhouette_cut_path:
        os.makedirs(silhouette_cut_path, exist_ok=True)

    count_frame = 0
    all_imgs, flip_imgs = [], []
    frame_list = sorted(os.listdir(silhouette_path))
    for frame_name in frame_list:
        if frame_name.lower().endswith(('png', 'jpg')):  # filter png files
            frame_path = os.path.join(silhouette_path, frame_name)

            img = cv2.imread(frame_path, cv2.IMREAD_GRAYSCALE)
            img = cut_img(img, 128, frame_name, pixel_threshold)  # cut img_size is 128, for later clean() function to determine

            if img is None:
                print('\t RM:', frame_name)
                os.remove(frame_path)
                continue
            if clean_img(img, clean):
                # resize
                ratio = img.shape[1] / img.shape[0]
                img = cv2.resize(img, (int(img_size * ratio), img_size), interpolation=cv2.INTER_CUBIC)

                # Save the img
                all_imgs.append(img)
                count_frame += 1

                if silhouette_cut_path:
                    silhouette_cut_save_path = os.path.join(silhouette_cut_path, frame_name)
                    cv2.imwrite(silhouette_cut_save_path, img)

                if augment:
                    flip_img = cv2.flip(img, 1)  # Flip horizontally to expand data
                    flip_imgs.append(flip_img)
                    # print('\t augment:', frame_path)
                    if silhouette_cut_path:
                        silhouette_cut_aug_save_path = os.path.join(silhouette_cut_path, "aug" + frame_name )
                        cv2.imwrite(silhouette_cut_aug_save_path, flip_img)
            else:
                print('\t no person:', frame_name)
                # print('\t RM:', frame_name)
                # os.remove(frame_path)
                # silhouette_cleaned_path = os.path.sep.join(['cleaned', "{0:.8f}-".format(time.perf_counter()) + frame_name])
                # cv2.imwrite(silhouette_cleaned_path, img)

    all_imgs = np.asarray(all_imgs + flip_imgs)

    if count_frame > 0:
        os.makedirs(pkl_path, exist_ok=True)
        pickle.dump(all_imgs, open(all_imgs_pkl, 'wb'))
        print(f"\t pkl save path: {all_imgs_pkl}")
        print()

    # Warn if the sequence contains less than 5 frames
    if count_frame < 5:
        print('\t Seq:{}, less than 5 valid data.'.format(_id))

    return count_frame


def datasets_to_pkl(silhouette_folder, pkl_folder, silhouette_cut_folder=None, img_size=64, clean=True, augment=True, pixel_threshold=0):
    print()
    print(f"Walk to {silhouette_folder}.")
    id_list = os.listdir(silhouette_folder)
    id_list.sort()
    for _id in id_list:
        seq_type = os.listdir(os.path.join(silhouette_folder, _id))
        seq_type.sort()
        for _seq_type in seq_type[::1]:
            silhouette_path = os.path.join(silhouette_folder, _id, _seq_type)
            pkl_path = os.path.join(pkl_folder, _id, _seq_type, "default")
            silhouette_cut_path = None
            if silhouette_cut_folder:
                silhouette_cut_path = os.path.join(silhouette_cut_folder, _id, _seq_type)
            imgs_to_pickle(_id, _seq_type, silhouette_path, pkl_path, silhouette_cut_path=silhouette_cut_path, img_size=img_size, clean=clean, augment=augment, pixel_threshold=pixel_threshold)
