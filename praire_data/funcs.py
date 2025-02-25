import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

BASE_URL = 'https://us.prairielearn.com'

def get_gradebook(course_id, token):
    """
    Gets the gradebook for a course from PrairieLearn. 
    Returns a DataFrame with the "Assessments" column exploded.
    """
    URL = BASE_URL + f'/pl/api/v1/course_instances/{course_id}/gradebook'
    grades = pd.DataFrame(requests.get(URL, headers={'Private-Token': token}).json())

    df_exploded = grades.explode("assessments")
    df_assessments = pd.json_normalize(df_exploded["assessments"])
    df_final = df_exploded.drop(columns=["assessments"]).reset_index(drop=True)
    df_final = pd.concat([df_final, df_assessments], axis=1)

    return df_final


def get_assessments(course_id, token) -> dict:
    """
    Gets the assessments for a course from PrairieLearn.
    Returns JSON object.
    """
    URL = BASE_URL + f'/pl/api/v1/course_instances/{course_id}/assessments'
    return requests.get(URL, headers={'Private-Token': token}).json()


def get_assessment_instance(course_id, token, assessment_id) -> dict:
    """
    Gets the assessment instance for a course from PrairieLearn.
    Returns JSON object.
    """
    URL = BASE_URL + f'/pl/api/v1/course_instances/{course_id}/assessment_instances/{assessment_id}'
    return requests.get(URL, headers={'Private-Token': token}).json()


def compare_grades(gradebook : pd.DataFrame, assessments : list) -> None:
    # ------------- TO BE IMPROVED -------------
    """
    Returns a DataFrame with the grades of the students for the given assessments.
    """
    grades_vetores = gradebook[(gradebook['assessment_label'].isin(assessments)) &
                         (~gradebook['assessment_name'].isin(['AI_2024s2', 'AF_2024s2']))]
    
    provas = grades_vetores[['score_perc', 'assessment_label']]
    prova1 = provas.loc[provas['assessment_label'] == assessments[0], 'score_perc'].to_numpy()
    prova2 = provas.loc[provas['assessment_label'] == assessments[1], 'score_perc'].to_numpy()
    provas = np.column_stack((prova1, prova2)) + np.random.randn(len(prova1), 2)

    scatter = provas[~np.isnan(provas).any(axis=1)]
    plt.scatter(scatter[:, 0], scatter[:, 1], alpha=0.3)
    plt.xlabel('Nota Prova 1')
    plt.ylabel('Nota Prova 2')
    plt.title('Prova 1 x Prova 2')
    plt.show()


def grades_and_time_by_student(gradebook : pd.DataFrame, assessments : list, by_assessment_type : bool = False) -> pd.DataFrame:
    """
    If by_assessment_type is True, returns a DataFrame with the average grade and time spent by student for each assessment type (CW, Q and Provas).
    Returns a DataFrame with the average grade and time spent by student for each assessment or assessment type.
    """

    grades = gradebook.loc[(gradebook['assessment_label'].isin(assessments)) &
                    (~gradebook['assessment_name'].isin(['AI_2024s2', 'AF_2024s2'])), :].copy()

    grades.loc[:, 'points%'] = grades.loc[:, 'points'] / grades.loc[:, 'max_points'] * 100

    grades_pivot = grades.pivot_table(
        index=['user_id', 'user_name'],
        columns='assessment_set_abbreviation' if by_assessment_type else 'assessment_label',
        values=['points%', 'duration_seconds'],
        aggfunc={'points%': 'mean', 'duration_seconds': 'mean'}
        ).reset_index()

    grades_pivot.columns = ['_'.join(col).strip() if col[1] else col[0] for col in grades_pivot.columns.values]

    assessment_types = grades['assessment_set_abbreviation'].unique() if by_assessment_type else grades['assessment_label'].unique()
    
    ordered_cols = [[f'points%_{assessment}', f'duration_seconds_{assessment}'] for assessment in assessment_types]
    return grades_pivot[['user_id', 'user_name', *[col for cols in ordered_cols for col in cols]]]