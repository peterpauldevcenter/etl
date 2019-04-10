import sqlalchemy
import os
from etl.models.timeseries import SchoolYear, Semester, Trimester, MarkingPeriod
from etl.models.student_demographics import School, Student, StudentDemographics, StudentAnnualDemographics
from etl.models.report_card import SchoolAttendance, ReportCard
from etl.models.peter_paul_roster import PeterPaulLocation, StudentAnnualPeterPaulSummary
import etl
import settings


try:
    os.remove(settings.DATABASE)
except OSError:
    pass
engine = sqlalchemy.create_engine(settings.ENGINE)
session = etl.session


def create_instance(model, **kwargs):
    instance = model(**kwargs)
    session.add(instance)
    session.commit()


def get_instance(model, **kwargs):
    return session.query(model).filter_by(**kwargs).first()


def setup_module():
    etl.models.Base.metadata.create_all(engine)


def teardown_module():
    try:
        os.remove(settings.DATABASE)
    except OSError:
        pass


def test_add_school_year():
    model = SchoolYear
    create_instance(model, school_year=2019)
    new_instance = get_instance(model, start_year=2018)
    assert new_instance.name == '2018-2019'


def test_add_semester():
    model = Semester
    create_instance(model, school_year=2017, name='Fall')
    new_instance = get_instance(model, name='Fall')
    assert new_instance.time_series_sequence == 2*(2017-1)+0
    assert new_instance.school_year.start_year == 2016


def test_add_trimester():
    model = Trimester
    create_instance(model, school_year=2016, name='Winter')
    new_instance = get_instance(model, name='Winter')
    assert new_instance.time_series_sequence == 3*(2016-1)+1
    assert new_instance.school_year.start_year == 2015


def test_add_marking_period():
    model = MarkingPeriod
    create_instance(model, school_year=2015, name='MP3')
    new_instance = get_instance(model, name='MP3')
    assert new_instance.time_series_sequence == 4*(2015-1)+2
    assert new_instance.school_year.start_year == 2014


def test_add_school():
    model = School
    create_instance(model, name='School Name')
    new_instance = get_instance(model, name='School Name')
    new_instance.district = 'District Name'
    session.commit()
    assert new_instance.district == 'District Name'


def test_add_student():
    model = Student
    create_instance(model, student_token=12345)
    new_instance = get_instance(model, student_token=12345)
    assert new_instance.student_token == 12345
    assert new_instance.first_name is None


def test_add_student_demographics():
    model = StudentDemographics
    create_instance(model, student_token=12345)
    student = get_instance(Student, student_token=12345)
    new_instance = get_instance(model, student_id=student.id)
    new_instance.gender = 'Orange'
    assert new_instance.gender == 'Orange'
    assert new_instance.student.student_token == 12345


def test_add_student_annual_demographics():
    model = StudentAnnualDemographics
    create_instance(model, student_token=12345, school_year=2018)
    student = get_instance(Student, student_token=12345)
    new_instance = get_instance(model, student_id=student.id)
    new_instance.family_size = 100
    assert new_instance.family_size == 100
    assert new_instance.student.student_token == 12345
    assert new_instance.school_year.school_year == 2018


def test_add_school_attendance():
    model = SchoolAttendance
    create_instance(model, student_token=12345, school_year=2018, marking_period='MP3')
    student = get_instance(Student, student_token=12345)
    school_year = get_instance(SchoolYear, school_year=2018)
    marking_period = get_instance(MarkingPeriod, school_year_id=school_year.id, name='MP3')
    new_instance = get_instance(model, student_id=student.id, marking_period_id=marking_period.id)
    new_instance.days_absent = 100
    assert new_instance.days_absent == 100
    assert new_instance.student.student_token == 12345
    assert new_instance.marking_period.school_year.school_year == 2018
    assert new_instance.marking_period.name == 'MP3'


def test_add_report_card():
    model = ReportCard
    create_instance(model, student_token=12345, school_year=2018, marking_period='MP3', subject='Science')
    student = get_instance(Student, student_token=12345)
    school_year = get_instance(SchoolYear, school_year=2018)
    marking_period = get_instance(MarkingPeriod, school_year_id=school_year.id, name='MP3')
    new_instance = get_instance(model, student_id=student.id, marking_period_id=marking_period.id, subject='Science')
    new_instance.grade_raw = 98
    assert new_instance.grade_raw == 98
    assert new_instance.student.student_token == 12345
    assert new_instance.marking_period.school_year.school_year == 2018
    assert new_instance.marking_period.name == 'MP3'
    assert new_instance.subject == 'Science'


def test_add_student_annual_peter_paul_summary():
    model = StudentAnnualPeterPaulSummary
    create_instance(model, student_token=54321, school_year=2010)
    student = get_instance(Student, student_token=54321)
    school_year = get_instance(SchoolYear, school_year=2010)
    new_instance = get_instance(model, student_id=student.id, school_year_id=school_year.id)
    new_instance.attended_peter_paul_during_school_year = False
    new_instance.test_percentile_in_reading = 80
    assert new_instance.attended_peter_paul_during_school_year is False
    assert new_instance.test_percentile_in_reading == 80
    assert new_instance.student.student_token == 54321
    assert new_instance.school_year.school_year == 2010


def test_add_peter_paul_location():
    model = PeterPaulLocation
    create_instance(model, name='Peter Paul (and Mary)')
    new_instance = get_instance(model, name='Peter Paul (and Mary)')
    session.commit()
    assert new_instance.name == 'Peter Paul (and Mary)'

