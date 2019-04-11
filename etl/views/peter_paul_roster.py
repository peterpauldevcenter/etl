import pathlib
import pandas
from etl.models.peter_paul_roster import StudentAnnualPeterPaulSummary, PeterPaulLocation
from etl.models.student_demographics import Student
from etl.models.timeseries import SchoolYear
from etl import session


def get_or_create_student(student_token: int) -> Student:
    student = session.query(Student).filter_by(student_token=student_token).first()
    if student is None:
        student = Student(student_token=student_token)
        session.add(student)
        session.commit()
    return student


def get_or_create_peter_paul_location(name: str) -> PeterPaulLocation:
    peter_paul_location = session.query(PeterPaulLocation).filter_by(name=name).first()
    if peter_paul_location is None:
        peter_paul_location = PeterPaulLocation(name=name)
        session.add(peter_paul_location)
        session.commit()
    return peter_paul_location


def get_or_create_school_year(school_year: int) -> SchoolYear:
    school_year_obj = session.query(SchoolYear).filter_by(school_year=school_year).first()
    if school_year_obj is None:
        school_year_obj = SchoolYear(school_year=school_year)
        session.add(school_year_obj)
        session.commit()
    return school_year_obj


def get_or_create_annual_summary(student: Student, school_year: SchoolYear) -> StudentAnnualPeterPaulSummary:
    annual_summary = session.query(StudentAnnualPeterPaulSummary).filter_by(student_id=student.id,
                                                                            school_year_id=school_year.id).first()
    if annual_summary is None:
        annual_summary = StudentAnnualPeterPaulSummary(student_token=student.student_token,
                                                       school_year=school_year.school_year)
        session.add(annual_summary)
        session.commit()
    return annual_summary


