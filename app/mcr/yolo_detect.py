from ultralytics import YOLO
import typing as tp
import data_exporting
import image_utils
import corner_finding
import grid_info as grid_i
import grid_reading as grid_r
import cv2
import grid_info
import geometry_utils
from collections import defaultdict
from grid_reading import *

model = YOLO("weights/best.pt")

def find_field_containing_cell(cell_index: tuple[int, int], form_variant: grid_info.FormVariant) -> tuple[str, grid_info.GridGroupInfo] | None:
    x, y = cell_index

    for field, group_info in form_variant.fields.items():
        if group_info is None:
            continue

        field_vertical = group_info.field_orientation == geometry_utils.Orientation.VERTICAL
        for i in range(group_info.num_fields):
            start_x = group_info.horizontal_start + i if field_vertical else group_info.horizontal_start
            start_y = group_info.vertical_start + i if not field_vertical else group_info.vertical_start

            for j in range(group_info.field_length):
                cur_x = start_x if field_vertical else start_x + j
                cur_y = start_y + j if field_vertical else start_y

                if (x, y) == (cur_x, cur_y):
                    return (field, group_info)
    for idx, group_info in enumerate(form_variant.questions):
        field_vertical = group_info.field_orientation == geometry_utils.Orientation.VERTICAL
        start_x = group_info.horizontal_start
        start_y = group_info.vertical_start

        for j in range(group_info.field_length):
            cur_x = start_x if field_vertical else start_x + j
            cur_y = start_y + j if field_vertical else start_y
            if (x, y) == (cur_x, cur_y):
                return (f"question_{idx}", group_info)
    return None

def is_cell_in_group(across: int, down: int, group_info: grid_info.GridGroupInfo) -> bool:
    for i in range(group_info.num_fields):
        if group_info.field_orientation == geometry_utils.Orientation.VERTICAL:
            x = group_info.horizontal_start + i
            y = group_info.vertical_start
        else:
            x = group_info.horizontal_start
            y = group_info.vertical_start + i

        for j in range(group_info.field_length):
            if group_info.field_orientation == geometry_utils.Orientation.VERTICAL:
                cell = (x, y + j)
            else:
                cell = (x + j, y)
            if cell == (across, down):
                return True
    return False

def generate_complete_string(field_info: grid_info.GridGroupInfo, grid: Grid, filled_cells: list[tuple[int, int]]) -> list[str]:
    field_group = get_group_from_info(field_info, grid)

    result = []

    for field in field_group.fields:
        field_chars = []
        for i in range(field.num_cells):
            is_vertical = field.orientation == grid_info.Orientation.VERTICAL
            x = field.horizontal_start if is_vertical else field.horizontal_start + i
            y = field.vertical_start if not is_vertical else field.vertical_start + i
            if (x, y) in filled_cells:
                value = alphabet.letters[i] if field_info.fields_type == grid_info.FieldType.LETTER else str(i)
            else:
                value = ""
            field_chars.append(value)
        result.append("".join(field_chars))
    return result

def generate_question_string(
    question_info: grid_info.GridGroupInfo,
    filled_cells: list[tuple[int, int]]
) -> str:
    result = []
    is_vertical = question_info.field_orientation == grid_info.Orientation.VERTICAL
    start_x = question_info.horizontal_start
    start_y = question_info.vertical_start

    for i in range(question_info.field_length):
        x = start_x if is_vertical else start_x + i
        y = start_y + i if is_vertical else start_y

        if (x, y) in filled_cells:
            if question_info.fields_type == grid_info.FieldType.LETTER:
                value = alphabet.letters[i]
            else:
                value = str(i)
        else:
            value = ""
        result.append(value)

    return "".join(result)

def yolo_detect(image) -> list:
    detections = model.predict(
        source=image,
        imgsz=1280,
    )
    results = []
    for r in detections:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = float(box.conf[0])
            cls_id = int(box.cls[0])
            results.append([x1, y1, x2, y2, conf, cls_id])
    return results

def yolo_process_input(
        image: bytes,
        image_name:str
        ):
    """Takes input as parameters and process it for either gui or cli.
    
    Parameter progress_tracker determines whith interface in use.
    If progress_tracker is given, function runs in gui mode.
    If progress_tracker parameter is None, prints all progress statuses to stdout.
    """
    form_variant = grid_i.form_75q
    try:
        file_bytes = np.asarray(bytearray(image), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        # image = cv2.imread(image)
        prepared_image = image_utils.prepare_scan_for_processing(
            image)
        try:
            corners = corner_finding.find_corner_marks(prepared_image)
        except corner_finding.CornerFindingError:
            return None
        morphed_image = image_utils.dilate(prepared_image)
        # Establish a grid
        grid = grid_r.Grid(corners,
                            grid_i.GRID_HORIZONTAL_CELLS,
                            grid_i.GRID_VERTICAL_CELLS,
                            morphed_image)
        
        yolo_results = yolo_detect(image)
        grouped_results = defaultdict(list)
        for result in yolo_results:
            x1, y1, x2, y2, conf, cls_id = result
            bbox = (x1, y1, x2, y2)
            x, y = grid.get_cell_index_from_bbox(bbox)
            group = find_field_containing_cell((x, y), form_variant)
            if group:
                key = group[0]
                grouped_results[key].append((x, y))
        questions = []
        last_name = []
        first_name = []
        middle_name = []
        test_form_code = []
        student_id = []
        course_id = []
        fields = []
        middle_name = ''
        for key, cells in grouped_results.items():
            if isinstance(key, str) and key.startswith("question_"):
                index = int(key.split('_')[1])
                field_info = grid_i.form_75q.questions[index]
                result = generate_question_string(field_info, cells)
                questions.append([index, result])
            else:
                field_info = grid_i.form_75q.fields[key]
                result = generate_complete_string(field_info, grid, cells)
                if key.name == 'LAST_NAME':
                    last_name = "".join(result)
                    fields.append(['Last Name', last_name])
                elif key.name == 'COURSE_ID':
                    course_id = "".join(result)
                    fields.append(['Course ID', course_id])
                elif key.name == 'STUDENT_ID':
                    student_id = "".join(result)
                    fields.append(['Student ID', student_id])
                elif key.name == 'TEST_FORM_CODE':
                    test_form_code = "".join(result)
                    fields.append(['Test Form Code', test_form_code])
                elif key.name == 'FIRST_NAME':
                    first_name = "".join(result)
                    fields.append(['First Name', first_name])
                elif key.name == 'MIDDLE_NAME':
                    middle_name = "".join(result)
        fields.append(['Source File', image_name])
        fields.append(['Middle Name', middle_name])
        questions = sorted(questions, key=lambda x: x[0])
        questions = [[f"Q{idx+1}", value] for idx, value in questions]
        data = fields + questions
        return data
    except Exception as e:
        print("Error:", e)
        return None
