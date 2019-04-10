import pathlib
import pandas
from etl.models.student_demographics import School, Student, StudentDemographics, StudentAnnualDemographics
from etl.models.timeseries import SchoolYear
from etl import utils, session


def get_or_create_school(name: str) -> School:
    school = session.query(School).filter_by(name=name).first()
    if school is None:
        school = School(name=name)
        session.add(school)
        session.commit()
    return school


def get_or_create_school_year(year: int) -> SchoolYear:
    school_year = session.query(SchoolYear).filter_by(school_year=year).first()
    if school_year is None:
        school_year = SchoolYear(school_year=year)
        session.add(school_year)
        session.commit()
    return school_year


def get_or_create_student(student_token: int) -> Student:
    student = session.query(Student).filter_by(student_token=student_token).first()
    if student is None:
        student = Student(student_token=student_token)
        session.add(student)
        session.commit()
    return student


def get_or_create_student_demographics(student: Student) -> StudentDemographics:
    student_demographics = session.query(StudentDemographics).filter_by(student_id=student.id).first()
    if student_demographics is None:
        student_demographics = StudentDemographics(student_token=student.student_token)
        session.add(student_demographics)
        session.commit()
    return student_demographics


def get_or_create_student_annual_demographics(student: Student, school_year: SchoolYear) -> StudentAnnualDemographics:
    student_annual_demographics = session.query(StudentAnnualDemographics).\
        filter_by(student_id=student.id, school_year_id=school_year.id).first()
    if student_annual_demographics is None:
        student_annual_demographics = StudentAnnualDemographics(student_token=student.student_token,
                                                                school_year=school_year.school_year)
        session.add(student_annual_demographics)
        session.commit()
    return student_annual_demographics


class SchoolListView:

    model = School

    def post(self, map_test_file: pathlib.Path):
        df = pandas.read_excel(map_test_file.absolute())
        schools = df[['SchoolName', 'DistrictName']].drop_duplicates()
        for index, row in schools.iterrows():
            school_name = row['SchoolName']
            district_name = row['DistrictName']
            school = utils.get_or_create(self.model, name=school_name)
            if district_name is not None:
                school.district = district_name
            session.commit()


class StudentListView:

    model = Student

    def post(self, student_roster_file: pathlib.Path):
        df = pandas.read_excel(student_roster_file.absolute())
        students = df[['MarkelID']].drop_duplicates()
        for index, row in students.iterrows():
            student_token = int(row['MarkelID'])
            student = get_or_create_student(student_token)
            session.commit()


class StudentDemographicsListView:

    model = StudentDemographics

    def post(self, file: pathlib.Path, file_type: str):
        df = pandas.read_excel(file.absolute())
        if file_type == 'MAP':
            self._process_map_file(df)
        elif file_type == 'Demographics':
            self._process_demographics_file(df)
        elif file_type == 'Roster':
            self._process_roster_file(df)
        else:
            pass

    @staticmethod
    def _process_map_file(df: pandas.DataFrame):
        students = df[['MarkelID', 'StudentEthnicGroup', 'StudentGender']].drop_duplicates()
        for index, row in students.iterrows():
            student_token = int(row['MarkelID'])
            ethnic_group = row['StudentEthnicGroup']
            gender = row['StudentGender']
            student = get_or_create_student(student_token)
            student_demographics = get_or_create_student_demographics(student)
            student_demographics.ethnic_group = ethnic_group
            student_demographics.gender = gender
            session.commit()

    @staticmethod
    def _process_demographics_file(df: pandas.DataFrame):
        students = df[['MarkelID', 'Gender', 'Birth Year', 'Race']].drop_duplicates()
        for index, row in students.iterrows():
            student_token = int(row['MarkelID'])
            gender = row['Gender'][0]
            year_of_birth = int(row['Birth Year'])
            race = row['Race']
            student = get_or_create_student(student_token)
            student_demographics = get_or_create_student_demographics(student)
            student_demographics.gender = gender
            student_demographics.year_of_birth = year_of_birth
            student_demographics.race = race
            session.commit()

    @staticmethod
    def _process_roster_file(df: pandas.DataFrame):
        students = df[['MarkelID', 'Initial PDCC Enrollment Date']].drop_duplicates()
        for index, row in students.iterrows():
            student_token = int(row['MarkelID'])
            peter_paul_enrollment_date = row['Initial PDCC Enrollment Date']
            student = get_or_create_student(student_token)
            student_demographics = get_or_create_student_demographics(student)
            student_demographics.peter_paul_enrollment_date = peter_paul_enrollment_date
            session.commit()


class StudentAnnualDemographicsListView:

    model = StudentAnnualDemographics

    def post(self, file: pathlib.Path, file_type: str):
        df = pandas.read_excel(file.absolute())
        if file_type == 'Demographics':
            self._process_demographics_file(df)
        elif file_type == 'Report Card':
            self._process_report_card_file(df)
        else:
            pass

    @staticmethod
    def _process_demographics_file(df: pandas.DataFrame):
        students = df[['MarkelID', 'FamilySize', 'HouseholdType', 'FamilySetting', 'IncomeCategory', 'Disability',
                       'StudentPFN [PFN Student]']].drop_duplicates()
        for index, row in students.iterrows():
            student_token = int(row['MarkelID'])
            family_size = row['FamilySize']
            household_type = row['HouseholdType']
            family_setting = row['FamilySetting']
            income_category = row['IncomeCategory']
            disability = row['Disability']
            if disability == 'Yes':
                disability = True
            elif disability == 'None':
                disability = False
            promise_family_network = row['StudentPFN [PFN Student]']

            student = get_or_create_student(student_token)
            school_year = get_or_create_school_year(2019)
            student_annual_demographics = get_or_create_student_annual_demographics(student, school_year)

            student_annual_demographics.family_size = family_size
            student_annual_demographics.household_type = household_type
            student_annual_demographics.family_setting = family_setting
            student_annual_demographics.income_category = income_category
            student_annual_demographics.disability = disability
            student_annual_demographics.promise_family_network = promise_family_network
            session.commit()

    @staticmethod
    def _process_report_card_file(df: pandas.DataFrame):
        students = df[['MarkelID', 'SCHOOL', 'CURRENT GRADE', 'PROMOTED', 'IEP']].drop_duplicates()
        for index, row in students.iterrows():
            student_token = int(row['MarkelID'])
            school_name = row['SCHOOL']
            grade_level = row['CURRENT GRADE'].replace('st', '').replace('nd', '').replace('rd', '').replace('th', '')
            promoted = row['PROMOTED']
            if promoted == 'Y':
                promoted = True
            else:
                promoted = False
            individualized_education_plan_indicator = row['IEP']
            if individualized_education_plan_indicator == 'Y':
                individualized_education_plan_indicator = True
            else:
                individualized_education_plan_indicator = False

            student = get_or_create_student(student_token)
            school_year = get_or_create_school_year(2019)
            school = get_or_create_school(school_name)
            student_annual_demographics = get_or_create_student_annual_demographics(student, school_year)

            student_annual_demographics.school = school
            student_annual_demographics.grade_level = grade_level
            student_annual_demographics.promoted = promoted
            student_annual_demographics.individualized_education_plan_indicator = individualized_education_plan_indicator
            session.commit()
