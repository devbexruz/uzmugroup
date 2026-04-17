from cv2 import Mat
import numpy as np
import crop_image
import cv2

# Savol 1: b) Yo'q, bunday usul yo'q.
# Savol 2: a) 1
# Savol 3: b) 2 ta ko'k shar olish
# Savol 4: c) 5
# Savol 5: a) 32145
# Savol 6: c) 30%
# Savol 7: b) 441
# Savol 8: c) 600 so'm
# Savol 9: b) 7.5
# Savol 10: b) 24
# Savol 11: d) Ma'lumot yetarli emas
# Savol 12: a) 39
# Savol 13: a) 6
# Savol 14: d) 12
# Savol 15: b) 10 000 000 000
# Savol 16: b) Yo'q, bu mumkin emas.
# Savol 17: a) 58
# Savol 18: b) Oxirgi odamga olmani savat bilan birga berdingiz.
# Savol 19: a) 2
# Savol 20: c) 15
questions_answers = [
    "B",  # Savol 1
    "A",  # Savol 2
    "B",  # Savol 3
    "C",  # Savol 4
    "A",  # Savol 5
    "C",  # Savol 6
    "B",  # Savol 7
    "C",  # Savol 8
    "B",  # Savol 9
    "B",  # Savol 10
    "D",  # Savol 11
    "A",  # Savol 12
    "A",  # Savol 13
    "D",  # Savol 14
    "B",  # Savol 15
    "B",  # Savol 16
    "A",  # Savol 17
    "B",  # Savol 18
    "A",  # Savol 19
    "C"   # Savol 20
]
def only_cyrcles(image, x=1, y=1):
    image = cv2.resize(image, (30*x, 30*y))
    for x_ in range(30*x):
        for y_ in range(30*y):
            if ((x_%30)-15)**2+((y_%30)-15)**2 >= 100:
                image[y_][x_] = 255
    return image
def restructure_matrix(img, N, M):
    img = cv2.resize(img, (N*30, M*30))
    n=0
    matrix = []
    for X in np.vsplit(img, M):
        n+=1
        cols = []
        for Y in np.hsplit(X, N):
            print(cv2.countNonZero(Y), end="\t")
            if cv2.countNonZero(Y) < 820:
                cols.append(True)
            else:
                cols.append(False)
        matrix.append(cols)
        print("")
    return matrix
def convert_to_abcd(answers):
    """
    answers: [[False, True, False, False], ...] ko'rinishidagi massiv
    return: ["B", "A", "-", ...] ko'rinishida
    """
    options = ["A", "B", "C", "D"]
    result = []

    for row in answers:
        if True in row and row.count(True) == 1:  # agar javob bor bo'lsa
            idx = row.index(True)
            result.append(options[idx])
        else:  # hammasi False bo'lsa
            result.append("-")
    return result

def scan(image: Mat):
    cropped = crop_image.biggest_rect(image, 1000, 1000)
    image = cropped[20:980, 20:980]
    image = cv2.vconcat(
        [
            cv2.resize(image[:,150:490], (100, 250)),
            cv2.resize(image[:,660:964], (100, 250))
        ]
    )
    bigray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Treshold image
    image = cv2.threshold(bigray, 0, 255, cv2.THRESH_OTSU)[1]
    image = only_cyrcles(image, 4, 20)
    # cv2.imshow("Scanned Image 2", image)

    return convert_to_abcd(restructure_matrix(image, 4, 20)), cropped

if __name__ == "__main__":
    img = cv2.imread("/home/bexruz/Documents/local/scan_titul/test_images/titul.jpg")
    result, img = scan(img)
    count = sum(1 for a, b in zip(result, questions_answers) if a == b)
    print(count, 20)
    print("Sizning javoblaringiz:", result)
    cv2.imshow("Scanned Image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
