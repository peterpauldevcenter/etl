import pathlib
import pandas
from etl.models.report_card import ReportCard, SchoolAttendance
from etl.models.student_demographics import Student
from etl.models.timeseries import MarkingPeriod, SchoolYear
from etl import utils, session


def get_or_create_student(student_token: int) -> Student:
    student = session.query(Student).filter_by(student_token=student_token).first()
    if student is None:
        student = Student(student_token=student_token)
        session.add(student)
        session.commit()
    return student


def get_or_create_marking_period(school_year: SchoolYear, name: str) -> MarkingPeriod:
    marking_period = session.query(MarkingPeriod).filter_by(name=name, school_year_id=school_year.id).first()
    if marking_period is None:
        marking_period = MarkingPeriod(name=name, school_year=school_year.school_year)
        session.add(marking_period)
        session.commit()
    return marking_period


class SchoolAttendanceListView:

    model = SchoolAttendance

    def post(self, report_card_file: pathlib.Path):
        df = pandas.read_excel(report_card_file.absolute())
        schools = df[['SchoolName', 'DistrictName']].drop_duplicates()
        for index, row in schools.iterrows():
            school_name = row['SchoolName']
            district_name = row['DistrictName']
            school = utils.get_or_create(self.model, name=school_name)
            if district_name is not None:
                school.district = district_name
            session.commit()

