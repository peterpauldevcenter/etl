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


def get_or_create_school_year(school_year: int) -> SchoolYear:
    school_year_obj = session.query(SchoolYear).filter_by(school_year=school_year).first()
    if school_year_obj is None:
        school_year_obj = SchoolYear(school_year=school_year)
        session.add(school_year_obj)
        session.commit()
    return school_year_obj


def get_or_create_marking_period(school_year: SchoolYear, name: str) -> MarkingPeriod:
    marking_period = session.query(MarkingPeriod).filter_by(name=name, school_year_id=school_year.id).first()
    if marking_period is None:
        marking_period = MarkingPeriod(name=name, school_year=school_year.school_year)
        session.add(marking_period)
        session.commit()
    return marking_period


def get_or_create_school_attendance(student: Student, marking_period: MarkingPeriod) -> SchoolAttendance:
    school_attendance = session.query(SchoolAttendance).filter_by(student_id=student.id,
                                                                  marking_period_id=marking_period.id).first()
    if school_attendance is None:
        school_attendance = SchoolAttendance(student_token=student.student_token,
                                             school_year=marking_period.school_year.school_year,
                                             marking_period=marking_period.name)
        session.add(school_attendance)
        session.commit()
    return school_attendance


def get_or_create_report_card(student: Student, marking_period: MarkingPeriod, subject: str) -> ReportCard:
    report_card = session.query(ReportCard).filter_by(student_id=student.id,
                                                      marking_period_id=marking_period.id,
                                                      subject=subject).first()
    if report_card is None:
        report_card = ReportCard(student_token=student.student_token,
                                 school_year=marking_period.school_year.school_year,
                                 marking_period=marking_period.name,
                                 subject=subject)
        session.add(report_card)
        session.commit()
    return report_card


class SchoolAttendanceListView:
    """View to feed Report Card data into the School Attendance model
    """

    model = SchoolAttendance

    def post(self, report_card_file: pathlib.Path):
        df = pandas.read_excel(report_card_file.absolute())
        columns_without_mp = ['MarkelID', 'ABSENT', 'TARDY', 'PRESENT', 'SUSPENDED', 'REASON']
        attendance_mp1 = df[['MarkelID', 'MP1 ABSENT', 'MP1 TARDY', 'MP1 PRESENT', 'MP1 # DAYS DUE TO SUSPENSION', 'REASON']].drop_duplicates()
        attendance_mp1.columns = columns_without_mp
        attendance_mp1['MP'] = 'MP1'
        attendance_mp2 = df[['MarkelID', 'MP2 ABSENT', 'MP2 TARDY', 'MP2 PRESENT', 'MP2 # DAYS DUE TO SUSPENSION', 'REASON.1']].drop_duplicates()
        attendance_mp2.columns = columns_without_mp
        attendance_mp2['MP'] = 'MP2'
        attendance_mp3 = df[['MarkelID', 'MP3 ABSENT', 'MP3 TARDY', 'MP3 PRESENT', 'MP3 # DAYS DUE TO SUSPENSION', 'REASON.2']].drop_duplicates()
        attendance_mp3.columns = columns_without_mp
        attendance_mp3['MP'] = 'MP3'
        attendance_mp4 = df[['MarkelID', 'MP4 ABSENT', 'MP4 TARDY', 'MP4 PRESENT', 'MP4 # DAYS DUE TO SUSPENSION', 'REASON.3']].drop_duplicates()
        attendance_mp4.columns = columns_without_mp
        attendance_mp4['MP'] = 'MP4'
        attendance = attendance_mp1.append(attendance_mp2).append(attendance_mp3).append(attendance_mp4)
        for index, row in attendance.iterrows():
            student_token = row['MarkelID']
            marking_period_name = row['MP']
            days_absent = row['ABSENT']
            days_tardy = row['TARDY']
            days_present = row['PRESENT']
            days_suspended = row['SUSPENDED']
            suspension_reason = row['REASON']

            student = get_or_create_student(student_token=student_token)
            school_year = get_or_create_school_year(2019)
            marking_period = get_or_create_marking_period(school_year, marking_period_name)
            school_attendance = get_or_create_school_attendance(student, marking_period)

            school_attendance.days_absent = days_absent
            school_attendance.days_tardy = days_tardy
            school_attendance.days_present = days_present
            school_attendance.days_suspended = days_suspended
            school_attendance.suspension_reason = suspension_reason
            session.commit()


