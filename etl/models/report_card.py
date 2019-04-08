from sqlalchemy import Column, String, Boolean, Integer, Float, ForeignKey
from etl.models import Base


class ReportCardSchool(Base):
    """Model for schools in the Richmond Public School system

    todo: combine into a consolidated school model
    """
    __tablename__ = 'report_card_school'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)


class MarkingPeriod(Base):
    """Model to represent a time series of RPS marking periods

    todo: combine into the time series quarterly model
    """
    __tablename__ = 'marking_period'

    id = Column(Integer, primary_key=True, autoincrement=True)
    school_year = Column(Integer)
    marking_period = Column(Integer)

    time_series_sequence = Column(Integer)
    name = Column(String)


class StudentSchoolYear(Base):
    """Model for the student attributes on the report card dataset

    This should align with other student models from other datasets, and could be incorporated into those models.
    The dataset provides the student's full name, which should be used to get a student_id.
    The dataset provides the school name, which should be used to get a school_id.

    todo: combine with other annual student data, like student_annual_demographics?
    """
    __tablename__ = 'student_school_year'

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('student.id'))
    school_year = Column(Integer)

    school_id = Column(Integer, ForeignKey('school.id'))
    grade_level = Column(Integer)
    promoted = Column(Boolean)


class Attendance(Base):
    """Model for tracking school attendance by marking period

    todo: change foreign key for marking period
    todo: is the iep by subject, or by quarter?
    """
    __tablename__ = 'school_attendance'

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('student.id'))
    marking_period_id = Column(Integer, ForeignKey('marking_period.id'))

    days_absent = Column(Integer)
    days_tardy = Column(Integer)
    days_present = Column(Integer)
    days_suspended = Column(Integer)
    suspension_reason = Column(String)
    individualized_education_plan_indicator = Column(Boolean)


class ReportCard(Base):
    """Model to report grades by course for each marking period

    todo: change foreign key for marking period
    """
    __tablename__ = 'report_card'

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('student.id'))
    marking_period_id = Column(Integer, ForeignKey('marking_period.id'))
    subject = Column(String)

    grade_raw = Column(String)
    grade_letter = Column(String)
    grade_number = Column(Float)
