"""This file will build the database from scratch, using the named Excel files lists within this code"""
import pathlib
from etl.models import Base
from etl import engine
from etl.views.map_testing import MAPTestGoalListView, MAPTestListView
from etl.views.peter_paul_roster import StudentAnnualPeterPaulSummaryListView
from etl.views.report_card import SchoolAttendanceListView, ReportCardListView
from etl.views.student_demographics import SchoolListView, StudentListView,\
    StudentDemographicsListView, StudentAnnualDemographicsListView


def build_database():
    data_directory = pathlib.Path(r'\\mklfile\datalake$\Peter Paul Innovation Day\Data Extracts')

    map_test_data = [
        data_directory / pathlib.Path('MAP Testing Data - Spring-Post (before manipulation) with Markel ID.xlsx')
    ]
    peter_paul_roster_data = [
        data_directory / pathlib.Path('Student Roster with Markel IDs Corrected.xlsx')
    ]
    report_card_data = [
        data_directory / pathlib.Path('Report Card Data- 2nd quarter (before manupulation) with MarkelID.xlsx'),
        data_directory / pathlib.Path('Report Card Data- 4th quarter (before manupulation) with MarkelID.xlsx')
    ]
    student_demographics_data = [data_directory / pathlib.Path('Student Demographics with Markel IDs.xlsx')]

    map_test = MAPTestListView()
    map_test_goal = MAPTestGoalListView()
    student_annual_peter_paul_summary = StudentAnnualPeterPaulSummaryListView()
    school_attendance = SchoolAttendanceListView()
    report_card = ReportCardListView()
    school = SchoolListView()
    student = StudentListView()
    student_demographics = StudentDemographicsListView()
    student_annual_demographics = StudentAnnualDemographicsListView()

    Base.metadata.create_all(bind=engine)

    for file in map_test_data:
        print(f'{file.name} is loading')
        map_test.post(file)
        map_test_goal.post(file)
        school.post(file)
        student_demographics.post(file, 'MAP')

    for file in peter_paul_roster_data:
        print(f'{file.name} is loading')
        student_annual_peter_paul_summary.post(file)
        student.post(file)
        student_demographics.post(file, 'Roster')

    for file in report_card_data:
        print(f'{file.name} is loading')
        school_attendance.post(file)
        report_card.post(file)
        student_annual_demographics.post(file, 'Report Card')

    for file in student_demographics_data:
        print(f'{file.name} is loading')
        student_demographics.post(file, 'Demographics')
        student_annual_demographics.post(file, 'Demographics')


if __name__ == '__main__':
    build_database()
