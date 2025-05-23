# 비디오 프레임 추출 도구
이 도구는 여러 비디오 파일에서 특정 간격의 프레임들을 추출하여 이미지로 저장하는 Python 스크립트입니다. 멀티스레딩과 GPU 가속(가능한 경우)을 활용하여 효율적으로 프레임을 추출합니다.

## 주요 기능

### 비디오 프레임 추출
이 스크립트는 지정된 폴더 내의 모든 비디오 파일(mp4, avi, mov, mkv, MOV 확장자)을 감지하고 각 비디오에서 프레임을 추출합니다. 각 비디오마다 별도의 출력 폴더가 생성되며, 설정한 프레임 간격에 따라 이미지가 저장됩니다. 여러 비디오를 동시에 처리하기 위해 ThreadPoolExecutor를 활용하여 병렬 처리를 구현했습니다.

### GPU 가속 지원
CUDA가 설치된 환경에서는 GPU 가속을 활용하여 이미지 처리 성능을 향상시킬 수 있습니다. 스크립트는 PyTorch를 통해 GPU 가용성을 확인하고, 가능한 경우 이미지 데이터를 GPU로 이동시켜 처리합니다.

### 멀티스레딩 최적화
프레임 추출 과정과 이미지 저장 작업을 멀티스레딩으로 처리하여 I/O 작업의 병목 현상을 최소화합니다. 또한 시스템의 CPU 코어 수에 맞춰 최적화된 작업자 수를 할당하여 효율성을 극대화합니다.

### 설치 요구사항
이 스크립트를 실행하기 위해서는 다음 패키지들이 필요합니다:
```bash

pip install opencv-python numpy torch

```
주요 종속성:

- OpenCV (cv2): 비디오 파일 처리 및 이미지 저장
- NumPy: 배열 처리
- PyTorch: GPU 가속 지원 (선택적)
- ThreadPoolExecutor: 병렬 처리

### 기본 사용법
1. 프로젝트 디렉토리에 VideoInput 폴더를 생성하고 처리할 비디오 파일을 넣습니다.
2. 스크립트를 실행하면 ImagesOutput 폴더에 각 비디오별로 하위 폴더가 생성되고 추출된 프레임이 저장됩니다.

```bash
python video_frame_extractor.py
```

### 설정 변경
기본 설정을 변경하려면 스크립트 하단의 다음 변수들을 수정하세요:
```python
video_folder_path = './VideoInput'      # 입력 비디오가 있는 폴더 경로
output_folder_path = './ImagesOutput'   # 출력 이미지가 저장될 폴더 경로
frame_rate = 2                          # 몇 프레임마다 이미지를 추출할지 결정 (값이 클수록 더 적은 이미지 추출)
```

### 작동 방식
프레임 추출 과정
1. 지정된 폴더에서 비디오 파일 목록을 가져옵니다.
2. 각 비디오 파일마다 별도의 스레드에서 처리를 시작합니다.
3. 비디오 파일을 열고 총 프레임 수를 계산합니다.
4. 설정된 프레임 레이트에 따라 프레임을 추출합니다.
5. GPU 가속이 가능한 경우, 이미지 데이터를 GPU로 이동시켜 처리합니다.
6. 추출된 프레임을 JPG 형식으로 저장합니다.
7. 모든 처리가 완료되면 비디오 캡처 객체를 해제합니다.

### 파일 구조
```text
프로젝트루트/
├── VideoInput/
│   ├── video1.mp4
│   ├── video2.avi
│   └── ...
├── ImagesOutput/
│   ├── video1/
│   │   ├── frame_0.jpg
│   │   ├── frame_2.jpg
│   │   └── ...
│   ├── video2/
│   │   ├── frame_0.jpg
│   │   ├── frame_2.jpg
│   │   └── ...
│   └── ...
└── video_frame_extractor.py
```

## 성능 최적화 및 참고사항
### 성능 향상 팁
- GPU 메모리가 충분하다면 max_workers 값을 증가시켜 더 많은 스레드를 활용할 수 있습니다.
- 대용량 비디오 파일 처리 시 메모리 사용량에 주의하세요.
- 프레임 레이트 값을 조정하여 추출할 이미지 수를 조절할 수 있습니다.

### 제한사항
- 매우 큰 해상도의 비디오 처리 시 GPU 메모리 부족 현상이 발생할 수 있습니다.
- 모든 비디오 코덱을 지원하지 않을 수 있으므로, 지원되지 않는 형식의 경우 먼저 변환이 필요할 수 있습니다.

### 결론
이 스크립트는 대량의 비디오 파일에서 효율적으로 프레임을 추출하는 작업에 적합합니다. 멀티스레딩과 GPU 가속을 활용하여 성능을 최적화했으며, 결과물은 체계적으로 정리된 폴더 구조에 저장됩니다. 필요에 따라 프레임 추출 간격과 처리 방식을 조정하여 다양한 프로젝트에 활용할 수 있습니다.
