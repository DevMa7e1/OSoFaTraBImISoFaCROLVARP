import cv2
import mediapipe as mp
import time

MODEL_PATH = "face_landmarker.task"

BaseOptions = mp.tasks.BaseOptions
FaceLandmarker = mp.tasks.vision.FaceLandmarker
FaceLandmarkerOptions = mp.tasks.vision.FaceLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

options = FaceLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=MODEL_PATH),
    running_mode=VisionRunningMode.VIDEO,
    num_faces=1
)

def main():
    cap = cv2.VideoCapture(0)
    with FaceLandmarker.create_from_options(options) as landmarker:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            ts_ms = int(time.time() * 1000)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)

            result = landmarker.detect_for_video(mp_image, ts_ms)

            if result.face_landmarks:
                landmarks = result.face_landmarks[0]   # flat list of NormalizedLandmark
                i = 0
                reye_l = (0, 0)
                reye_u = (0, 0)
                leye_l = (0, 0)
                leye_u = (0, 0)
                for p in landmarks:
                    i += 1
                    x = int(p.x * frame.shape[1])
                    y = int(p.y * frame.shape[0])
                    if(i == 161):
                        reye_u = (x, y)
                    if(i == 146):
                        leye_l = (x, y)
                    if(i == 387):
                        leye_u = (x, y)
                    if(i == 374):
                        reye_l = (x, y)
                    cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)
                dr = abs(reye_u[1] - reye_l[1])+1
                dl = abs(leye_u[1] - leye_l[1])+1
                print(dl, dr)
                if 1/dl > 1/10:
                    print("L-", end=" ")
                else:
                    print("LO", end=" ")
                if 1/dr > 1/20:
                    print("R-", end=" ")
                else:
                    print("RO", end=" ")
                print()
                
            cv2.imshow("Face Landmarks", frame)
            if cv2.waitKey(1) & 0xFF == 27:
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
