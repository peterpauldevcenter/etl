from typing import List
from collections import namedtuple

from openpyxl import load_workbook

from etl.resources import get_pkg_resource_path
from etl.models import questionnaire
from etl.views.peter_paul_roster import get_or_create_school_year, get_or_create_student
from etl.excel_ingestion.youthsurvey.youthsurveyhistorical import (
    get_workbook, get_data, validate_and_get_question_metadata)


QuestionConfig = namedtuple('QuestionConfig', 'question_text cls attribute')


def get_question_object_map() -> List[QuestionConfig]:
    p = get_pkg_resource_path('etl.excel_ingestion.youthsurvey', 'youthsurveyconfig.xlsx')
    wb = load_workbook(p, read_only=True, data_only=True)
    config_data = list(wb['Sheet1'].values)
    config_entries = []
    for entry in config_data[1:]:
        question_text = entry[0]
        cls, attribute = entry[1].split('.')
        config_entries.append(QuestionConfig(question_text, cls, attribute))

    return config_entries


def load_student_roster_to_db(workbook_path):
    wb = get_workbook(workbook_path)
    data = get_data(wb)
    student_records = data[1:]
    question_metadata = validate_and_get_question_metadata(data)


def process_student_data(student_token, semester_data: dict):
    student = get_or_create_student(student_token)
    semester = get_or_create_school_year()




config_entries = get_question_object_map()
