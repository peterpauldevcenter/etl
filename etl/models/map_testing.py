"""Records MAP Test results, goals, and growth projections.

The MAP Test is given three times per year, during the Fall, Winter, and Spring of each school year.
"""
from sqlalchemy import Column, String, Integer, ForeignKey, Float, Enum
from etl.models import Base


class MAPTest(Base):
    """Model for tracking MAP test results

    Source: MAP Test
    """
    __tablename__ = 'map_test'

    id = Column(Integer, primary_key=True, autoincrement='auto')
    student_id = Column(Integer, ForeignKey('student.id'))
    trimester_id = Column(Integer, ForeignKey('trimester.id'))  # term
    discipline = Column(String)

    rit_score = Column(Integer)
    rit_score_standard_error = Column(Float)
    rit_score_percentile = Column(Integer)
    percent_correct = Column(Integer)
    accommodation_category = Column(String)
    accommodation = Column(String)
    act_projected_proficiency = Column(String)
    sol_projected_proficiency = Column(String)


class MAPTestGrowth(Base):
    """Model for tracking growth in MAP scores from trimester to trimester

    Source: MAP Test

    Actual values and projected values are collected three times a year so that projected values can be measured:
    At fall, fall to winter and fall to spring are captured as projections
    At winter, fall to winter is captured as an actual and winter to spring is captured as a projection
    """
    __tablename__ = 'map_test_growth'

    id = Column(Integer, primary_key=True, autoincrement='auto')
    map_test_id = Column(Integer, ForeignKey('map_test.id'))
    base_trimester_id = Column(Integer, ForeignKey('trimester.id'))
    projected_trimester_id = Column(Integer, ForeignKey('trimester.id'))

    projected_growth = Column(Integer)
    observed_growth = Column(Integer)
    observed_growth_standard_error = Column(Float)
    typical_growth = Column(Integer)


class MAPTestGoal(Base):
    """Model to track MAP test goals

    Source: MAP Test

    A student will have several of these per MAP test.
    """
    __tablename__ = 'map_test_goal'

    id = Column(Integer, primary_key=True, autoincrement='auto')
    map_test_id = Column(Integer, ForeignKey('map_test.id'))

    name = Column(String)
    score = Column(Integer)
    standard_error = Column(Float)
    range_min = Column(Integer)
    range_max = Column(Integer)
    level = Column(String)  # adjective
