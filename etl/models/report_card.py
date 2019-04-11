"""Report card data and school attendance data from Richmond Public Schools"""
from sqlalchemy import Column, String, Integer, Float, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from etl.models import Base
from etl.models.timeseries import SchoolYear, MarkingPeriod
from etl.models.student_demographics import Student
from etl import session


def get_or_create_school_year(school_year: int) -> SchoolYear:
    school_year_obj = session.query(SchoolYear).filter_by(school_year=school_year).first()
    if school_year_obj is None:
        school_year_obj = SchoolYear(school_year=school_year)
        session.add(school_year_obj)
        session.commit()
    return school_year_obj


def get_or_create_marking_period(school_year: SchoolYear, name: str) -> MarkingPeriod:
    marking_period = session.query(MarkingPeriod).filter_by(school_year_id=school_year.id, name=name).first()
    if marking_period is None:
        marking_period = MarkingPeriod(school_year=school_year.school_year, name=name)
        session.add(marking_period)
        session.commit()
    return marking_period


def get_or_create_student(student_token: int) -> Student:
    student = session.query(Student).filter_by(student_token=student_token).first()
    if student is None:
        student = Student(student_token=student_token)
        session.add(student)
        session.commit()
    return student


class SchoolAttendance(Base):
    """Model for tracking school attendance by marking period

    Source: Report Card
    """
    __tablename__ = 'school_attendance'
    __table_args__ = (UniqueConstraint('student_id', 'marking_period_id', name='uc__student__marking_period'),)

    id = Column(Integer, primary_key=True, autoincrement='auto')
    student_id = Column(Integer, ForeignKey('student.id'))
    student = relationship('Student', back_populates='school_attendance')
    marking_period_id = Column(Integer, ForeignKey('marking_period.id'))
    marking_period = relationship('MarkingPeriod', back_populates='school_attendance')

    days_absent = Column(Integer)
    days_tardy = Column(Integer)
    days_present = Column(Integer)
    days_suspended = Column(Integer)
    suspension_reason = Column(String)

    def __init__(self, student_token: int, school_year: int, marking_period: str):
        self.student = get_or_create_student(student_token)
        school_year_obj = get_or_create_school_year(school_year=school_year)
        self.marking_period = get_or_create_marking_period(school_year_obj, marking_period)


class ReportCard(Base):
    """Model to report grades by course for each marking period

    Source: Report Card
    """
    __tablename__ = 'report_card'
    __table_args__ = (UniqueConstraint('student_id', 'marking_period_id', 'subject',
                                       name='uc__student__marking_period__subject'),)

    id = Column(Integer, primary_key=True, autoincrement='auto')
    student_id = Column(Integer, ForeignKey('student.id'))
    student = relationship('Student', back_populates='report_cards')
    marking_period_id = Column(Integer, ForeignKey('marking_period.id'))
    marking_period = relationship('MarkingPeriod', back_populates='report_cards')
    subject = Column(String)

    grade_raw = Column(String)
    grade_letter = Column(String)
    grade_number = Column(Float)

    def __init__(self, student_token: int, school_year: int, marking_period: str, subject: str):
        self.student = get_or_create_student(student_token)
        school_year_obj = get_or_create_school_year(school_year=school_year)
        self.marking_period = get_or_create_marking_period(school_year_obj, marking_period)
        self.subject = subject
