import cv2

cap = cv2.VideoCapture(0, cv2.CAP_MSMF) #If the camera feed is not detected, try different input indices (0, 1, or 2) to identify the correct video source for your system.


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
