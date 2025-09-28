import cv2
import numpy as np
import re
import sys
import os


drawing = False
point_radius = 5
color = 0
size = 750


def draw_point(event, x, y, flags, img):
    global drawing
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        cv2.circle(img, (x, y), point_radius, color, -1)
    elif event == cv2.EVENT_MOUSEMOVE and drawing:
        cv2.circle(img, (x, y), point_radius, color, -1)
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.circle(img, (x, y), point_radius, color, -1)


def check_filename(name: str) -> str:
    name = name.strip()
    if not name or re.search(r'[<>:"/\\|?*]', name):
        raise ValueError("Недопустимое имя файла")
    return name if name.lower().endswith(".png") else name + ".png"


try:
    filename = check_filename(input(
        "Введите имя PNG файла [default: drawn_raster.png]: "
        ) or "drawn_raster.png")
except ValueError as e:
    print(f"{e}")
    sys.exit(1)

filepath = os.path.join("png", filename)

img = np.ones((size, size), dtype=np.uint8) * 255
cv2.namedWindow("Raster Draw")
cv2.setMouseCallback("Raster Draw", draw_point, img)

print("ЛКМ — рисовать, 's' — сохранить, 'q' — выйти")

while True:
    cv2.imshow("Raster Draw", img)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('s'):
        cv2.imwrite(filepath, img)
        print(f"Сохранено как {filepath}")
        break
    elif key == ord('q'):
        print("Выход без сохранения")
        break

cv2.destroyAllWindows()
