import cv2
import mediapipe as mp
import time
from tkinter import *
import math

def dist(a, b):
    return math.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

tk = Tk()
tk.title = "Program"
tk.resizable(0,0)

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
okpressed = False
def okcmd():
    global okpressed
    okpressed = True

def main():
    global okpressed, okbt, okcmd
    cap = cv2.VideoCapture(0)
    te = StringVar()
    te.set("")
    text = Label(tk, textvariable=te)
    text.pack()
    okbt = Button(tk, text="OK", command=okcmd)
    okbt.pack()
    fohfr = 0
    calr = 0
    calcr = 0
    call = 0
    calcl = 0
    calm = 0
    calom = 0
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
                reye_1 = (0, 0)
                reye_2 = (0, 0)
                leye_l = (0, 0)
                leye_u = (0, 0)
                leye_1 = (0, 0)
                leye_2 = (0, 0)
                mout_l = (0, 0)
                mout_u = (0, 0)
                mout_1 = (0, 0)
                mout_2 = (0, 0)
                for p in landmarks:
                    i += 1
                    x = int(p.x * frame.shape[1])
                    y = int(p.y * frame.shape[0])
                    if(i == 160):
                        leye_u = (x, y)
                    if(i == 146):
                        leye_l = (x, y)
                    if(i == 387):
                        reye_u = (x, y)
                    if(i == 375):
                        reye_l = (x, y)
                    if(i == 34):
                        leye_1 = (x, y)
                    if(i == 134):
                        leye_2 = (x, y)
                    if(i == 264):
                        reye_1 = (x, y)
                    if(i == 363):
                        reye_2 = (x, y)
                    if(i == 14):
                        mout_u = (x, y)
                    if(i == 15):
                        mout_l = (x, y)
                    cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)
                dr = dist(leye_l, leye_u) / dist(leye_1, leye_2)
                dl = dist(reye_l, reye_u) / dist(reye_1, reye_2)
                dm = abs(mout_l[1]-mout_u[1])
                print(dl, dr, dm)
                t = ""
                if fohfr > 21:
                    if abs(call - dl) > abs(calcl - dl):
                        t += "L- " 
                    else:
                        t += "LO "
                    if abs(calr - dr) > abs(calcr - dr):
                        t += "R- "
                    else:
                        t += "RO "
                    if abs(calm - dm) < 10:
                        t += "M- "
                    else:
                        t += "MO "
                if fohfr < 10:
                  te.set(f"Calibration is required. Stay in a relatively fixed position with your eyes open and your mouth closed. Press OK to start.\nCalibrating for {fohfr}/10 frames.")
                  calr = (calr+dr)/2
                  call = (call+dl)/2
                  calm = (calm+dm)/2
                  if okpressed:
                      fohfr += 1
                elif fohfr == 10:
                    okpressed = False
                    tk.bell()
                    fohfr += 1
                elif fohfr < 21:
                    te.set(f"This is the second step of calibration. Stay in a relatively fixed position with your eyes closed. Press OK to continue.\nCalibrating for {fohfr-1}/20 frames.")
                    calcr = (calr+dr)/2
                    calcl = (call+dl)/2
                    if okpressed:
                      fohfr += 1
                elif fohfr == 21:
                    okbt.destroy()
                    okpressed = False
                    tk.bell()
                    fohfr += 1
                else:
                    te.set(t + f" L: {call},{calcl} R: {calr},{calcr} M: {calm}")
            cv2.imshow("Face Landmarks", frame)
            if cv2.waitKey(1) & 0xFF == 27:
                break
            tk.update_idletasks()
            tk.update()

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
