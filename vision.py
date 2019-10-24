from constants import *
import cv2
from vizutil import *
import grip4 as grip
# import ntinter as nt
import numpy as np
import pprint


print('VERSION')
print(cv2.__version__)

cap = cv2.VideoCapture(0)
pipeline = grip.GripPipeline()
pp = pprint.PrettyPrinter()
rl_points = TARGET
debug = False

dist_mat = np.zeros((4, 1))
# frame = np.zeros([640, 480, 3], dtype=np.uint8)

while True:
    # Read the frame and process it using the GRIP-generated pipeline
    _, frame = cap.read()
    pipeline.process(frame)
    # Get images and contours from the pipeline
    normal = pipeline.normalize_output
    contours = pipeline.filter_contours_output
    cv2.drawContours(normal, contours, -1, RED, 3)

    # Bodged Camera Parameters
    size = normal.shape
    focal_length = size[1]
    center = (size[1]/2, size[0]/2)
    camera_matrix = np.array([[focal_length, 0, center[0]],
                              [0, focal_length, center[1]],
                              [0, 0, 1]], dtype="double")

    if len(contours) is not 0:
        extremes = find_points(contours)
        if len(extremes) is 4:
            # print("target detected")
            camera = get_vectors(extremes, TARGET, camera_matrix, dist_mat)
            if camera[0]:
                rVec = camera[1]
                tVec = camera[2]
                center = project_origin(rVec, tVec, camera_matrix, dist_mat)
                hitbox_contour = project_hitbox(HITBOX, rVec, tVec, camera_matrix, dist_mat)
                draw_bounding_box(normal, hitbox_contour, WHITE, 5)

    cv2.circle(normal, RETICLE, 1, WHITE, 5)

    # # Draw contour extremes
    # for point in px_points:
    #     cv2.circle(normal, point, 1, AQUA, 5)

    # Draw the reticle
    cv2.circle(normal, RETICLE, 1, WHITE, 5)

    # -1: reflect over x-axis
    # 1: reflect over y-axis
    # 0: reflect over origin
    # normal = cv2.flip(frame, -1)

    cv2.imshow('Contours', normal)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

