import cv2
from constants import *


# Find the four points farthest from the center in the given contour
def find_extremes(cnt):
    extremes = [tuple(cnt[cnt[:, :, 1].argmin()][0]),  # North
                tuple(cnt[cnt[:, :, 0].argmin()][0]),  # East
                tuple(cnt[cnt[:, :, 1].argmax()][0]),  # South
                tuple(cnt[cnt[:, :, 0].argmax()][0])]  # West
    return extremes


# Find the Northernmost point in a given contour
def find_north_extreme(cnt):
    return tuple(cnt[cnt[:, :, 1].argmin()][0])


# Find the Southernmost point in a given contour
def find_south_extreme(cnt):
    return tuple(cnt[cnt[:, :, 1].argmax()][0])


# Find the Easternmost point in a given contour
def find_east_extreme(cnt):
    return tuple(cnt[cnt[:, :, 0].argmin()][0])


# Find the Westernmost point in a given contour
def find_west_extreme(cnt):
    return tuple(cnt[cnt[:, :, 0].argmax()][0])


# Draws the generated contour
def draw_bounding_box(img, cnt, color, thickness):
    contour = find_extremes(cnt)
    for i in range(len(contour)):
        cv2.line(img,
                 (contour[i-1][0], contour[i-1][1]),
                 (contour[i][0], contour[i][1]),
                 color,
                 thickness)


# Processing Functions
def calc_cam_mat(src):
    size = src.shape
    focal_length = size[1]
    center = (size[1]/2, size[0]/2)
    cam_mat = np.array([[focal_length, 0, center[0]],
                        [0, focal_length, center[1]],
                        [0, 0, 1]], dtype="double")
    return cam_mat


# Find pix points
def find_points(cnt):
    px_points = []
    for contour in cnt:
        px_points.append(find_north_extreme(contour))
        px_points.append(find_south_extreme(contour))
    return px_points


# get rVec and tVec
def get_vectors(px_points, rl_points, cam_mat, dist_coeffs):
    if len(px_points) is 4:
        return cv2.solvePnP(rl_points, np.asarray(px_points, dtype='double'), cam_mat, dist_coeffs, 0)


def project_origin(r_vec, t_vec, cam_mat, dist_coeffs):
    (target, _) = cv2.projectPoints(np.array([(0.0, 0.0, 0.0)]),
                                    r_vec, t_vec, cam_mat, dist_coeffs)
    return int(target[0][0][0]), int(target[0][0][1])


def project_hitbox(rl_points, r_vec, t_vec, cam_mat, dist_coeffs):
    (hitbox_points, _) = cv2.projectPoints(rl_points, r_vec, t_vec, cam_mat, dist_coeffs)
    hitbox_contour = np.asarray(hitbox_points, dtype='int32')
    return hitbox_contour
