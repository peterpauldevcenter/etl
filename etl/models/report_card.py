from sqlalchemy import Column, String, Integer, Float, ForeignKey
from etl.models import Base


class SchoolAttendance(Base):
    """Model for tracking school attendance by marking period

    Source: Report Card
    """
    __tablename__ = 'school_attendance'

    id = Column(Integer, primary_key=True, autoincrement='auto')
    student_id = Column(Integer, ForeignKey('student.id'))
    marking_period_id = Column(Integer, ForeignKey('marking_period.id'))

    days_absent = Column(Integer)
    days_tardy = Column(Integer)
    days_present = Column(Integer)
    days_suspended = Column(Integer)
    suspension_reason = Column(String)


class ReportCard(Base):
    """Model to report grades by course for each marking period

    Source: Report Card
    """
    __tablename__ = 'report_card'

    id = Column(Integer, primary_key=True, autoincrement='auto')
    student_id = Column(Integer, ForeignKey('student.id'))
    marking_period_id = Column(Integer, ForeignKey('marking_period.id'))
    subject = Column(String)

    grade_raw = Column(String)
    grade_letter = Column(String)
    grade_number = Column(Float)
