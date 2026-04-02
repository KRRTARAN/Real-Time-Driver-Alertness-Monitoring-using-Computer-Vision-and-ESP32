import cv2
import mediapipe as mp
import numpy as np
import serial
import time
from collections import deque

# 🔌 SERIAL
try:
    ser = serial.Serial('COM6', 9600)
    time.sleep(2)
    print("✅ ESP32 Connected")
except:
    print("⚠️ ESP32 not connected")
    ser = None

# 🎥 CAMERA INIT
def init_camera():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
    cap.set(cv2.CAP_PROP_FPS, 30)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    time.sleep(2)

    if not cap.isOpened():
        print("❌ Camera failed")
        exit()

    print("✅ Camera initialized")
    return cap

cap = init_camera()

# 🎯 MEDIAPIPE (IMPROVED SETTINGS)
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    refine_landmarks=True,
    max_num_faces=1,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
)

# 👁️ EYE INDEX
LEFT_EYE = [33,160,158,133,153,144]
RIGHT_EYE = [362,385,387,263,373,380]

def ear_calc(eye):
    A = np.linalg.norm(eye[1]-eye[5])
    B = np.linalg.norm(eye[2]-eye[4])
    C = np.linalg.norm(eye[0]-eye[3])
    return (A+B)/(2*C)

EAR_THRESHOLD = 0.25
counter = 0

# 🔥 SMOOTHING BUFFERS
yaw_buffer = deque(maxlen=5)
pitch_buffer = deque(maxlen=5)

# 🔥 CALIBRATION BUFFER
calibration_frames = 20
cal_pitch_list = []
cal_yaw_list = []

baseline_pitch = None
baseline_yaw = None

print("👉 Sit straight for 2 seconds for calibration")

# 🔁 LOOP
while True:
    ret, frame = cap.read()

    # AUTO RECOVERY
    if not ret or frame is None or frame.mean() < 20:
        print("⚠️ Camera resetting...")
        cap.release()
        time.sleep(1)
        cap = init_camera()
        continue

    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = face_mesh.process(rgb)

    status = "NORMAL"

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:

            # 👁️ EAR
            left_eye = [(int(face_landmarks.landmark[i].x*w),
                         int(face_landmarks.landmark[i].y*h)) for i in LEFT_EYE]

            right_eye = [(int(face_landmarks.landmark[i].x*w),
                          int(face_landmarks.landmark[i].y*h)) for i in RIGHT_EYE]

            ear = (ear_calc(np.array(left_eye)) +
                   ear_calc(np.array(right_eye))) / 2

            cv2.putText(frame, f"EAR:{ear:.2f}", (300,30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0),2)

            if ear < EAR_THRESHOLD:
                counter += 1
                if counter > 15:
                    status = "DROWSY"
            else:
                counter = 0

            # 🧭 HEAD POSE
            nose = face_landmarks.landmark[1]
            le = face_landmarks.landmark[33]
            re = face_landmarks.landmark[263]
            chin = face_landmarks.landmark[199]

            nose = np.array([nose.x*w, nose.y*h])
            le = np.array([le.x*w, le.y*h])
            re = np.array([re.x*w, re.y*h])
            chin = np.array([chin.x*w, chin.y*h])

            fw = np.linalg.norm(re-le)
            if fw == 0: fw = 1

            yaw = ((le[0]+re[0])/2 - nose[0]) / fw
            pitch = (nose[1] - chin[1]) / fw

            # 🔥 SMOOTHING
            yaw_buffer.append(yaw)
            pitch_buffer.append(pitch)

            smooth_yaw = np.mean(yaw_buffer)
            smooth_pitch = np.mean(pitch_buffer)

            # 🔥 CALIBRATION (FIRST FEW FRAMES)
            if baseline_pitch is None:
                cal_pitch_list.append(smooth_pitch)
                cal_yaw_list.append(smooth_yaw)

                if len(cal_pitch_list) >= calibration_frames:
                    baseline_pitch = np.mean(cal_pitch_list)
                    baseline_yaw = np.mean(cal_yaw_list)
                    print("✅ Calibration complete")

            else:
                rel_pitch = smooth_pitch - baseline_pitch
                rel_yaw = smooth_yaw - baseline_yaw

                # 🔥 IMPROVED THRESHOLDS
                if rel_pitch < -0.12:
                    status = "DOWN"
                elif rel_yaw > 0.10:
                    status = "LEFT"
                elif rel_yaw < -0.10:
                    status = "RIGHT"

            cv2.putText(frame, f"HEAD:{status}", (50,150),
                        cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,0,0),2)

    # 🔌 SEND TO ESP32
    if ser:
        ser.write((status + "\n").encode())

    cv2.imshow("Driver System", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('r'):
        baseline_pitch = None
        cal_pitch_list.clear()
        cal_yaw_list.clear()
        print("🔄 Recalibrating...")

    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()

if ser:
    ser.close()