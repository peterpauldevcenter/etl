import sqlalchemy
import os
from .context import (SchoolYear, Semester, Trimester, MarkingPeriod,
                      School, Student, StudentDemographics, StudentAnnualDemographics,
                      SchoolAttendance, ReportCard,
                      PeterPaulLocation, StudentAnnualPeterPaulSummary,
                      MAPTestGoal, MAPTest, MAPTestGrowth, settings, etl)

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


def test_add_map_test():
    model = MAPTest
    create_instance(model, student_token=42, school_year=2017, trimester='Winter', discipline='Sailing')
    student = get_instance(Student, student_token=42)
    school_year = get_instance(SchoolYear, school_year=2017)
    trimester = get_instance(Trimester, school_year_id=school_year.id, name='Winter')
    new_instance = get_instance(model, student_id=student.id, trimester_id=trimester.id, discipline='Sailing')
    new_instance.rit_score = 4242
    session.commit()
    assert new_instance.rit_score == 4242
    assert new_instance.trimester.school_year.school_year == 2017
    assert new_instance.trimester.name == 'Winter'
    assert new_instance.student.student_token == 42
    assert new_instance.discipline == 'Sailing'


def test_add_map_test_goal():
    model = MAPTestGoal
    create_instance(model, student_token=25, school_year=2005, trimester='Spring',
                    discipline='Sailing', name='Seven Seas')
    student = get_instance(Student, student_token=25)
    school_year = get_instance(SchoolYear, school_year=2005)
    trimester = get_instance(Trimester, school_year_id=school_year.id, name='Spring')
    map_test = get_instance(MAPTest, student_id=student.id, trimester_id=trimester.id, discipline='Sailing')
    new_instance = get_instance(model, map_test_id=map_test.id, name='Seven Seas')
    new_instance.score = 1234
    session.commit()
    assert new_instance.score == 1234
    assert new_instance.map_test.trimester.school_year.school_year == 2005
    assert new_instance.map_test.trimester.name == 'Spring'
    assert new_instance.map_test.student.student_token == 25
    assert new_instance.map_test.discipline == 'Sailing'
    assert new_instance.name == 'Seven Seas'


def test_add_map_test_growth():
    model = MAPTestGrowth
    create_instance(model, student_token=42, discipline='Sailing', school_year=2017,
                    base_trimester='Winter', projected_trimester='Spring')
    student = get_instance(Student, student_token=42)
    school_year = get_instance(SchoolYear, school_year=2017)
    base_trimester = get_instance(Trimester, school_year_id=school_year.id, name='Winter')
    projected_trimester = get_instance(Trimester, school_year_id=school_year.id, name='Spring')
    new_instance = get_instance(model, student_id=student.id, discipline='Sailing',
                                base_trimester_id=base_trimester.id, projected_trimester_id=projected_trimester.id)
    new_instance.projected_growth = 10
    session.commit()
    assert new_instance.projected_growth == 10
    assert new_instance.base_trimester.school_year.school_year == 2017
    assert new_instance.base_trimester.name == 'Winter'
    assert new_instance.projected_trimester.name == 'Spring'
    assert new_instance.student.student_token == 42
    assert new_instance.discipline == 'Sailing'
