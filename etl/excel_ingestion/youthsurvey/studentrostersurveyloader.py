from typing import Dict, Type, AnyStr, Tuple

from openpyxl import load_workbook

from etl.resources import get_pkg_resource_path
from etl.models import questionnaire, timeseries
from etl.views.peter_paul_roster import get_or_create_student, get_or_create_school_year
from etl.excel_ingestion.youthsurvey.contrib import get_or_create
from etl.excel_ingestion.youthsurvey.youthsurveyhistorical import (
    get_workbook, get_data, validate_and_get_question_metadata, get_student_results, YouthSurveyValidationException)
from etl import session


def get_question_object_map() -> Dict[AnyStr, Dict[AnyStr, AnyStr]]:
    p = get_pkg_resource_path('etl.excel_ingestion.youthsurvey', 'youthsurveyconfig.xlsx')
    wb = load_workbook(p, read_only=True, data_only=True)
    config_data = list(wb['Sheet1'].values)
    config_entries = {}
    for entry in config_data[1:]:
        question_text = entry[0]
        cls, attribute = entry[1].split('.')
        config_entries.update({question_text: {'cls': cls, 'attribute': attribute}})

    return config_entries


def load_student_roster_to_db(workbook_path):
    wb = get_workbook(workbook_path)
    data = get_data(wb)
    student_rows = data[1:]
    question_metadata = validate_and_get_question_metadata(data)

    for row_index, row in enumerate(student_rows):
        student_token = str(row[0])
        if not student_token:
            raise YouthSurveyValidationException(
                f'No student token was found on the first column {row_index + 1} row.'
            )

        student_results = get_student_results(question_metadata, row)
        all_semester_data = student_results[student_token]
        for semester_key, semester_answers in all_semester_data.items():
            process_student_data(student_token, semester_key, semester_answers)


def process_student_data(student_token, semester_key, semester_answers: dict):
    student = get_or_create_student(student_token)
    question_object_map = get_question_object_map()
    container = get_or_create_container(student, semester_key)
    create_sections(container, question_object_map, semester_answers)


def get_or_create_container(student, semseter_key):
    season, year = semseter_key.split()
    semester = get_or_create_semester(season, year)
    container = get_or_create_questionnaire_container(student, semester)
    return container


def get_or_create_semester(season, year):
    year = int(year)
    school_year = get_or_create_school_year(int(year))
    season = season.capitalize()
    semester = session.query(timeseries.Semester).filter_by(school_year_id=school_year.id, name=season).first()
    if not semester:
        semester = timeseries.Semester(school_year=year, name=season)
    return semester


def get_or_create_questionnaire_container(student, semester):
    student_id = student.id
    semester_id = semester.id
    return get_or_create(session,
                         questionnaire.StudentExperienceQuestionnaire,
                         student_id=student_id,
                         semester_id=semester_id)


def create_sections(container, question_object_map, semester_answers):
    # Map of model to list of attrs
    model_question_map = {}
    for question_txt, mapping in question_object_map.items():
        model_name = mapping['cls']
        attr_name = mapping['attribute']
        model_question_map.setdefault(model_name, {})
        model_question_map[model_name].update({attr_name: question_txt})

    for model_name, attr_to_question in model_question_map.items():
        model = getattr(questionnaire, model_name)
        section = get_or_create_section(model, container)
        for attr_name, question_txt in attr_to_question.items():
            answer = semester_answers.get(question_txt)
            setattr(section, attr_name, answer)
        session.commit()


def get_or_create_section(model, container):
    return get_or_create(session, model, student_experience_questionnaire_id=container.id)


def get_model_attr_for_question(question_txt, question_object_map) -> Tuple[Type, AnyStr]:
    """Returns a tuple of Model, Attribute where Model is the model and attribute
    combination map to the question.

    Args:
        question_txt:
        question_object_map:
    """
    entry = question_object_map[question_txt]
    model = getattr(questionnaire, entry['cls'])
    attr = entry['attribute']
    return model, attr


def create_or_update_model_for_question(question_txt, answer, container):
    question_object_map = get_question_object_map()
    model, attribute = get_model_attr_for_question(question_txt, question_object_map)

    section_instance = get_or_create(session, model, student_experience_questionnaire_id=container.id)
    setattr(section_instance, attribute, answer)
    session.commit()
