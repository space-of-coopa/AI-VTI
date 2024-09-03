import cv2
import os

def extract_frames_from_videos(video_folder, output_folder, frame_rate):
    # 비디오 파일 리스트 생성
    video_files = [f for f in os.listdir(video_folder) if f.endswith(('.mp4', '.avi', '.mov', '.mkv', '.MOV'))]

    for video_file in video_files:
        video_path = os.path.join(video_folder, video_file)
        video_name = os.path.splitext(video_file)[0]
        output_video_folder = os.path.join(output_folder, video_name)

        os.makedirs(output_video_folder, exist_ok=True)

        video_cap = cv2.VideoCapture(video_path)

        total_frames = int(video_cap.get(cv2.CAP_PROP_FRAME_COUNT))

        count = 0

        while count < total_frames:
            video_cap.set(cv2.CAP_PROP_POS_FRAMES, count)
            success, image = video_cap.read()

            if not success:
                break

            frame_filename = os.path.join(output_video_folder, f"frame_{count}.jpg")
            cv2.imwrite(frame_filename, image)
            print(f"Saved frame {count} from {video_file}")

            count += frame_rate

        video_cap.release()
        print(f"Extracted frames from {video_file} are saved in {output_video_folder}")

extract_frames_from_videos('./VideoInput', './ImagesOutput', 60)
