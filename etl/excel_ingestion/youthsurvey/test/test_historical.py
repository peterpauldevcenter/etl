from etl.excel_ingestion.youthsurvey.youthsurveyhistorical import question_re


def test_regex():
    question_1 = 'Spring-2016 c. Is there an adult here who helps you when you have a problem?'
    question_2 = 'spring - 2017 b. This is a test question.'
    question_3 = 'fall 2015 another test'

    expected = (
        {'firstword': 'Spring', 'year': '2016',
         'question': 'c. Is there an adult here who helps you when you have a problem?'},
        {'firstword': 'spring', 'year': '2017', 'question': 'b. This is a test question.'},
        {'firstword': 'fall', 'year': '2015', 'question': 'another test'}
    )

    for expected, question in zip(expected, (question_1, question_2, question_3)):
        match = question_re.match(question)
        assert match.groupdict() == expected
