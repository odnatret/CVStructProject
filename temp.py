import cv2
import numpy as np

file = "test.mp4"
target_color = None
color_tolerance = 20

#Захват мыши
def pick_color(event, x, y, flags, param):
    global target_color
    if event == cv2.EVENT_LBUTTONDOWN:
        #Для HSV
        target_color = cv2.cvtColor(np.uint8([[frame[y, x]]]), cv2.COLOR_BGR2HSV)[0][0]
        print(f"Выбранный цвет в HSV: {target_color}")

        #Для BGR
        #target_color = frame[y, x].copy()
        #print(f"Выбранный цвет: {target_color}")

def on_trackbar(val):
    pass

cv2.namedWindow("Frame")
cv2.moveWindow("Frame", 100, 100)

cv2.namedWindow("Mask", cv2.WINDOW_NORMAL)
cv2.moveWindow("Mask", 100 + 640 + 20, 100)

cv2.namedWindow("Frame")
cv2.setMouseCallback("Frame", pick_color)
cv2.createTrackbar("Tolerance", "Frame", color_tolerance, 100, on_trackbar)

#Захват видео
cap = cv2.VideoCapture(file) 
#cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    color_tolerance = cv2.getTrackbarPos("Tolerance", "Frame")
    if target_color is not None:
        #BGR в HSV
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        #Для HSV
        lower_bound = np.array([max(0, target_color[0] - color_tolerance//2),
                                max(0, target_color[1] - color_tolerance),
                                max(0, target_color[2] - color_tolerance)])
        upper_bound = np.array([min(179, target_color[0] + color_tolerance//2),
                                min(255, target_color[1] + color_tolerance),
                                min(255, target_color[2] + color_tolerance)])
        #Для HSV

        #Для BGR

        # lower_bound = np.array([max(0, target_color[0] - color_tolerance),
        #                         max(0, target_color[1] - color_tolerance),
        #                         max(0, target_color[2] - color_tolerance)])
        # upper_bound = np.array([min(255, target_color[0] + color_tolerance),
        #                         min(255, target_color[1] + color_tolerance),
        #                         min(255, target_color[2] + color_tolerance)])

        #mask = cv2.inRange(frame, lower_bound, upper_bound)
        #Для BGR

        #Для HSV
        mask = cv2.inRange(hsv_frame, lower_bound, upper_bound)
        kernel = np.ones((5,5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        #Для HSV

        for contour in contours:
            if cv2.contourArea(contour) > 100:
                cv2.drawContours(frame, [contour], -1, (0, 255, 0), 2)
        
    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", mask) if 'mask' in locals() else None

    if cv2.waitKey(33) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()