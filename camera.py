import cv2

cap = cv2.VideoCapture(0, cv2.CAP_MSMF)

while True:
    ret, frame = cap.read()

    if not ret:
        print("No frame")
        continue

    cv2.imshow("Test", frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()