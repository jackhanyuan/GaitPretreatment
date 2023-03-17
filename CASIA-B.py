from CASIA.video_to_silhouette import person_ext_from_video
from CASIA.pretreatment_CASIA import datasets_to_pkl


if __name__ == '__main__':
    video_folder = "CASIA/CASIA-B-video"
    silhouette_folder = "CASIA/CASIA-B-silhouette"
    silhouette_cut_folder = "CASIA/CASIA-B-silhouette-cut"
    pkl_folder = "CASIA/CASIA-B-pkl"
    person_ext_from_video(video_folder, silhouette_folder, frame_resize_threshold=800)
    datasets_to_pkl(silhouette_folder, pkl_folder, silhouette_cut_folder,  img_size=64, clean=True, augment=True, pixel_threshold=800)


