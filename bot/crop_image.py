import cv2
import numpy as np

def by_points(image, points, w, h):
    """
    points: to'rtburchakning 4 nuqtasi (np.array, tartib: chap-yuqori, o'ng-yuqori, past-o'ng, past-chap)
    w, h: chiqadigan crop o'lchami
    """
    # chiqadigan to'rtburchak koordinatalari
    dst_points = np.array([[0, 0], [w-1, 0], [w-1, h-1], [0, h-1]], dtype="float32")
    
    # perspektiva transform
    M = cv2.getPerspectiveTransform(points, dst_points)
    crop = cv2.warpPerspective(image, M, (w, h))
    return crop


def biggest_rect(image, w, h):
    """
    Eng katta to'rtburchakni topadi va crop_by_points orqali crop qaytaradi
    """
    # kulrang va threshold
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    edged = cv2.Canny(blur, 50, 200)

    # konturlarni topish
    contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    biggest = None
    max_area = 0

    for cnt in contours:
        peri = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)

        if len(approx) == 4:  # to'rtburchak bo‘lsa
            area = cv2.contourArea(approx)
            if area > max_area:
                biggest = approx
                max_area = area

    if biggest is None:
        return None  # agar to'rtburchak topilmasa

    # 4 nuqtani tartibga solish (yuqori-chap, yuqori-o‘ng, past-o‘ng, past-chap)
    pts = biggest.reshape(4, 2).astype("float32")
    rect = order_points(pts)

    # crop qilish
    return by_points(image, rect, w, h)


def order_points(pts):
    """
    4 nuqtani tartiblab beradi: yuqori-chap, yuqori-o'ng, past-o'ng, past-chap
    """
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]  # top-left
    rect[2] = pts[np.argmax(s)]  # bottom-right

    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]  # top-right
    rect[3] = pts[np.argmax(diff)]  # bottom-left
    return rect
