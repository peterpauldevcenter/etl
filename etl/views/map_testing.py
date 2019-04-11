import pathlib
import pandas
from etl.models.map_testing import MAPTest, MAPTestGoal
from etl.models.student_demographics import Student
from etl.models.timeseries import SchoolYear, Trimester
from etl import session


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


def get_or_create_trimester(school_year: SchoolYear, name: str) -> Trimester:
    trimester = session.query(Trimester).filter_by(name=name, school_year_id=school_year.id).first()
    if trimester is None:
        trimester = Trimester(name=name, school_year=school_year.school_year)
        session.add(trimester)
        session.commit()
    return trimester


def get_or_create_map_test(student: Student, trimester: Trimester, discipline: str) -> MAPTest:
    map_test = session.query(MAPTest).filter_by(student_id=student.id, trimester_id=trimester.id,
                                                discipline=discipline).first()
    if map_test is None:
        map_test = MAPTest(student_token=student.student_token, school_year=trimester.school_year.school_year,
                           trimester=trimester.name, discipline=discipline)
        session.add(map_test)
        session.commit()
    return map_test


def get_or_create_map_test_goal(map_test: MAPTest, name: str) -> MAPTestGoal:
    map_test_goal = session.query(MAPTestGoal).filter_by(map_test_id=map_test.id, name=name).first()
    if map_test_goal is None:
        map_test_goal = MAPTestGoal(student_token=map_test.student.student_token,
                                    school_year=map_test.trimester.school_year.school_year,
                                    trimester=map_test.trimester.name,
                                    discipline=map_test.discipline,
                                    name=name)
        session.add(map_test_goal)
        session.commit()
    return map_test_goal


class MAPTestListView:
    """View to feed MAP Test data into the MAP Test model"""

    model = MAPTest

    def post(self, map_test_file: pathlib.Path):
        df = pandas.read_excel(map_test_file.absolute())
        map_tests = df[['MarkelID', 'TermName', 'Discipline', 'TestRITScore', 'TestStandardError', 'TestPercentile',
                        'PercentCorrect', 'AccommodationCategory', 'Accommodations', 'ProjectedProficiencyLevel1',
                        'ProjectedProficiencyLevel2']].drop_duplicates()
        for index, row in map_tests.iterrows():
            student_token = int(row['MarkelID'])
            term = row['TermName']
            discipline = row['Discipline']
            rit_score = row['TestRITScore']
            rit_score_standard_error = row['TestStandardError']
            rit_score_percentile = row['TestPercentile']
            percent_correct = row['PercentCorrect']
            accommodation_category = row['AccommodationCategory']
            accommodation = row['Accommodations']
            act_projected_proficiency = row['ProjectedProficiencyLevel1']
            sol_projected_proficiency = row['ProjectedProficiencyLevel2']

            student = get_or_create_student(student_token)
            year = term[-4:]
            school_year = get_or_create_school_year(year)
            trimester_name = term.split(' ')[0]
            trimester = get_or_create_trimester(school_year, trimester_name)
            map_test = get_or_create_map_test(student, trimester, discipline)

            map_test.rit_score = rit_score
            map_test.rit_score_standard_error = rit_score_standard_error
            map_test.rit_score_percentile = rit_score_percentile
            map_test.percent_correct = percent_correct
            map_test.accommodation_category = accommodation_category
            map_test.accommodation = accommodation
            map_test.act_projected_proficiency = act_projected_proficiency
            map_test.sol_projected_proficiency = sol_projected_proficiency
            session.commit()


class MAPTestGoalListView:
    """View to feed MAP Test data into the MAP Test Goal model"""

    model = MAPTestGoal

    def post(self, map_test_file: pathlib.Path):
        df = pandas.read_excel(map_test_file.absolute())
        map_test_goal_1 = self._get_goal(df, '1')
        map_test_goal_2 = self._get_goal(df, '2')
        map_test_goal_3 = self._get_goal(df, '3')
        map_test_goal_4 = self._get_goal(df, '4')
        map_test_goal_5 = self._get_goal(df, '5')
        map_test_goal_6 = self._get_goal(df, '6')
        map_test_goal_7 = self._get_goal(df, '7')
        map_test_goal_8 = self._get_goal(df, '8')
        map_test_goals = pandas.concat([map_test_goal_1, map_test_goal_2, map_test_goal_3, map_test_goal_4,
                                        map_test_goal_5, map_test_goal_6, map_test_goal_7, map_test_goal_8])
        for index, row in map_test_goals.iterrows():
            student_token = int(row['MarkelID'])
            term = row['TermName']
            discipline = row['Discipline']
            name = row['name']
            score = row['score']
            standard_error = row['standard_error']
            range = row['range']
            level = row['level']

            student = get_or_create_student(student_token)
            year = term[-4:]
            school_year = get_or_create_school_year(year)
            trimester_name = term.split(' ')[0]
            trimester = get_or_create_trimester(school_year, trimester_name)
            map_test = get_or_create_map_test(student, trimester, discipline)
            map_test_goal = get_or_create_map_test_goal(map_test, name)

            map_test_goal.score = score
            map_test_goal.standard_error = standard_error
            map_test_goal.range = range
            map_test_goal.level = level
            session.commit()

    @staticmethod
    def _get_goal(df: pandas.DataFrame, goal: str) -> pandas.DataFrame:
        map_test_goal = df[['MarkelID', 'TermName', 'Discipline',
                            f'Goal{goal}Name',
                            f'Goal{goal}RitScore',
                            f'Goal{goal}StdErr',
                            f'Goal{goal}Range',
                            f'Goal{goal}Adjective']].drop_duplicates()
        map_test_goal.rename(columns={f'Goal{goal}Name': 'name',
                                      f'Goal{goal}RitScore': 'score',
                                      f'Goal{goal}StdErr': 'standard_error',
                                      f'Goal{goal}Range': 'range',
                                      f'Goal{goal}Adjective': 'level'}, inplace=True)
        return map_test_goal
