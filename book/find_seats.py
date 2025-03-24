import cv2
import numpy as np


def detect_adjacent_colored_circles(image_path, output_path="output.png"):
    # Load the image
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Convert to HSV to filter non-gray colors
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define lower and upper bounds for non-gray colors (e.g., green circles)
    lower_bound = np.array([30, 40, 40])  # Adjust based on color range
    upper_bound = np.array([90, 255, 255])

    # Mask non-gray colors
    mask = cv2.inRange(hsv, lower_bound, upper_bound)

    # Detect circles using HoughCircles
    circles = cv2.HoughCircles(
        gray,
        cv2.HOUGH_GRADIENT,
        dp=1.2,
        minDist=10,
        param1=50,
        param2=30,
        minRadius=5,
        maxRadius=15,
    )

    adjacent_pairs = []

    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        colored_circles = [(x, y) for x, y, r in circles if mask[y, x] > 0]

        # Find adjacent circles
        for i, (x1, y1) in enumerate(colored_circles):
            for j, (x2, y2) in enumerate(colored_circles):
                if (
                    i != j and abs(x1 - x2) <= 20 and abs(y1 - y2) <= 5
                ):  # Close in x, same y
                    adjacent_pairs.append(((x1, y1), (x2, y2)))
                    break  # Select only one pair

    # If adjacent pairs are found, modify the image by coloring the first detected pair in red
    if adjacent_pairs:
        (x1, y1), (x2, y2) = adjacent_pairs[0]  # Select the first adjacent pair

        # Draw the two adjacent circles in red
        cv2.circle(image, (x1, y1), 10, (0, 0, 255), -1)  # Red color (BGR format)
        cv2.circle(image, (x2, y2), 10, (0, 0, 255), -1)

    # Save the modified image
    cv2.imwrite(output_path, image)

    return adjacent_pairs, output_path


def transform_coordinates(
    img_x, img_y, image_width, image_height, canvas_width, canvas_height
):
    """
    Convert an image coordinate to the corresponding canvas pixel coordinate.
    """

    print(img_x, img_y)
    canvas_x = float(img_x) * (canvas_width / image_width)
    canvas_y = float(img_y) * (canvas_height / image_height)
    return canvas_x, canvas_y


[
    ((np.int64(1083), np.int64(218)), (np.int64(1102), np.int64(218))),
    ((np.int64(1180), np.int64(218)), (np.int64(1199), np.int64(218))),
    ((np.int64(1786), np.int64(262)), (np.int64(1805), np.int64(262))),
    ((np.int64(1199), np.int64(218)), (np.int64(1180), np.int64(218))),
    ((np.int64(1102), np.int64(218)), (np.int64(1083), np.int64(218))),
    ((np.int64(1180), np.int64(195)), (np.int64(1161), np.int64(195))),
    ((np.int64(307), np.int64(263)), (np.int64(287), np.int64(265))),
    ((np.int64(209), np.int64(263)), (np.int64(229), np.int64(265))),
    ((np.int64(289), np.int64(285)), (np.int64(269), np.int64(285))),
    ((np.int64(1805), np.int64(262)), (np.int64(1786), np.int64(262))),
    ((np.int64(1220), np.int64(242)), (np.int64(1201), np.int64(242))),
    ((np.int64(1142), np.int64(195)), (np.int64(1161), np.int64(195))),
    ((np.int64(1161), np.int64(195)), (np.int64(1180), np.int64(195))),
    ((np.int64(328), np.int64(241)), (np.int64(309), np.int64(241))),
    ((np.int64(191), np.int64(308)), (np.int64(211), np.int64(307))),
    ((np.int64(289), np.int64(307)), (np.int64(269), np.int64(308))),
    ((np.int64(367), np.int64(285)), (np.int64(347), np.int64(285))),
    ((np.int64(1201), np.int64(242)), (np.int64(1220), np.int64(242))),
    ((np.int64(211), np.int64(307)), (np.int64(191), np.int64(308))),
    ((np.int64(191), np.int64(285)), (np.int64(211), np.int64(285))),
    ((np.int64(211), np.int64(285)), (np.int64(191), np.int64(285))),
    ((np.int64(287), np.int64(265)), (np.int64(307), np.int64(263))),
    ((np.int64(269), np.int64(285)), (np.int64(289), np.int64(285))),
    ((np.int64(230), np.int64(285)), (np.int64(211), np.int64(285))),
    ((np.int64(308), np.int64(285)), (np.int64(289), np.int64(285))),
    ((np.int64(309), np.int64(241)), (np.int64(328), np.int64(241))),
    ((np.int64(229), np.int64(265)), (np.int64(209), np.int64(263))),
    ((np.int64(153), np.int64(351)), (np.int64(173), np.int64(351))),
    ((np.int64(230), np.int64(308)), (np.int64(211), np.int64(307))),
    ((np.int64(172), np.int64(286)), (np.int64(191), np.int64(285))),
    ((np.int64(190), np.int64(265)), (np.int64(209), np.int64(263))),
    ((np.int64(249), np.int64(263)), (np.int64(229), np.int64(265))),
    ((np.int64(249), np.int64(285)), (np.int64(269), np.int64(285))),
    ((np.int64(269), np.int64(308)), (np.int64(289), np.int64(307))),
    ((np.int64(308), np.int64(307)), (np.int64(289), np.int64(307))),
    ((np.int64(347), np.int64(285)), (np.int64(367), np.int64(285))),
    ((np.int64(173), np.int64(351)), (np.int64(153), np.int64(351))),
    ((np.int64(153), np.int64(285)), (np.int64(172), np.int64(286))),
    ((np.int64(386), np.int64(285)), (np.int64(367), np.int64(285))),
]
