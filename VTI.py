import cv2
import os

def extract_frames_from_videos(video_folder, output_folder, frame_rate):
    video_files = [f for f in os.listdir(video_folder) if f.endswith(('.mp4', '.avi', '.mov', '.mkv', '.MOV'))]

    for video_file in video_files:
        video_path = os.path.join(video_folder, video_file)
        video_name = os.path.splitext(video_file)[0]
        output_video_folder = os.path.join(output_folder, video_name)

        os.makedirs(output_video_folder, exist_ok=True)

        video_cap = cv2.VideoCapture(video_path)
        count = 0
        success, image = video_cap.read()

        while success:
            if count % frame_rate == 0:
                frame_filename = os.path.join(output_video_folder, f"frame_{count}.jpg")
                cv2.imwrite(frame_filename, image)
            success, image = video_cap.read()
            count += 1

        video_cap.release()
        print(f"Extracted frames from {video_file} are saved in {output_video_folder}")

extract_frames_from_videos('./VideoInput', './ImagesOutput', 2)
