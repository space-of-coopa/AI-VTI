import cv2
import os
import numpy as np
from multiprocessing import Pool, cpu_count

def extract_frames_from_video(video_path, output_video_folder, frame_rate):
    video_cap = cv2.VideoCapture(video_path)
    total_frames = int(video_cap.get(cv2.CAP_PROP_FRAME_COUNT))

    count = 0
    frames = []

    while count < total_frames:
        success, image = video_cap.read()
        if not success:
            break

        # 프레임 저장 (배치로 저장할 수 있도록 메모리에 모음)
        frames.append((count, image))

        if len(frames) >= 10:  # 예: 배치 크기가 10인 경우
            save_frames_batch(frames, output_video_folder)
            frames.clear()

        count += frame_rate  # 다음 프레임으로 이동

    # 남은 프레임 저장
    if frames:
        save_frames_batch(frames, output_video_folder)

    video_cap.release()

def save_frames_batch(frames, output_video_folder):
    """배치로 프레임을 저장하는 함수"""
    for count, image in frames:
        frame_filename = os.path.join(output_video_folder, f"frame_{count}.jpg")
        cv2.imwrite(frame_filename, image)
        print(f"Saved frame {count} to {frame_filename}")

def process_video(video_file, video_folder, output_folder, frame_rate):
    video_path = os.path.join(video_folder, video_file)
    video_name = os.path.splitext(video_file)[0]
    output_video_folder = os.path.join(output_folder, video_name)

    os.makedirs(output_video_folder, exist_ok=True)
    extract_frames_from_video(video_path, output_video_folder, frame_rate)

def extract_frames_from_videos(video_folder, output_folder, frame_rate):
    video_files = [f for f in os.listdir(video_folder) if f.endswith(('.mp4', '.avi', '.mov', '.mkv', '.MOV'))]

    # 병렬 처리
    pool = Pool(processes=cpu_count())
    for video_file in video_files:
        pool.apply_async(process_video, args=(video_file, video_folder, output_folder, frame_rate))

    pool.close()
    pool.join()

if __name__ == '__main__':
    video_folder_path = './VideoInput'
    output_folder_path = './ImagesOutput'
    frame_rate = 2

    extract_frames_from_videos(video_folder_path, output_folder_path, frame_rate)
