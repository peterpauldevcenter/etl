import sys
import pathlib
import logging

PACKAGE_ROOT = pathlib.Path(__file__).parent
PROJECT_ROOT = PACKAGE_ROOT.parent
sys.path.insert(0, str(PROJECT_ROOT.absolute()))

logger = logging.getLogger(__name__)
# noinspection PyUnresolvedReferences
import etl
# noinspection PyUnresolvedReferences
from etl.models.timeseries import SchoolYear, Semester, Trimester, MarkingPeriod
from etl.models.student_demographics import School, Student, StudentDemographics, StudentAnnualDemographics
from etl.models.report_card import SchoolAttendance, ReportCard
from etl.models.peter_paul_roster import PeterPaulLocation, StudentAnnualPeterPaulSummary
from etl.models.map_testing import MAPTestGoal, MAPTest, MAPTestGrowth

try:
    import settings
    logging.info('Using project level settings.')
except ImportError:
    from tests import settings
    logging.info('Using package level settings.')
