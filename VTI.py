import cv2
import os
import numpy
import torch
from concurrent.futures import ThreadPoolExecutor

def extract_frames_from_video(video_path, output_video_folder, frame_rate):
    video_cap = cv2.VideoCapture(video_path)
    total_frames = int(video_cap.get(cv2.CAP_PROP_FRAME_COUNT))

    count = 0
    frames = []

    with ThreadPoolExecutor(max_workers=8) as executor:
        while count < total_frames:
            success, image = video_cap.read()
            if not success:
                break

            # GPU로 이미지 데이터를 이동하고 변환하는 예시 (이 작업을 꼭 필요로 하는 경우에만)
            if torch.cuda.is_available():
                tensor_image = torch.from_numpy(image).to('cuda')
                # 이미지 처리 로직 추가 가능 (GPU 상에서)
                image = tensor_image.cpu().numpy()  # CPU로 다시 이동 (저장할 때만)

            future = executor.submit(save_frame, image, output_video_folder, count)
            frames.append(future)

            count += frame_rate

    video_cap.release()

def save_frame(image, output_video_folder, count):
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

    with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
        for video_file in video_files:
            executor.submit(process_video, video_file, video_folder, output_folder, frame_rate)

if __name__ == '__main__':
    video_folder_path = './VideoInput'
    output_folder_path = './ImagesOutput'
    frame_rate = 2

    extract_frames_from_videos(video_folder_path, output_folder_path, frame_rate)
