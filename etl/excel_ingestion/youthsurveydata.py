import json
from typing import TYPE_CHECKING
from collections import namedtuple

from fuzzywuzzy import fuzz

from etl.excel_ingestion.contrib import excel_column_alpha_to_index, ExcelIngestionException
from etl.excel_ingestion.transformations import (
    ScaleTransformation, InverseScaleTransformation, AgreementTransformation, ExpectationTransformation,
    GradeStringToIntTransformation
)
from etl.resources import get_pkg_resource_path

if TYPE_CHECKING:
    from openpyxl.worksheet.worksheet import Worksheet
    from typing import Dict, Tuple


#: Mapping Transformations to configuration keys so in the future we can describe the rules in data with a config
tranformation_name_map = {
    cls.__name__.lower() for cls in (ScaleTransformation,
                                     InverseScaleTransformation,
                                     AgreementTransformation,
                                     ExpectationTransformation,
                                     GradeStringToIntTransformation)
}

QuestionConfigTuple = namedtuple('QuestionConfigTuple', 'column_label expected_header transformation')
"""A container object for the configuration of a particular field.

Args:
    column_label: The expected excel alpha column label ie AAA or AB, case insensitive.
    expected_header: The expected column header at this label case insensitive
    transformation: Optional, one of the transformation names to transform the values
        returned by the Question. Options are ``ScaleTransformation``, ``InverseScaleTransformation``,
        ``AgreementTransformation``, ``ExpectationTransformation``, and ``GradeStringToIntTransformation``.
"""


class YouthSurveyConfigurationException(ExcelIngestionException):
    pass


class WorksheetRunner:
    def __init__(self, worksheet: 'Worksheet', header=0, pk_col_index=0, fuzzy_threshold=75):
        data = list(worksheet.values)
        self.fuzzy_threshold = fuzzy_threshold
        self.questions = []
        self.rows = data[header + 1:]
        self.headers = data[header]
        self.pk_col_index = pk_col_index

    def add_question(self, question):
        """Add a question to the worksheet runner. Question objects are responsible for returning values at indexes."""
        question.add_to_worksheetrunner(self)
        self.questions.append(question)

    def run(self) -> 'Dict[Tuple]':
        """Returns a dictionary whose keys are the primary keys and values are tuples
        of all the :attr:`questions` in order of addition.

        Use the :meth:`add_question` method to add a question to the runner.
        """
        if not self.questions:
            raise ExcelIngestionException(
                f'Worksheetrunner has no questions.'
            )

        ret = {}
        for row_index, row in enumerate(self.rows):
            pk = self._get_pk_value(row_index)
            exists = ret.get(pk)
            if exists:
                raise ExcelIngestionException(
                    f'Primary key {pk} duplicate found at row {row_index}.'
                )
            ret[pk] = self._run_questions(row_index)
        return ret

    def _get_pk_value(self, row_index):
        """Returns the pk value at the row_index."""
        return self.rows[row_index][self.pk_col_index]

    def _run_questions(self, row_index) -> tuple:
        return tuple((question.get_val(row_index) for question in self.questions))


class Question:
    def __init__(self, column_label, expected_header):
        """A wrapper to get the value from the worksheet row.

        Questions check to make sure the expected header is found at the column index
        when added to a :class:`WorksheetRunner`.

        Args:
            column_label: The alpha numeric Excel column label ie 'ab' or 'aaa'
            expected_header: The expected value of the header at the column label. Case insensitive.
        """
        self.column_label = column_label
        self.expected_header = expected_header.lower()
        self.col_index = excel_column_alpha_to_index(column_label)
        self.worksheetrunner = None

    def add_to_worksheetrunner(self, worksheetrunner: WorksheetRunner):
        """Checks the expected header is at the expected column index and links the question to the data."""
        self._check_col(worksheetrunner.headers)
        self.worksheetrunner = worksheetrunner

    def _check_col(self, worksheetrunner):
        headers, fuzz_threshold = worksheetrunner.headers, worksheetrunner.fuzzy_threshold
        val = headers[self.col_index].lower()
        ratio = fuzz.ratio(val, self.expected_header)
        if ratio < fuzz_threshold:
            raise ExcelIngestionException(
                f'Found header value {val} did not exceed fuzzy match {self.expected_header} threshold of '
                f'{fuzz_threshold}.'
            )

    def get_val(self, index):
        """Returns the value at the index."""
        if not self.worksheetrunner:
            raise ExcelIngestionException(
                'Cannot get value without being added to an worksheetrunner.'
            )
        if not self.worksheetrunner.data:
            raise ExcelIngestionException(
                'Cannot get value as worksheetrunner has no data.'
            )
        row = self.worksheetrunner.data[index]
        return row[self.col_index]


def get_questions_from_json() -> 'List[QuestionConfigTuple]':
    file = get_pkg_resource_path('etl.excel_ingestion', 'youthsurveyconfig.json')
    data = json.loads(file.read_text())
    return [QuestionConfigTuple(**obj) for obj in data]


def question_factory(question_config_list: 'List[QuestionConfigTuple]'):
    """Given a list of :class:`QuestionConfigTuple` return a list of Question-like objects.

    Args:
        question_config_list:
    """
    return [_make_question(config_obj) for config_obj in question_config_list]


def _make_question(config_obj: QuestionConfigTuple):
    question = Question(column_label=config_obj.column_label,
                        expected_header=config_obj.expected_header)
    # Wrap it with the appropriate transformation if required.
    transformation = config_obj.transformation
    if transformation:
        try:
            cls = tranformation_name_map[transformation]
        except KeyError:
            raise YouthSurveyConfigurationException(
                f'{config_obj.column_label} column configuration error. '
                f'{transformation} not found in the app.'
            )
        question = cls(question)
    return question
