"""Records MAP Test results, goals, and growth projections.

The MAP Test is given three times per year, during the Fall, Winter, and Spring of each school year.
There is a Mathematics component, and a Reading component, as noted by the discipline.
Goals and projections are produced for each component each trimester.
Projections are validated against actuals as new scores are collected.
"""
from sqlalchemy import Column, String, Integer, ForeignKey, Float, UniqueConstraint
from sqlalchemy.orm import relationship
from etl.models import Base
from etl.models.student_demographics import Student
from etl.models.timeseries import SchoolYear, Trimester
from etl import session


class MAPTest(Base):
    """Model for tracking MAP test results by discipline

    Source: MAP Test
    """
    __tablename__ = 'map_test'
    __table_args__ = (UniqueConstraint('student_id', 'trimester_id', 'discipline',
                                       name='uc__student__trimester__discipline'),)

    id = Column(Integer, primary_key=True, autoincrement='auto')
    student_id = Column(Integer, ForeignKey('student.id'))
    student = relationship('Student', back_populates='map_tests')
    trimester_id = Column(Integer, ForeignKey('trimester.id'))  # term
    trimester = relationship('Trimester', back_populates='map_tests')
    discipline = Column(String)

    rit_score = Column(Integer)
    rit_score_standard_error = Column(Float)
    rit_score_percentile = Column(Integer)
    percent_correct = Column(Integer)
    accommodation_category = Column(String)
    accommodation = Column(String)
    act_projected_proficiency = Column(String)
    sol_projected_proficiency = Column(String)
    map_test_goals = relationship('MAPTestGoal')

    def __init__(self, student_token: int, school_year: int, trimester: str, discipline: str):
        student = session.query(Student).filter_by(student_token=student_token).first()
        if student is None:
            student = Student(student_token=student_token)
        self.student = student
        school_year_obj = session.query(SchoolYear).filter_by(school_year=school_year).first()
        if school_year_obj is None:
            school_year_obj = SchoolYear(school_year=school_year)
        trimester_obj = session.query(Trimester).filter_by(school_year_id=school_year_obj.id,
                                                           name=trimester).first()
        if trimester_obj is None:
            trimester_obj = Trimester(school_year=school_year_obj.school_year, name=trimester)
        self.trimester = trimester_obj
        self.discipline = discipline


class MAPTestGoal(Base):
    """Model to track MAP test goals

    Source: MAP Test

    A student will have up to ten of these per MAP test.
    """
    __tablename__ = 'map_test_goal'
    __table_args__ = (UniqueConstraint('map_test_id', 'name', name='uc__map_test__name'),)

    id = Column(Integer, primary_key=True, autoincrement='auto')
    map_test_id = Column(Integer, ForeignKey('map_test.id'))
    map_test = relationship('MAPTest', back_populates='map_test_goals')
    name = Column(String)

    score = Column(Integer)
    standard_error = Column(Float)
    range = Column(String)
    level = Column(String)  # adjective

    def __init__(self, student_token: int, school_year: int, trimester: str, discipline: str, name: str):
        student = session.query(Student).filter_by(student_token=student_token).first()
        if student is None:
            student = Student(student_token=student_token)
        school_year_obj = session.query(SchoolYear).filter_by(school_year=school_year).first()
        if school_year_obj is None:
            school_year_obj = SchoolYear(school_year=school_year)
        trimester_obj = session.query(Trimester).filter_by(school_year_id=school_year_obj.id,
                                                           name=trimester).first()
        if trimester_obj is None:
            trimester_obj = Trimester(school_year=school_year_obj.school_year, name=trimester)
        map_test = session.query(MAPTest).filter_by(student_id=student.id,
                                                    trimester_id=trimester_obj.id,
                                                    discipline=discipline).first()
        if map_test is None:
            map_test = MAPTest(student_token=student.student_token,
                               school_year=school_year_obj.school_year,
                               trimester=trimester,
                               discipline=discipline)
        self.map_test = map_test
        self.name = name


class MAPTestGrowth(Base):
    """Model for tracking growth in MAP scores from trimester to trimester

    Source: MAP Test

    .. warning::

        This model is not currently populated

    Actual values and projected values are collected three times a year so that projected values can be measured:
    At fall, fall to winter and fall to spring are captured as projections
    At winter, fall to winter is captured as an actual and winter to spring is captured as a projection
    """
    __tablename__ = 'map_test_growth'
    __table_args__ = (UniqueConstraint('student_id', 'discipline', 'base_trimester_id', 'projected_trimester_id',
                                       name='uc__student__discipline__base_trimester__projected_trimester'),)

    id = Column(Integer, primary_key=True, autoincrement='auto')
    student_id = Column(Integer, ForeignKey('student.id'))
    student = relationship('Student', back_populates='map_test_growth')
    discipline = Column(String)
    base_trimester_id = Column(Integer, ForeignKey('trimester.id'))
    base_trimester = relationship('Trimester', foreign_keys=[base_trimester_id])
    projected_trimester_id = Column(Integer, ForeignKey('trimester.id'))
    projected_trimester = relationship('Trimester', foreign_keys=[projected_trimester_id])

    projected_growth = Column(Integer)
    observed_growth = Column(Integer)
    observed_growth_standard_error = Column(Float)
    typical_growth = Column(Integer)

    def __init__(self, student_token: int, discipline: str, school_year: int, base_trimester: str, projected_trimester: str):
        student = session.query(Student).filter_by(student_token=student_token).first()
        if student is None:
            student = Student(student_token=student_token)
        self.student = student
        self.discipline = discipline

        school_year_obj = session.query(SchoolYear).filter_by(school_year=school_year).first()
        if school_year_obj is None:
            school_year_obj = SchoolYear(school_year=school_year)

        base_trimester_obj = session.query(Trimester).filter_by(school_year_id=school_year_obj.id, name=base_trimester).first()
        if base_trimester_obj is None:
            base_trimester_obj = Trimester(school_year=school_year, name=base_trimester)
        self.base_trimester = base_trimester_obj

        projected_trimester_obj = session.query(Trimester).filter_by(school_year_id=school_year_obj.id, name=projected_trimester).first()
        if projected_trimester_obj is None:
            projected_trimester_obj = Trimester(school_year=school_year, name=projected_trimester)
        self.projected_trimester = projected_trimester_obj
