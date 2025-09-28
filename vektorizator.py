import os
import cv2
import numpy as np
import svgwrite
import matplotlib.pyplot as plt


def vectorize_binary_raster(img, dilate_kernel=3, dilate_iterations=2):
    mask = (img == 0).astype(np.uint8) * 255
    if dilate_iterations > 0:
        kernel = np.ones((dilate_kernel, dilate_kernel), np.uint8)
        mask = cv2.dilate(mask, kernel, iterations=dilate_iterations)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL,
                                   cv2.CHAIN_APPROX_SIMPLE)
    return contours


def save_svg(contours, filename, img_shape):
    dwg = svgwrite.Drawing(filename, size=(img_shape[1], img_shape[0]))
    for contour in contours:
        points = [(int(p[0][0]), int(p[0][1])) for p in contour]
        dwg.add(dwg.polygon(points, fill="black"))
    dwg.save()
    print(f"SVG сохранён как {filename}")


def show_contours(img, contours):
    vis = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    cv2.drawContours(vis, contours, -1, (0, 0, 255), 1)
    plt.imshow(cv2.cvtColor(vis, cv2.COLOR_BGR2RGB))
    plt.title("Векторное представление растра")
    plt.axis("off")
    plt.show()


def main():
    print("=== Векторизация PNG ===")

    filename_input = input("Введите имя PNG файла (в папке 'png'): ").strip()
    if not filename_input:
        print("Вы не ввели имя файла")
        return

    filename_png = os.path.join("png", filename_input)

    if not os.path.isfile(filename_png):
        print(f"Не удалось найти PNG: {filename_png}")
        return

    img = cv2.imread(filename_png, cv2.IMREAD_GRAYSCALE)
    print(f"PNG загружён: {filename_png}")

    dilate_kernel = int(input(
        "Размер ядра для объединения точек [default: 5]: "
        ) or 5)
    dilate_iterations = int(input(
        "Количество итераций объединения точек [default: 2]: "
        ) or 2)

    contours = vectorize_binary_raster(img, dilate_kernel, dilate_iterations)

    filename_svg = "output.svg"
    save_svg(contours, filename_svg, img.shape)

    show_contours(img, contours)

    if os.path.exists(filename_svg):
        os.remove(filename_svg)


if __name__ == "__main__":
    main()
