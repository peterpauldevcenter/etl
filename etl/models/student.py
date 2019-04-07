from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, Enum
from sqlalchemy.orm import relationship
from etl.models import Base


class StudentRoster(Base):
    """Model for static and summary level student features."""
    __tablename__ = 'student_roster'

    id = Column(Integer, primary_key=True, autoincrement='auto')
    initial_enrollment_date = None
    number_of_completed_school_years = None


class StudentTermObservation(Base):
    """Model for Peter Paul term time series student features"""
    __tablename__ = 'student_term_observation'

    growth_eumerated_values = 'any projection exceeded'.split()

    id = Column(Integer, primary_key=True, autoincrement='auto')
    student_id = Column(Integer, ForeignKey('student_roster.id'))
    time_series = Column(Integer, ForeignKey('PeterPaulTerm.id'))
    grade = Column(Integer)
    peter_paul_location = Column(Integer, ForeignKey('PeterPaulLocation.id'))
    attended_peter_paul_for_time_series = Column(Boolean)
    growth_in_reading = Column(Enum(growth_eumerated_values))
    test_percentile_in_reading = Column(Integer)
    met_national_norm_in_reading = Column(Boolean)
    growth_in_math = Column(Enum(growth_eumerated_values))
    test_percentile_in_math = Column(Integer)
    met_national_norm_in_math = Column(Boolean)


class StudentExperienceQuestionnaire(Base):
    __tablename__ = 'student_experience_questionnaire'

    id = Column(Integer, primary_key=True, autoincrement='auto')
    student_id = Column(Integer, ForeignKey('student_roster.id'))
    time_series_id = Column(Integer, ForeignKey('BiannualObservation.id'))
    kids_friendly_with_each_other = Column(Integer)
    does_unwanted_teasing = Column(Integer)
    kids_treat_each_other_respect = Column(Integer)
    have_good_friends = Column(Integer)
    other_kids_help = Column(Integer)
    other_kids_listen_to_you = Column(Integer)
    you_like_coming_here = Column(Integer)
    have_fun_here = Column(Integer)
    feel_bored = Column(Integer)
    find_things_to_do = Column(Integer)
    learn_new_things = Column(Integer)
    feel_challenged = Column(Integer)
    do_new_things = Column(Integer)
    adult_interested_in_think = Column(Integer)
    adult_can_talk_when_upset = Column(Integer)
    adult_helps_with_problems = Column(Integer)
    adult_you_respect = Column(Integer)
    like_to_read_at_home = Column(Integer)
    like_to_read_at_school = Column(Integer)
    like_to_read_after_school_program = Column(Integer)
    good_at_reading = Column(Integer)
    like_to_give_new_books_try = Column(Integer)
    coming_to_this_program_helped_read_more_often = Column(Integer)
    like_to_learn_new_math = Column(Integer)
    like_to_do_math_at_school = Column(Integer)
    like_to_do_math_at_after_school_program = Column(Integer)
    math_is_something_good_at = Column(Integer)
    interested_in_math = Column(Integer)
    like_to_try_new_math_programs = Column(Integer)
    coming_helped_math = Column(Integer)
    coming_helped_homework = Column(Integer)
    coming_helped_try_harder_in_school = Column(Integer)
    coming_helped_do_better_in_school = Column(Integer)
    be_successful_in_high_school = Column(Integer)
    graduated_from_high_school = Column(Integer)
    go_to_college = Column(Integer)


class StudentYearTimeSeries(Base):
    """Model for year based student features."""
    __tablename__ = 'student_year_time_series'

    id = Column(Integer, primary_key=True, autoincrement='auto')
    student_id = Column(Integer, ForeignKey('student_roster.id'))
    year = Column(Integer, ForeignKey('year.id'), unique=True)
    grade_promotion = Column(Boolean)
    school_missed_for_suspension = Column(Boolean)
    reading_sol_passed = Column(Boolean)
    math_sol_passed = Column(Boolean)


class StudentObservation(Base):
    __tablename__ = 'student_roster_observation'

    id = Column(Integer, primary_key=True, autoincrement='auto')
    student_id = Column(Integer, ForeignKey('StudentRoster.id'))
    peter_paul_term_id = Column(Integer, ForeignKey('PeterPaulTerm.id'))
    # ToDO: Define enum?
    description_reading = Column(String)
    description_math = Column(String)

