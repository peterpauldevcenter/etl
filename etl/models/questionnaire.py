"""Describes a Survey of Academic Youth Outcomes (SAYO) Questionnaire.

A questionnaire is given during the Fall and Spring of each school year.
The questions and sections are on a semi-Likert scale, only 1-4.

The component sections roll up to the questionnaire.

.. warning::

    During ETL two questions need to be reversed so the semi-Likert section averages
    compute properly. ie. 4 becomes 1, 3 becomes 2, etc

    - EnjoymentEngagementScale.feel_bored
    - SupportiveSocialEnvironmentScale.does_unwanted_teasing
"""
from sqlalchemy import Column, Integer, ForeignKey, Enum
from etl.models import Base


class SupportiveSocialEnvironmentScale(Base):
    __tablename__ = 'student_experience_questionnaire_social_scale'

    id = Column(Integer, primary_key=True, autoincrement='auto')
    questionnaire_id = Column(Integer, ForeignKey('student_experience_questionnaire.id'))
    kids_friendly_with_each_other = Column(Integer)
    does_unwanted_teasing = Column(Integer)
    kids_treat_each_other_respect = Column(Integer)
    have_good_friends = Column(Integer)
    other_kids_help = Column(Integer)
    other_kids_listen_to_you = Column(Integer)


class EnjoymentEngagementScale(Base):
    __tablename__ = 'student_experience_questionnaire_enjoyment_scale'

    id = Column(Integer, primary_key=True, autoincrement='auto')
    questionnaire_id = Column(Integer, ForeignKey('student_experience_questionnaire.id'))
    you_like_coming_here = Column(Integer)
    have_fun_here = Column(Integer)
    feel_bored = Column(Integer)
    find_things_to_do = Column(Integer)


class FeelChallengedScale(Base):
    __tablename__ = 'student_experience_questionnaire_challenge_scale'

    id = Column(Integer, primary_key=True, autoincrement='auto')
    questionnaire_id = Column(Integer, ForeignKey('student_experience_questionnaire.id'))
    learn_new_things = Column(Integer)
    feel_challenged = Column(Integer)
    do_new_things = Column(Integer)


class SupportiveAdultScale(Base):
    __tablename__ = 'student_experience_questionnaire_supportive_adult_scale'

    id = Column(Integer, primary_key=True, autoincrement='auto')
    questionnaire_id = Column(Integer, ForeignKey('student_experience_questionnaire.id'))
    adult_interested_in_think = Column(Integer)
    adult_can_talk_when_upset = Column(Integer)
    adult_helps_with_problems = Column(Integer)
    adult_you_respect = Column(Integer)


class ReaderScale(Base):
    __tablename__ = 'student_experience_questionnaire_reader_scale'

    id = Column(Integer, primary_key=True, autoincrement='auto')
    questionnaire_id = Column(Integer, ForeignKey('student_experience_questionnaire.id'))
    like_to_read_at_home = Column(Integer)
    like_to_read_at_school = Column(Integer)
    like_to_read_after_school_program = Column(Integer)
    good_at_reading = Column(Integer)
    like_to_give_new_books_try = Column(Integer)


class MathScale(Base):
    """All scales are 1-4"""
    __tablename__ = 'student_experience_questionnaire_math_scale'

    id = Column(Integer, primary_key=True, autoincrement='auto')
    questionnaire_id = Column(Integer, ForeignKey('student_experience_questionnaire.id'))
    like_to_learn_new_math = Column(Integer)
    like_to_do_math_at_school = Column(Integer)
    like_to_do_math_at_after_school_program = Column(Integer)
    math_is_something_good_at = Column(Integer)
    interested_in_math = Column(Integer)
    like_to_try_new_math_problems = Column(Integer)


class RetrospectiveQuestionnaire(Base):
    """Restrospective questions are independent, only for subjective analysis
    They are not used to create a scaled rating. Only asked on Spring survey.
    Fall survey will have nulls.

    todo: Figure out nullables in sqlalchemy
    """
    __tablename__ = 'student_experience_questionnaire_retrospective'

    id = Column(Integer, primary_key=True, autoincrement='auto')
    questionnaire_id = Column(Integer, ForeignKey('student_experience_questionnaire.id'))
    coming_to_this_program_helped_read_more_often = Column(Integer)
    coming_helped_math = Column(Integer)
    coming_helped_homework = Column(Integer)
    coming_helped_try_harder_in_school = Column(Integer)
    coming_helped_do_better_in_school = Column(Integer)
    # The below features only apply to middle school students and should only be averaged
    be_successful_in_high_school = Column(Integer)
    graduated_from_high_school = Column(Integer)
    go_to_college = Column(Integer)


class StudentExperienceQuestionnaire(Base):
    """Model for the student questionnaire, taken once in the Fall and again in the Spring.

    todo: Group questions
    """
    __tablename__ = 'student_experience_questionnaire'

    id = Column(Integer, primary_key=True, autoincrement='auto')
    student_id = Column(Integer, ForeignKey('student_roster.id'))
    time_series_id = Column(Integer, ForeignKey('biannual_observation.id'))
