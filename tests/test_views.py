import pathlib
import os
import datetime
import sqlalchemy
import etl
import settings
from etl.models.student_demographics import School, Student, StudentDemographics, StudentAnnualDemographics
from etl.views.student_demographics import SchoolListView, StudentListView, StudentDemographicsListView, \
    StudentAnnualDemographicsListView
from etl.models.report_card import SchoolAttendance, ReportCard
from etl.views.report_card import SchoolAttendanceListView, ReportCardListView
from etl.models.timeseries import MarkingPeriod, SchoolYear
from etl import session
from .context import PACKAGE_ROOT


try:
    os.remove(settings.DATABASE)
except OSError:
    pass
engine = sqlalchemy.create_engine(settings.ENGINE)


def get_instance(model, **kwargs):
    return session.query(model).filter_by(**kwargs).first()


def setup_module():
    etl.models.Base.metadata.create_all(engine)


def teardown_module():
    try:
        os.remove(settings.DATABASE)
    except OSError:
        pass


def get_test_data_file(file_name: str):
    return PACKAGE_ROOT / pathlib.Path(f'static/{file_name}')


def test_read_schools_from_map_test():
    test_data_file = get_test_data_file('MAP_Test_Data.xlsx')
    view_instance = SchoolListView()
    view_instance.post(test_data_file)
    school = get_instance(School, name='Woodville Elementary')
    assert school.district == 'Richmond City Public Schools'


def test_read_students_from_student_roster():
    test_data_file = get_test_data_file('Student_Roster_Test_Data.xlsx')
    view_instance = StudentListView()
    view_instance.post(test_data_file)
    student = get_instance(Student, student_token=94)
    assert student.student_token == 94


def test_read_student_demographics_from_map_file():
    test_data_file = get_test_data_file('MAP_Test_Data.xlsx')
    view_instance = StudentDemographicsListView()
    view_instance.post(test_data_file, 'MAP')
    student = get_instance(Student, student_token=16)
    student_demograpics = get_instance(StudentDemographics, student_id=student.id)
    assert student_demograpics.gender == 'M'
    assert student_demograpics.ethnic_group == '3'


def test_read_student_demographics_from_demographics_file():
    test_data_file = get_test_data_file('Student_Demographics_Test_Data.xlsx')
    view_instance = StudentDemographicsListView()
    view_instance.post(test_data_file, 'Demographics')
    student = get_instance(Student, student_token=134)
    student_demographics = get_instance(StudentDemographics, student_id=student.id)
    assert student_demographics.gender == 'F'
    assert student_demographics.year_of_birth == 2007
    assert student_demographics.race == 'African American'


def test_read_student_demographics_from_roster_file():
    test_data_file = get_test_data_file('Student_Roster_Test_Data.xlsx')
    view_instance = StudentDemographicsListView()
    view_instance.post(test_data_file, 'Roster')
    student = get_instance(Student, student_token=43)
    student_demographics = get_instance(StudentDemographics, student_id=student.id)
    assert student_demographics.peter_paul_enrollment_date == datetime.datetime(2011, 6, 1, 0, 0)


def test_read_student_annual_demographics_from_demographics_file():
    test_data_file = get_test_data_file('Student_Demographics_Test_Data.xlsx')
    view_instance = StudentAnnualDemographicsListView()
    view_instance.post(test_data_file, 'Demographics')
    student = get_instance(Student, student_token=120)
    student_annual_demographics = get_instance(StudentAnnualDemographics, student_id=student.id)
    assert student_annual_demographics.family_size == 4
    assert student_annual_demographics.household_type == 'Eastview'
    assert student_annual_demographics.family_setting == 'Two Parent Household'
    assert student_annual_demographics.income_category == '$0 - 10,000'
    assert student_annual_demographics.disability is False
    assert student_annual_demographics.promise_family_network == 'PFN'


def test_read_student_annual_demographics_from_report_card_file():
    test_data_file = get_test_data_file('Report_Card_Test_Data.xlsx')
    view_instance = StudentAnnualDemographicsListView()
    view_instance.post(test_data_file, 'Report Card')
    student = get_instance(Student, student_token=7)
    student_annual_demographics = get_instance(StudentAnnualDemographics, student_id=student.id)
    assert student_annual_demographics.school.name == 'Bellevue Elementary School'
    assert student_annual_demographics.grade_level == 3
    assert student_annual_demographics.promoted is False
    assert student_annual_demographics.individualized_education_plan_indicator is False


def test_read_school_attendence_from_report_card_file():
    test_data_file = get_test_data_file('Report_Card_Test_Data.xlsx')
    view_instance = SchoolAttendanceListView()
    view_instance.post(test_data_file)
    student = get_instance(Student, student_token=6)
    school_year = get_instance(SchoolYear, school_year=2019)
    marking_period = get_instance(MarkingPeriod, name='MP1', school_year_id = school_year.id)
    attendance = get_instance(SchoolAttendance, student_id=student.id, marking_period_id=marking_period.id)
    assert attendance.days_absent == 1
    assert attendance.days_tardy == 17
    assert attendance.days_present == 43
    assert attendance.days_suspended == 0
    assert attendance.suspension_reason is None
    marking_period = get_instance(MarkingPeriod, name='MP2', school_year_id = school_year.id)
    attendance = get_instance(SchoolAttendance, student_id=student.id, marking_period_id=marking_period.id)
    assert attendance.days_absent == 2
    assert attendance.days_tardy == 19
    assert attendance.days_present == 43
    assert attendance.days_suspended == 3
    assert attendance.suspension_reason == 'Jib Jabbin'


def test_read_grades_from_report_card_file():
    test_data_file = get_test_data_file('Report_Card_Test_Data.xlsx')
    view_instance = ReportCardListView()
    view_instance.post(test_data_file)
    student = get_instance(Student, student_token=5)
    school_year = get_instance(SchoolYear, school_year=2019)
    marking_period = get_instance(MarkingPeriod, name='MP1', school_year_id = school_year.id)
    grade = get_instance(ReportCard, student_id=student.id, marking_period_id=marking_period.id,
                         subject='3rd Grade Mathematics')
    assert grade.grade_raw == 'C'
    assert grade.grade_letter == 'C'
    assert grade.grade_number == 70
    grade = get_instance(ReportCard, student_id=student.id, marking_period_id=marking_period.id,
                         subject='3rd Grade Language Arts')
    assert grade.grade_raw == 'A'
    assert grade.grade_letter == 'A'
    assert grade.grade_number == 90
    marking_period = get_instance(MarkingPeriod, name='MP2', school_year_id = school_year.id)
    grade = get_instance(ReportCard, student_id=student.id, marking_period_id=marking_period.id,
                         subject='3rd Grade Mathematics')
    assert grade.grade_raw == '84'
    assert grade.grade_letter == 'B'
    assert grade.grade_number == 84
    grade = get_instance(ReportCard, student_id=student.id, marking_period_id=marking_period.id,
                         subject='3rd Grade Language Arts')
    assert grade.grade_raw == '91.48'
    assert grade.grade_letter == 'A'
    assert grade.grade_number == 91.48
