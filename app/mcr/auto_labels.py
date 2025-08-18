# import textwrap
import typing as tp
# from datetime import datetime

import data_exporting
import image_utils
import corner_finding
# import scoring
import grid_info as grid_i
import grid_reading as grid_r
# from user_interface import ProgressTrackerWidget
# from mcta_processing import transform_and_save_mcta_output
import cv2
import numpy as np
from image_utils import *
import os

GRID_CELL_CROP_FRACTION = 0.25


def check_x_y(x:int, y:int):
    fields = {
                "last_name":      (1, 3, 12, 28),
                "first_name":     (14, 3, 19, 28),
                "middle_name":    (21, 3, 22, 28),
                "student":        (25, 3, 34, 12),
                "course_id":      (25, 16, 34, 25),
                "test_form_code": (27, 28, 32, 28),
                "ans1": (2, 32, 6,46),
                "ans2": (9, 32, 13, 46),
                "ans3": (16, 32, 20,46),
                "ans4": (23, 32, 27,46),
                "ans5": (30, 32, 34,46),
            }
    for _, (x_min, y_min, x_max, y_max) in fields.items():
        if x_min <= x <= x_max and y_min <= y <= y_max:
            return True
    return False

def process_input(
        image_path_input: str, name_image : str, labels_path : str):
    """Takes input as parameters and process it for either gui or cli.
    
    Parameter progress_tracker determines whith interface in use.
    If progress_tracker is given, function runs in gui mode.
    If progress_tracker parameter is None, prints all progress statuses to stdout.
    """
    form_variant = grid_i.form_75q
    image = cv2.imread(image_path_input)
    prepared_image = image_utils.prepare_scan_for_processing(
        image)
    try:
        corners = corner_finding.find_corner_marks(prepared_image)
    except corner_finding.CornerFindingError:
        return None

    # Dilates the image - removes black pixels from edges, which preserves
    # solid shapes while destroying nonsolid ones. By doing this after noise
    # removal and thresholding, it eliminates irregular things like W and M
    morphed_image = image_utils.dilate(prepared_image)
    # Establish a grid
    grid = grid_r.Grid(corners,
                        grid_i.GRID_HORIZONTAL_CELLS,
                        grid_i.GRID_VERTICAL_CELLS,
                        morphed_image)

    # Calculate fill percent for every bubble
    field_fill_percents = {
        key: grid_r.get_group_from_info(value,
                                        grid).get_all_fill_percents()
        for key, value in form_variant.fields.items() if value is not None
    }
    answer_fill_percents = [
        grid_r.get_group_from_info(question, grid).get_all_fill_percents()
        for question in form_variant.questions
    ]
    threshold = grid_r.calculate_bubble_fill_threshold(
        field_fill_percents,
        answer_fill_percents)

    image = image_utils.bw_to_bgr(morphed_image)
    label_lines = []
    image_h, image_w = image.shape[:2]
    for x in range(grid.horizontal_cells):
        for y in range(grid.vertical_cells):
            check = check_x_y(x,y)
            if not check:
                continue

            unmasked = grid.get_unmasked_cell_matrix(x, y)
            mask = np.ones(unmasked.shape)
            unit_dimension = sum(mask.shape) / 2
            center = (round(mask.shape[0] / 2), round(mask.shape[1] / 2))
            circle_radius = (unit_dimension / 2) * (1 -
                                                    (GRID_CELL_CROP_FRACTION / 2))
            cv2.circle(mask, center, int(circle_radius), (0, 0, 0), -1)
            masked = ma.masked_array(unmasked, mask)
            fill_percent = image_utils.get_fill_percent(masked)
            center, _ = grid.get_cell_circle(x, y)
            box_w = 40
            box_h = 40
            x_center_norm = center.x / image_w
            y_center_norm = center.y / image_h
            w_norm = box_w / image_w
            h_norm = box_h / image_h
            if fill_percent < threshold:
                label_lines.append(f"0 {x_center_norm:.6f} {y_center_norm:.6f} {w_norm:.6f} {h_norm:.6f}")
                continue    
            label_lines.append(f"1 {x_center_norm:.6f} {y_center_norm:.6f} {w_norm:.6f} {h_norm:.6f}")
            # image = cv2.rectangle(image, 
            #                   (int(center.x) - 20, int(center.y) - 20), 
            #                   (int(center.x) + 20, int(center.y) + 20), 
            #                   (0,255,0), thickness=2)
    label_name = image_name.split(".")[0]
    label_path = os.path.join(labels_folder, f"{label_name}.txt")
    with open(label_path, "w") as f:
        f.write("\n".join(label_lines))
    # image_utils.save_image("C://Users//Admin//Documents//mcr//open-mcr//test//end-to-end//75q-core-1-v1//output//grid.jpg", image)
    
if __name__ == '__main__':
    image_folder = r"C:\Users\Admin\Documents\mcr\open-mcr\test\yolo\images\all"
    labels_folder = r"C:\Users\Admin\Documents\mcr\open-mcr\test\yolo\labels"
    images_name = os.listdir(image_folder)
    for image_name in images_name:
        image_path_input = os.path.join(image_folder, image_name)
        image = cv2.imread(image_path_input)
        process_input(image_path_input, image_name, labels_folder)