class StudentAnnualPeterPaulSummaryListView:
    """View to feed Student Roster data into the Peter Paul Annual Summary model

    This extract pivots years back to a transactional structure and does some light transformation
    to combine things like reading and math growth into one column.
    """

    model = StudentAnnualPeterPaulSummary

    @staticmethod
    def post(student_roster_file: pathlib.Path):
        df = pandas.read_excel(student_roster_file.absolute())

        annual_summary_2019 = df[['MarkelID', 'Peter Paul Location (2019)', 'PPDC 2018-2019', 'Summer Promise 2018']]
        annual_summary_2019.rename(columns={'Peter Paul Location (2019)': 'PETER PAUL LOCATION',
                                            'PPDC 2018-2019': 'PPDC',
                                            'Summer Promise 2018': 'SUMMER PROMISE'}, inplace=True)
        annual_summary_2019['YEAR'] = 2019
        annual_summary_2019['GROWTH READING EXCEED'] = None
        annual_summary_2019['GROWTH READING MET'] = None
        annual_summary_2019['GROWTH READING ANY'] = None
        annual_summary_2019['TEST READING PERCENTILE'] = None
        annual_summary_2019['MET NORM READING'] = None
        annual_summary_2019['GROWTH MATH EXCEED'] = None
        annual_summary_2019['GROWTH MATH MET'] = None
        annual_summary_2019['GROWTH MATH ANY'] = None
        annual_summary_2019['TEST MATH PERCENTILE'] = None
        annual_summary_2019['MET NORM MATH'] = None

        annual_summary_2018 = df[['MarkelID', 'Peter Paul Location (2018)', 'PPDC 2017-2018', 'Summer Promise 2017',
                                  'Exceeded Growth Projection for Reading (Spring-2018)',
                                  'Achieved Growth Projection Reading (Spring-2018)',
                                  'Achieved Any Growth in Reading (Spring-2018)',
                                  'Test Percentile Reading (Spring-2018)',
                                  'Met the National Norm for Reading (Spring-2018)',
                                  'Exceeded Growth Projection for Math (Spring-2018)',
                                  'Achieved Growth Projection Math (Spring-2018)',
                                  'Achieved Any Growth in Math (Spring-2018)',
                                  'Test Percentile Math (Spring-2018)',
                                  'Met the National Norm for Math (Spring-2018)']]
        annual_summary_2018.rename(columns={'Peter Paul Location (2018)': 'PETER PAUL LOCATION',
                                            'PPDC 2017-2018': 'PPDC',
                                            'Summer Promise 2017': 'SUMMER PROMISE',
                                            'Exceeded Growth Projection for Reading (Spring-2018)': 'GROWTH READING EXCEED',
                                            'Achieved Growth Projection Reading (Spring-2018)': 'GROWTH READING MET',
                                            'Achieved Any Growth in Reading (Spring-2018)': 'GROWTH READING ANY',
                                            'Test Percentile Reading (Spring-2018)': 'TEST READING PERCENTILE',
                                            'Met the National Norm for Reading (Spring-2018)': 'MET NORM READING',
                                            'Exceeded Growth Projection for Math (Spring-2018)': 'GROWTH MATH EXCEED',
                                            'Achieved Growth Projection Math (Spring-2018)': 'GROWTH MATH MET',
                                            'Achieved Any Growth in Math (Spring-2018)': 'GROWTH MATH ANY',
                                            'Test Percentile Math (Spring-2018)': 'TEST MATH PERCENTILE',
                                            'Met the National Norm for Math (Spring-2018)': 'MET NORM MATH'}, inplace=True)
        annual_summary_2018['YEAR'] = 2018

        annual_summary_2017 = df[['MarkelID', 'Peter Paul Location (2017)', 'PPDC 2016-2017', 'Summer Promise 2016',
                                  'Exceeded Growth Projection for Reading (Spring-2017)',
                                  'Achieved Growth Projection Reading (Spring-2017)',
                                  'Achieved Any Growth in Reading (Spring-2017)',
                                  'Test Percentile Reading (Spring-2017)',
                                  'Met the National Norm for Reading (Spring-2017)',
                                  'Exceeded Growth Projection for Math (Spring-2017)',
                                  'Achieved Growth Projection Math (Spring-2017)',
                                  'Achieved Any Growth in Math (Spring-2017)',
                                  'Test Percentile Math (Spring-2017)',
                                  'Met the National Norm for Math (Spring-2017)']]
        annual_summary_2017.rename(columns={'Peter Paul Location (2017)': 'PETER PAUL LOCATION',
                                            'PPDC 2016-2017': 'PPDC',
                                            'Summer Promise 2016': 'SUMMER PROMISE',
                                            'Exceeded Growth Projection for Reading (Spring-2017)': 'GROWTH READING EXCEED',
                                            'Achieved Growth Projection Reading (Spring-2017)': 'GROWTH READING MET',
                                            'Achieved Any Growth in Reading (Spring-2017)': 'GROWTH READING ANY',
                                            'Test Percentile Reading (Spring-2017)': 'TEST READING PERCENTILE',
                                            'Met the National Norm for Reading (Spring-2017)': 'MET NORM READING',
                                            'Exceeded Growth Projection for Math (Spring-2017)': 'GROWTH MATH EXCEED',
                                            'Achieved Growth Projection Math (Spring-2017)': 'GROWTH MATH MET',
                                            'Achieved Any Growth in Math (Spring-2017)': 'GROWTH MATH ANY',
                                            'Test Percentile Math (Spring-2017)': 'TEST MATH PERCENTILE',
                                            'Met the National Norm for Math (Spring-2017)': 'MET NORM MATH'}, inplace=True)
        annual_summary_2017['YEAR'] = 2017

        annual_summary_2016 = df[['MarkelID', 'Peter Paul Location (2016)', 'PPDC 2015-2016', 'Summer Promise 2015',
                                  'Exceeded Growth Projection for Reading (Spring-2016)',
                                  'Achieved Growth Projection Reading (Spring-2016)',
                                  'Achieved Any Growth in Reading (Spring-2016)',
                                  'Test Percentile Reading (Spring-2016)',
                                  'Met the National Norm for Reading (Spring-2016)',
                                  'Exceeded Growth Projection for Math (Spring-2016)',
                                  'Achieved Growth Projection Math (Spring-2016)',
                                  'Achieved Any Growth in Math (Spring-2016)',
                                  'Test Percentile Math (Spring-2016)',
                                  'Met the National Norm for Math (Spring-2016)']]
        annual_summary_2016.rename(columns={'Peter Paul Location (2016)': 'PETER PAUL LOCATION',
                                            'PPDC 2015-2016': 'PPDC',
                                            'Summer Promise 2015': 'SUMMER PROMISE',
                                            'Exceeded Growth Projection for Reading (Spring-2016)': 'GROWTH READING EXCEED',
                                            'Achieved Growth Projection Reading (Spring-2016)': 'GROWTH READING MET',
                                            'Achieved Any Growth in Reading (Spring-2016)': 'GROWTH READING ANY',
                                            'Test Percentile Reading (Spring-2016)': 'TEST READING PERCENTILE',
                                            'Met the National Norm for Reading (Spring-2016)': 'MET NORM READING',
                                            'Exceeded Growth Projection for Math (Spring-2016)': 'GROWTH MATH EXCEED',
                                            'Achieved Growth Projection Math (Spring-2016)': 'GROWTH MATH MET',
                                            'Achieved Any Growth in Math (Spring-2016)': 'GROWTH MATH ANY',
                                            'Test Percentile Math (Spring-2016)': 'TEST MATH PERCENTILE',
                                            'Met the National Norm for Math (Spring-2016)': 'MET NORM MATH'}, inplace=True)
        annual_summary_2016['YEAR'] = 2016

        annual_summary_2015 = df[['MarkelID', 'Peter Paul Location (2015)', 'PPDC 2014-2015', 'Summer Promise 2014',
                                  'Exceeded Growth Projection for Reading (Spring-2015)',
                                  'Achieved Growth Projection Reading (Spring-2015)',
                                  'Achieved Any Growth in Reading (Spring-2015)',
                                  'Test Percentile Reading (Spring-2015)',
                                  'Met the National Norm for Reading (Spring-2015)',
                                  'Exceeded Growth Projection for Math (Spring-2015)',
                                  'Achieved Growth Projection Math (Spring-2015)',
                                  'Achieved Any Growth in Math (Spring-2015)',
                                  'Test Percentile Math (Spring-2015)',
                                  'Met the National Norm for Math (Spring-2015)']]
        annual_summary_2015.rename(columns={'Peter Paul Location (2015)': 'PETER PAUL LOCATION',
                                            'PPDC 2014-2015': 'PPDC',
                                            'Summer Promise 2014': 'SUMMER PROMISE',
                                            'Exceeded Growth Projection for Reading (Spring-2015)': 'GROWTH READING EXCEED',
                                            'Achieved Growth Projection Reading (Spring-2015)': 'GROWTH READING MET',
                                            'Achieved Any Growth in Reading (Spring-2015)': 'GROWTH READING ANY',
                                            'Test Percentile Reading (Spring-2015)': 'TEST READING PERCENTILE',
                                            'Met the National Norm for Reading (Spring-2015)': 'MET NORM READING',
                                            'Exceeded Growth Projection for Math (Spring-2015)': 'GROWTH MATH EXCEED',
                                            'Achieved Growth Projection Math (Spring-2015)': 'GROWTH MATH MET',
                                            'Achieved Any Growth in Math (Spring-2015)': 'GROWTH MATH ANY',
                                            'Test Percentile Math (Spring-2015)': 'TEST MATH PERCENTILE',
                                            'Met the National Norm for Math (Spring-2015)': 'MET NORM MATH'}, inplace=True)
        annual_summary_2015['YEAR'] = 2015

        annual_summary_2014 = df[['MarkelID', 'Peter Paul Location (2014)', 'PPDC 2013-2014', 'Summer Promise 2013',
                                  'Exceeded Growth Projection for Reading (Spring-2014)',
                                  'Achieved Growth Projection Reading (Spring-2014)',
                                  'Achieved Any Growth in Reading (Spring-2014)',
                                  'Met the National Norm for Reading (Spring-2014)',
                                  'Exceeded Growth Projection for Math (Spring-2014)',
                                  'Achieved Growth Projection Math (Spring-2014)',
                                  'Achieved Any Growth in Math (Spring-2014)',
                                  'Met the National Norm for Math (Spring-2014)']]
        annual_summary_2014.rename(columns={'Peter Paul Location (2014)': 'PETER PAUL LOCATION',
                                            'PPDC 2013-2014': 'PPDC',
                                            'Summer Promise 2013': 'SUMMER PROMISE',
                                            'Exceeded Growth Projection for Reading (Spring-2014)': 'GROWTH READING EXCEED',
                                            'Achieved Growth Projection Reading (Spring-2014)': 'GROWTH READING MET',
                                            'Achieved Any Growth in Reading (Spring-2014)': 'GROWTH READING ANY',
                                            'Met the National Norm for Reading (Spring-2014)': 'MET NORM READING',
                                            'Exceeded Growth Projection for Math (Spring-2014)': 'GROWTH MATH EXCEED',
                                            'Achieved Growth Projection Math (Spring-2014)': 'GROWTH MATH MET',
                                            'Achieved Any Growth in Math (Spring-2014)': 'GROWTH MATH ANY',
                                            'Met the National Norm for Math (Spring-2014)': 'MET NORM MATH'}, inplace=True)
        annual_summary_2014['YEAR'] = 2014
        annual_summary_2019['TEST READING PERCENTILE'] = None
        annual_summary_2019['TEST MATH PERCENTILE'] = None

        annual_summaries = pandas.concat([annual_summary_2019, annual_summary_2018, annual_summary_2017,
                                         annual_summary_2016, annual_summary_2015, annual_summary_2014])
        for index, row in annual_summaries.iterrows():
            student_token = row['MarkelID']
            year = row['YEAR']

            peter_paul_location = row['PETER PAUL LOCATION']
            attended_peter_paul_during_school_year = row['PPDC']
            if str(attended_peter_paul_during_school_year).lower() == 'incomplete':
                attended_peter_paul_during_school_year = True
                did_not_complete_peter_paul_during_school_year = True
            elif attended_peter_paul_during_school_year == 1:
                attended_peter_paul_during_school_year = True
                did_not_complete_peter_paul_during_school_year = False
            else:
                attended_peter_paul_during_school_year = False
                did_not_complete_peter_paul_during_school_year = False
            attended_peter_paul_summer_promise = row['SUMMER PROMISE']
            if attended_peter_paul_summer_promise == 1:
                attended_peter_paul_summer_promise = True
            else:
                attended_peter_paul_summer_promise = False

            if row['GROWTH READING ANY'] is None:
                growth_in_reading = None
            elif type(row['GROWTH READING ANY']) != str:
                growth_in_reading = None
            elif row['GROWTH READING ANY'].lower() != 'yes':
                growth_in_reading = 'No Growth'
            elif row['GROWTH READING MET'] is None:
                growth_in_reading = 'Below Projection'
            elif type(row['GROWTH READING MET']) != str:
                growth_in_reading = 'Below Projection'
            elif row['GROWTH READING MET'].lower() != 'yes':
                growth_in_reading = 'Below Projection'
            elif row['GROWTH READING EXCEED'] is None:
                growth_in_reading = 'Met Projection'
            elif type(row['GROWTH READING EXCEED']) != str:
                growth_in_reading = 'Met Projection'
            elif row['GROWTH READING EXCEED'].lower() != 'yes':
                growth_in_reading = 'Met Projection'
            elif row['GROWTH READING EXCEED'].lower() == 'yes':
                growth_in_reading = 'Exceeded Projection'
            else:
                growth_in_reading = None

            test_percentile_in_reading = row['TEST READING PERCENTILE']
            met_national_norm_in_reading = row['MET NORM READING']
            if met_national_norm_in_reading is None:
                met_national_norm_in_reading = None
            elif type(met_national_norm_in_reading) != str:
                met_national_norm_in_reading = None
            elif met_national_norm_in_reading.lower() == 'yes':
                met_national_norm_in_reading = True
            elif met_national_norm_in_reading.lower() == 'no':
                met_national_norm_in_reading = False
            else:
                met_national_norm_in_reading = None

            if row['GROWTH MATH ANY'] is None:
                growth_in_math = None
            elif type(row['GROWTH MATH ANY']) != str:
                growth_in_math = None
            elif row['GROWTH MATH ANY'].lower() != 'yes':
                growth_in_math = 'No Growth'
            elif row['GROWTH MATH MET'] is None:
                growth_in_math = 'Below Projection'
            elif type(row['GROWTH MATH MET']) != str:
                growth_in_math = 'Below Projection'
            elif row['GROWTH MATH MET'].lower() != 'yes':
                growth_in_math = 'Below Projection'
            elif row['GROWTH MATH EXCEED'] is None:
                growth_in_math = 'Met Projection'
            elif type(row['GROWTH MATH EXCEED']) != str:
                growth_in_math = 'Met Projection'
            elif row['GROWTH MATH EXCEED'].lower() != 'yes':
                growth_in_math = 'Met Projection'
            elif row['GROWTH MATH EXCEED'].lower() == 'yes':
                growth_in_math = 'Exceeded Projection'
            else:
                growth_in_math = None

            test_percentile_in_math = row['TEST MATH PERCENTILE']
            met_national_norm_in_math = row['MET NORM MATH']
            if met_national_norm_in_math is None:
                met_national_norm_in_math = None
            elif type(met_national_norm_in_math) != str:
                met_national_norm_in_math = None
            elif met_national_norm_in_math.lower() == 'yes':
                met_national_norm_in_math = True
            elif met_national_norm_in_math.lower() == 'no':
                met_national_norm_in_math = False
            else:
                met_national_norm_in_math = None

            student = get_or_create_student(student_token=student_token)
            school_year = get_or_create_school_year(school_year=year)
            annual_summary = get_or_create_annual_summary(student, school_year)

            annual_summary.peter_paul_location = get_or_create_peter_paul_location(name=peter_paul_location)
            annual_summary.attended_peter_paul_during_school_year = attended_peter_paul_during_school_year
            annual_summary.attended_peter_paul_summer_promise = attended_peter_paul_summer_promise
            annual_summary.did_not_complete_peter_paul_during_school_year = did_not_complete_peter_paul_during_school_year

            annual_summary.growth_in_reading = growth_in_reading
            annual_summary.test_percentile_in_reading = test_percentile_in_reading
            annual_summary.met_national_norm_in_reading = met_national_norm_in_reading

            annual_summary.growth_in_math = growth_in_math
            annual_summary.test_percentile_in_math = test_percentile_in_math
            annual_summary.met_national_norm_in_math = met_national_norm_in_math

            session.commit()
