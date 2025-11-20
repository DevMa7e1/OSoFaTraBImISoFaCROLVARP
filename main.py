import cv2
import mediapipe as mp
import time
from tkinter import *

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
                leye_l = (0, 0)
                leye_u = (0, 0)
                mout_l = (0, 0)
                mout_u = (0, 0)
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
                    if(i == 82):
                        mout_u = (x, y)
                    if(i == 88):
                        mout_l = (x, y)
                    cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)
                dr = abs(reye_u[1] - reye_l[1])+1
                dl = abs(leye_u[1] - leye_l[1])+1
                dm = abs(mout_u[1] - mout_l[1])+1
                print(dl, dr, okpressed)
                t = ""
                if fohfr > 200:
                    if abs(dr-calcl) > call-calcl:
                        t += "L- " 
                    else:
                        t += "LO "
                    if abs(dr-calcr) > calr-calcr:
                        t += "R- "
                    else:
                        t += "RO "
                    if 1/dm > 1/calm :
                        t += "M- "
                    else:
                        t += "MO "
                if(fohfr < 100):
                    te.set(f"Keep both eyes open and mouth closed. Stay in a fixed, comfortable position. Press OK to start. Calibrating for {str(fohfr)}/100 frames... Values: " + str(calr) + " " + str(call) + " " + str(calm))
                    calr = round((calr+dr)/2)
                    call = round((call+dl)/2)
                    calm = round((calm+dm)/2)
                    if okpressed:
                        fohfr += 1
                elif fohfr == 100:
                    tk.bell()
                    okpressed = False
                    calr -= 0
                    call -= 0
                    calm += 2
                    calr = calr
                    call = call
                    calm = calm
                    fohfr += 1
                elif fohfr < 201:
                    te.set(f"Keep both eyes closed. Stay in a fixed, comfortable position. Press OK to start. Calibrating for {str(fohfr)}/201 frames... Values: " + str(calcr) + " " + str(calcl) + " " + str(calom))
                    calcr = round((calr+dr)/2)
                    calcl = round((call+dl)/2)
                    calom = round((calm+dm)/2)
                    if okpressed:
                        fohfr += 1
                elif fohfr == 201:
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