class ReportCardListView:
    """View to feed Report Card data into the Report Card model

    todo: move grade translation out of the model and into the view, also verify the translation
    todo: pivot a different way, pandas groups by column names, so maybe subject first instead of mp
    """

    model = ReportCard

    def post(self, report_card_file: pathlib.Path):
        df = pandas.read_excel(report_card_file.absolute())
        columns_without_subject = ['MarkelID', 'SUBJECT', 'GRADE']

        subject_0 = df[['MarkelID', 'SUBJECT', 'GRADE MP1']].drop_duplicates()
        subject_1 = df[['MarkelID', 'SUBJECT.1', 'GRADE MP1.1']].drop_duplicates()
        subject_2 = df[['MarkelID', 'SUBJECT.2', 'GRADE MP1.2']].drop_duplicates()
        subject_3 = df[['MarkelID', 'SUBJECT.3', 'GRADE MP1.3']].drop_duplicates()
        subject_4 = df[['MarkelID', 'SUBJECT.4', 'GRADE MP1.4']].drop_duplicates()
        subject_5 = df[['MarkelID', 'SUBJECT.5', 'GRADE MP1.5']].drop_duplicates()
        subject_6 = df[['MarkelID', 'SUBJECT.6', 'GRADE MP1.6']].drop_duplicates()
        subject_7 = df[['MarkelID', 'SUBJECT.7', 'GRADE MP1.7']].drop_duplicates()
        subject_8 = df[['MarkelID', 'SUBJECT.8', 'GRADE MP1.8']].drop_duplicates()
        subject_9 = df[['MarkelID', 'SUBJECT.9', 'GRADE MP1.9']].drop_duplicates()
        subject_mp1 = subject_0.append(subject_1).append(subject_2).append(subject_3).append(subject_4)\
            .append(subject_5).append(subject_6).append(subject_7).append(subject_8).append(subject_9).drop_duplicates()
        subject_mp1.columns = columns_without_subject
        subject_mp1['MP'] = 'MP1'

        subject_0 = df[['MarkelID', 'SUBJECT', 'GRADE MP2']].drop_duplicates()
        subject_1 = df[['MarkelID', 'SUBJECT.1', 'GRADE MP2.1']].drop_duplicates()
        subject_2 = df[['MarkelID', 'SUBJECT.2', 'GRADE MP2.2']].drop_duplicates()
        subject_3 = df[['MarkelID', 'SUBJECT.3', 'GRADE MP2.3']].drop_duplicates()
        subject_4 = df[['MarkelID', 'SUBJECT.4', 'GRADE MP2.4']].drop_duplicates()
        subject_5 = df[['MarkelID', 'SUBJECT.5', 'GRADE MP2.5']].drop_duplicates()
        subject_6 = df[['MarkelID', 'SUBJECT.6', 'GRADE MP2.6']].drop_duplicates()
        subject_7 = df[['MarkelID', 'SUBJECT.7', 'GRADE MP2.7']].drop_duplicates()
        subject_8 = df[['MarkelID', 'SUBJECT.8', 'GRADE MP2.8']].drop_duplicates()
        subject_9 = df[['MarkelID', 'SUBJECT.9', 'GRADE MP2.9']].drop_duplicates()
        subject_mp2 = subject_0.append(subject_1).append(subject_2).append(subject_3).append(subject_4)\
            .append(subject_5).append(subject_6).append(subject_7).append(subject_8).append(subject_9).drop_duplicates()
        subject_mp2.columns = columns_without_subject
        subject_mp2['MP'] = 'MP2'

        subject_0 = df[['MarkelID', 'SUBJECT', 'GRADE MP3']].drop_duplicates()
        subject_1 = df[['MarkelID', 'SUBJECT.1', 'GRADE MP3.1']].drop_duplicates()
        subject_2 = df[['MarkelID', 'SUBJECT.2', 'GRADE MP3.2']].drop_duplicates()
        subject_3 = df[['MarkelID', 'SUBJECT.3', 'GRADE MP3.3']].drop_duplicates()
        subject_4 = df[['MarkelID', 'SUBJECT.4', 'GRADE MP3.4']].drop_duplicates()
        subject_5 = df[['MarkelID', 'SUBJECT.5', 'GRADE MP3.5']].drop_duplicates()
        subject_6 = df[['MarkelID', 'SUBJECT.6', 'GRADE MP3.6']].drop_duplicates()
        subject_7 = df[['MarkelID', 'SUBJECT.7', 'GRADE MP3.7']].drop_duplicates()
        subject_8 = df[['MarkelID', 'SUBJECT.8', 'GRADE MP3.8']].drop_duplicates()
        subject_9 = df[['MarkelID', 'SUBJECT.9', 'GRADE MP3.9']].drop_duplicates()
        subject_mp3 = subject_0.append(subject_1).append(subject_2).append(subject_3).append(subject_4)\
            .append(subject_5).append(subject_6).append(subject_7).append(subject_8).append(subject_9).drop_duplicates()
        subject_mp3.columns = columns_without_subject
        subject_mp3['MP'] = 'MP3'

        subject_0 = df[['MarkelID', 'SUBJECT', 'GRADE MP4']].drop_duplicates()
        subject_1 = df[['MarkelID', 'SUBJECT.1', 'GRADE MP4.1']].drop_duplicates()
        subject_2 = df[['MarkelID', 'SUBJECT.2', 'GRADE MP4.2']].drop_duplicates()
        subject_3 = df[['MarkelID', 'SUBJECT.3', 'GRADE MP4.3']].drop_duplicates()
        subject_4 = df[['MarkelID', 'SUBJECT.4', 'GRADE MP4.4']].drop_duplicates()
        subject_5 = df[['MarkelID', 'SUBJECT.5', 'GRADE MP4.5']].drop_duplicates()
        subject_6 = df[['MarkelID', 'SUBJECT.6', 'GRADE MP4.6']].drop_duplicates()
        subject_7 = df[['MarkelID', 'SUBJECT.7', 'GRADE MP4.7']].drop_duplicates()
        subject_8 = df[['MarkelID', 'SUBJECT.8', 'GRADE MP4.8']].drop_duplicates()
        subject_9 = df[['MarkelID', 'SUBJECT.9', 'GRADE MP4.9']].drop_duplicates()
        subject_mp4 = subject_0.append(subject_1).append(subject_2).append(subject_3).append(subject_4)\
            .append(subject_5).append(subject_6).append(subject_7).append(subject_8).append(subject_9).drop_duplicates()
        subject_mp4.columns = columns_without_subject
        subject_mp4['MP'] = 'MP4'

        subjects = subject_mp1.append(subject_mp2).append(subject_mp3).append(subject_mp4)
        for index, row in subjects.iterrows():
            student_token = row['MarkelID']
            marking_period_name = row['MP']
            subject = row['SUBJECT']
            grade_raw = row['GRADE']

            student = get_or_create_student(student_token=student_token)
            school_year = get_or_create_school_year(2019)
            marking_period = get_or_create_marking_period(school_year, marking_period_name)
            report_card = get_or_create_report_card(student, marking_period, subject)

            report_card.grade_raw = grade_raw
            if grade_raw in ['A', 'B', 'C', 'D', 'F', 'P']:
                report_card.grade_letter = grade_raw
                grades = {'A': 90, 'B': 80, 'C': 70, 'D': 60, 'F': 50, 'P': 70}
                report_card.grade_number = grades[grade_raw]
            else:
                report_card.grade_number = grade_raw
                if grade_raw >= 90:
                    report_card.grade_letter = 'A'
                elif grade_raw >= 80:
                    report_card.grade_letter = 'B'
                elif grade_raw >= 70:
                    report_card.grade_letter = 'C'
                elif grade_raw >= 60:
                    report_card.grade_letter = 'D'
                elif grade_raw >= 0:
                    report_card.grade_letter = 'F'
                else:
                    pass
            session.commit()
