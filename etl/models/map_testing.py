from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, Date, Float, DateTime, Enum
from etl.models import Base


class MAPStudent(Base):
    """Model for MAP test students

    todo: combine into a consolidated student model
    """
    __tablename__ = 'map_student'

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer)

    first_name = Column(String)
    last_name = Column(String)
    middle_initial = Column(String)
    date_of_birth = Column(Date)
    ethnic_group = Column(String)
    gender = Column(String)


class MAPSchool(Base):
    """Model for MAP test schools

    This should be able to be derived from student.id and map_test.trimester.year
    todo: combine into a consolidated school model
    """
    __tablename__ = 'map_school'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    district = Column(String)


class MAPTest(Base):
    """Model for tracking MAP test results

    The MAP test is given three times a year.
    todo: I should be able to map from student.id and trimester.year to school.id and grade_level
    """
    __tablename__ = 'map_test'

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('map_student.id'))
    trimester_id = Column(Integer, ForeignKey('trimester.id'))  # term
    test_type = Column(String)  # measurement_scale / discipline

    rit_score = Column(Integer)
    rit_score_standard_error = Column(Float)
    rit_score_percentile = Column(Integer)
    percent_correct = Column(Integer)
    accommodation_category = Column(String)
    accommodation = Column(String)


class MAPGrowth(Base):
    """Model for tracking growth in MAP scores from trimester to trimester

    todo: is this annual, or is it 3/yr
    """
    __tablename__ = 'map_growth'

    id = Column(Integer, primary_key=True, autoincrement=True)
    map_test_sitting_id = Column(Integer, ForeignKey('map_test.id'))
    base_trimester_id = Column(Integer, ForeignKey('trimester.id'))
    target_trimester_id = Column(Integer, ForeignKey('trimester.id'))

    projected_growth = Column(Integer)
    observed_growth = Column(Integer)
    observed_growth_standard_error = Column(Float)
    typical_growth = Column(Integer)


class MAPTestGoal(Base):
    """Model to track MAP test goals

    A student will have several of these per MAP test.
    """
    __tablename__ = 'map_test_goal'

    id = Column(Integer, primary_key=True, autoincrement=True)
    map_test_id = Column(Integer, ForeignKey('map_test.id'))

    name = Column(String)
    score = Column(Integer)
    standard_error = Column(Float)
    range_min = Column(Integer)
    range_max = Column(Integer)
    level = Column(String)  # adjective


class MAPProjectedProficiency(Base):
    """Model for tracking projected proficiencies for various studies (ACT and SOL for now)

    Projected proficiencies are captured annually on a file that is sent three times a year.
    Any new value will update the old.

    todo: do these vary between math/reading
    """
    __tablename__ = 'map_projected_proficiency'

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('student.id'))
    year_id = Column(Integer, ForeignKey('year.id'))

    act = Column(Enum('On Track', 'Non on Track'))
    sol = Column(Enum('Advanced', 'Proficient', 'Basic'))
