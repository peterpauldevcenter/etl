from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, Date, Float, DateTime
from etl.models import Base


class MAPStudent(Base):
    """Model for MAP test students"""
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
    """Model for MAP test schools"""
    __tablename__ = 'map_school'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    district = Column(String)


class MAPTestSitting(Base):
    """Model for MAP Test sittings"""
    __tablename__ = 'map_test_sitting'

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey('map_student.id'))
    school_id = Column(Integer, ForeignKey('map_school.id'))
    term_name = Column(String)
    grade_level = Column(Integer)


class MAPGrowth(Base):
    """Model for tracking growth in MAP scores from trimester to trimester"""
    __tablename__ = 'map_growth'

    id = Column(Integer, primary_key=True, autoincrement=True)
    map_test_sitting_id = Column(Integer, ForeignKey('map_test_sitting.id'))
    base_period_id = Column(Integer, ForeignKey('trimester_observation.id'))
    target_period_id = Column(Integer, ForeignKey('trimester_observation.id'))

    projected_growth = Column(Integer)
    observed_growth = Column(Integer)
    observed_growth_standard_error = Column(Float)
    met_projected_growth = Column(Boolean)
    conditional_growth_index = Column(Float)
    conditional_growth_percentile = Column(Integer)
    typical_growth = Column(Integer)


class MAPGoal(Base):
    """Model to track MAP goals"""
    __tablename__ = 'map_goal'

    id = Column(Integer, primary_key=True, autoincrement=True)
    map_test_sitting_id = Column(Integer, ForeignKey('map_test_sitting.id'))
    name = Column(String)

    rit_score = Column(Integer)
    standard_error = Column(Float)
    range_min = Column(Integer)
    range_max = Column(Integer)
    adjective = Column(String)


class MAPProficiency(Base):
    """Model for tracking proficiencies for various studies"""
    __tablename__ = 'map_proficiency'

    id = Column(Integer, primary_key=True, autoincrement=True)
    map_test_sitting_id = Column(Integer, ForeignKey('map_test_sitting.id'))
    study = Column(String)

    proficiency_level = Column(String)


class RITtoReading(Base):
    """Model for tracking proficiencies for various studies"""
    __tablename__ = 'rit_to_reading'

    id = Column(Integer, primary_key=True, autoincrement=True)
    map_test_sitting_id = Column(Integer, ForeignKey('map_test_sitting.id'))

    score = Column(String)
    min = Column(String)
    max = Column(String)


class MAPTest(Base):
    """Model for tracking proficiencies for various studies"""
    __tablename__ = 'map_test'

    id = Column(Integer, primary_key=True, autoincrement=True)
    map_test_sitting_id = Column(Integer, ForeignKey('map_test_sitting.id'))

    type = Column(String)
    name = Column(String)
    start_datetime = Column(DateTime)
    duration_minutes = Column(Integer)
    rit_score = Column(Integer)
    rit_score_standard_error = Column(Float)
    rit_score_percentile = Column(Integer)
    percent_correct = Column(Integer)
    accommodation_category = Column(String)
    accommodation = Column(String)
    measurement_scale = Column(String)
    discipline = Column(String)


class MAPReferenceData(Base):
    """Model containing reference data for MAP"""
    __tablename__ = 'map_reference_data'

    id = Column(Integer, primary_key=True, autoincrement=True)
    reference_year = Column(Integer)
    trimester = Column(Integer, ForeignKey('trimester.id'))

    wi_selected_ay = Column(Integer)
    wi_previous_ay = Column(Integer)
