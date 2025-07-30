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

def process_input(
        image: bytes,
        image_name:str
        ):
    """Takes input as parameters and process it for either gui or cli.
    
    Parameter progress_tracker determines whith interface in use.
    If progress_tracker is given, function runs in gui mode.
    If progress_tracker parameter is None, prints all progress statuses to stdout.
    """
    form_variant = grid_i.form_75q
    answers_results = data_exporting.OutputSheet([x for x in grid_i.Field],
                                                 form_variant.num_questions)
    keys_results = data_exporting.OutputSheet([grid_i.Field.TEST_FORM_CODE, grid_i.Field.IMAGE_FILE],
                                              form_variant.num_questions)

    try:
        file_bytes = np.asarray(bytearray(image), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
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
        # Get the answers for questions
        answers = [
            grid_r.read_answer_as_string(i, grid,
                                            threshold, form_variant,
                                            answer_fill_percents[i])
            for i in range(form_variant.num_questions)
        ]
        field_data: tp.Dict[grid_i.RealOrVirtualField, str] = {
            grid_i.Field.IMAGE_FILE: image_name,
        }
        # Read the Student ID. If it indicates this exam is a key, treat it as such
        student_id = grid_r.read_field_as_string(
            grid_i.Field.STUDENT_ID, grid, threshold, form_variant,
            field_fill_percents[grid_i.Field.STUDENT_ID])
        if student_id == grid_i.KEY_STUDENT_ID:
            form_code_field = grid_i.Field.TEST_FORM_CODE
            field_data[form_code_field] = grid_r.read_field_as_string(
                form_code_field, grid, threshold, form_variant,
                field_fill_percents[form_code_field]) or ""
            keys_results.add(field_data, answers)

        else:
            for field in form_variant.fields.keys():
                field_value = grid_r.read_field_as_string(
                    field, grid, threshold, form_variant,
                    field_fill_percents[field])
                if field_value is not None:
                    field_data[field] = field_value
            answers_results.add(field_data, answers)
        answers_results.clean_up(
            replace_empty_with="G")
        data = answers_results.save()
        return data
    except Exception as e:
        print("Error:", e)
        return None