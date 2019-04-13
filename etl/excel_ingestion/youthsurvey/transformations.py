"""
Transformations for questions are objects wrap how questions get a value. They can be chained.

See the decorator pattern.
"""
import abc
import re
from typing import TYPE_CHECKING

from etl.excel_ingestion.utils import ExcelIngestionException

if TYPE_CHECKING:
    from etl.excel_ingestion.youthsurvey.new import Question, WorksheetRunner
    from typing import Any


class TransformationException(ExcelIngestionException):
    pass


class QuestionTransformation(abc.ABC):
    """Decorates :class:`~etl.excel_ingestion.youthsurveydata.Question`"""
    def __init__(self, wrapped: 'Question'):
        self._wrapped = wrapped

    def add_to_worksheetrunner(self, worksheetrunner: 'WorksheetRunner'):
        """Checks the expected header is at the expected column index and links the question to the data."""
        self._wrapped.add_to_worksheetrunner(worksheetrunner)

    @abc.abstractmethod
    def get_val(self, index) -> 'Any':
        raise NotImplementedError


class ScaleTransformation(QuestionTransformation):
    """Returns the integer mapped for no, mostly no, etc."""
    likert_map = {
        'no': 1,
        'mostly no': 2,
        'mostly yes': 3,
        'yes': 4
    }

    def get_val(self, index) -> int:
        original_val = self._wrapped.get_val(index)
        if not original_val:
            return original_val

        key = original_val.lower()
        try:
            return self.likert_map[key]
        except KeyError:
            valid_opts = ' '.join(self.likert_map.keys())
            raise TransformationException(
                f'{self.__class__.__name__} does not have a key for {key}. Valid options are {valid_opts}.'
            )


class InverseScaleTransformation(ScaleTransformation):
    """Similar to :class:`ScaleTransformation` only in reverse for those
    questions which need to be phrased negatively to make sense.
    """
    likert_map = {
        'no': 4,
        'mostly no': 3,
        'mostly yes': 2,
        'yes': 1
    }


class AgreementTransformation(ScaleTransformation):
    """Same as :class:`ScaleTransformation` only for agreement."""
    likert_map = {
        'don\'t agree': 1,
        'agree a little': 2,
        'mostly agree': 3,
        'agree a lot': 4
    }


class ExpectationTransformation(ScaleTransformation):
    """Same as :class:`ScaleTransformation` only for probablies and maxes at 3."""
    likert_map = {
        'probably won\'t': 1,
        'probably will': 2,
        'definitely will': 3
    }


class GradeStringToIntTransformation(ScaleTransformation):
    regex = re.compile(r'\A\d*')

    def get_val(self, index) -> int:
        original_val = self._wrapped.get_val(index)
        if not original_val:
            return original_val
        string = self._wrapped.get_val(index)
        match = self.regex.match(string)

        if not match:
            raise TransformationException(
                f'{string} does not meet the number format (ie 10th, 9th, 2nd, etc).'
            )
        return int(match.group())
