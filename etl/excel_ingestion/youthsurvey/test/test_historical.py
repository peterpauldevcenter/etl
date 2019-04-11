from etl.excel_ingestion.youthsurvey.youthsurveyhistorical import (
    question_re, get_student_results, validate_and_get_question_metadata, get_answer_for_question
)
from etl.resources import get_pkg_resource_path

from openpyxl import load_workbook

PACKAGE = 'etl.excel_ingestion.youthsurvey.test'


def get_workbook(name: str):
    p = get_pkg_resource_path(PACKAGE, name)
    return load_workbook(p, read_only=True, data_only=True)


def get_data(workbook):
    return list(workbook['Students'].values)


def test_regex():
    question_1 = 'Spring-2016 c. Is there an adult here who helps you when you have a problem?'
    question_2 = 'spring - 2017 b. This is a test question.'
    question_3 = 'fall 2015 another test'

    expected = (
        {'firstword': 'Spring', 'year': '2016',
         'question': 'c. Is there an adult here who helps you when you have a problem?'},
        {'firstword': 'spring', 'year': '2017', 'question': 'b. This is a test question.'},
        {'firstword': 'fall', 'year': '2015', 'question': 'another test'}
    )

    for expected, question in zip(expected, (question_1, question_2, question_3)):
        match = question_re.match(question)
        assert match.groupdict() == expected


def test_get_student_results():
    """Check a known row and make sure the question for the season returns the expected test value."""
    wb = get_workbook('test_student_roster.xlsx')
    data = get_data(wb)
    question_metadata = validate_and_get_question_metadata(data)
    dictionary = get_student_results(1, question_metadata, data)
    answers = dictionary['78']
    fall_2015_records = answers['fall 2015']
    question_txt = 'd. Is there an adult here who you will listen to and respect?'
    answer = get_answer_for_question(fall_2015_records, question_txt)
    assert answer == 4
