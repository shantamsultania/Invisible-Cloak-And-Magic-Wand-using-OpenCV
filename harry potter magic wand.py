import cv2
import numpy as np

x, y, k = 200, 200, -1

cap = cv2.VideoCapture(0)

def get_wand(event, x1, y1, flag, param):
    global x, y, k
    if event == cv2.EVENT_LBUTTONDOWN:
        x = x1
        y = y1
        k = 1


cv2.namedWindow("get_wand")
cv2.setMouseCallback("get_wand", get_wand)

while True:
    check, frame = cap.read()
    frame = cv2.flip(frame, 1)
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    cv2.imshow("get_wand", frame)

    if k == 1 or cv2.waitKey(30) == 27:
        cv2.destroyAllWindows()
        break

stp = 0


old_pts = np.array([[x, y]], dtype=np.float32).reshape(-1, 1, 2)

mask = np.zeros_like(frame)

while True:
    _, new_frame = cap.read()
    new_frame = cv2.flip(new_frame, 1)
    new_gray = cv2.cvtColor(new_frame, cv2.COLOR_BGR2GRAY)
    new_pts, status, err = cv2.calcOpticalFlowPyrLK(gray_frame,
                                                    new_gray,
                                                    old_pts,
                                                    None, maxLevel=1,
                                                    criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT,
                                                              15, 0.08))

    for i, j in zip(old_pts, new_pts):
        x, y = j.ravel()
        a, b = i.ravel()
        if cv2.waitKey(2) & 0xff == ord('q'):
            stp = 1

        elif cv2.waitKey(2) & 0xff == ord('w'):
            stp = 0

        elif cv2.waitKey(2) == ord('n'):
            mask = np.zeros_like(new_frame)

        if stp == 0:
            mask = cv2.line(mask, (a, b), (x, y), (0, 0, 255), 6)

        cv2.circle(new_frame, (x, y), 6, (0, 255, 0), -1)

    new_frame = cv2.addWeighted(mask, 0.3, new_frame, 0.7, 0)
    cv2.imshow("OutPut Window", new_frame)
    cv2.imshow("Result Window", mask)

    gray_frame = new_gray.copy()
    old_pts = new_pts.reshape(-1, 1, 2)
    key = cv2.waitKey(1)
    if key == 27:
        break

cv2.destroyAllWindows()
cap.release()
