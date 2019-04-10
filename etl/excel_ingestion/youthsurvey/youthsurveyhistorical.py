"""
The historical data is saved in a likert-like format on the Student Roster file.

Each year is captured under a different column, and so the ranges must be mapped for ETL.
"""
import re
from etl.excel_ingestion.youthsurvey.youthsurveydata import YouthSurveyValidationException


survey_header_range_start = 'DE'
survey_header_range_end = 'NS'

question_re = re.compile(r'(?P<firstword>\A\w*)(?=\s)?.*(?P<year>\d{4})\s?(?P<question>.*)')


def process_year(year: int, column_range: str):
    pass


def get_season_year_question_from_header(header_value: str) -> dict:
    """Extracts the values of "firstword", "year", and "question", from the header as a dict.

    Args:
        header_value:
    """
    match = question_re.match(header_value)
    if not match:
        raise YouthSurveyValidationException(
            f'Could not match regular expression format of header {header_value}.'
        )
    data = match.groupdict()
    for key, value in data.items():
        if not value:
            raise YouthSurveyValidationException(
                f'Missing {key} for header {header_value}.'
            )
    return data

