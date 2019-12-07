"""
    Combine the FCE scores with available sections for the next semester
    Input:
        fce files located in fce folder
        sch files located in sch folder
    Output:
        mrg files located in mrg folder
"""

import os
import pandas as pd
import scoring
import math

DATAFRAME_ADDITIONAL_INDEX = [
    scoring.HOURS_PER_WEEK,
    scoring.INTEREST_IN_STUDENT,
    scoring.COURSE_REQ,
    scoring.CLEAR_LEARNING,
    scoring.FEEDBACK,
    scoring.IMPORTANCE_SUBJECT,
    scoring.SUBJECT_MATTER,
    scoring.SHOW_RESPECT,
    scoring.OVERALL_TEACHING,
    scoring.OVERALL_COURSE
]


def generateSchedule():
    """
        Parse fce and sch files. calculate the scores of instructor's course using the scoring.py files
    :return:
    """
    for prefix in ['94', '95']:
        filename = os.getcwd() + os.sep + 'sch' + os.sep + prefix + '.csv'
        merged_filename = os.getcwd() + os.sep + 'mrg' + os.sep + 'mrg_' + prefix + '.csv'
        data = pd.read_csv(filename, dtype={'Course': 'str', 'Sec': 'str'})

        # append additional data - set 0 as default value
        for col in DATAFRAME_ADDITIONAL_INDEX:
            data[col] = [0 for i in range(0, len(data))]
        data[scoring.HOURS_PER_WEEK] = scoring.HOURS_PER_WEEK_DEFAULT

        for i in data.index:
            # reformat for bruteforce approach
            if math.isnan(float(data.loc[i]['Course'])):
                for c in ['Course', 'Course Title', 'Units']:
                    data.loc[i, c] = data[c][i - 1]

            if str(data['Sec'][i]) == 'nan':
                data.loc[i, 'Sec'] = data['Sec'][i - 1]

            # calculate the section score for each of its instructor
            instructors = data['Instructor'][i].split('\n')
            course = data['Course'][i]
            scoreDataFrame = pd.DataFrame({k: [] for k in DATAFRAME_ADDITIONAL_INDEX})
            for instructor in instructors:
                # print('looking for', course, instructor)
                dictScores = scoring.fceScore(course, instructor)
                scoreDataFrame = scoreDataFrame.append({k: dictScores[k] for k in DATAFRAME_ADDITIONAL_INDEX},
                                                       ignore_index=True)
            # append scoring if we found any instructor data
            if len(scoreDataFrame) > 0:
                scoreDataFrame = scoreDataFrame.mean()
                for c in DATAFRAME_ADDITIONAL_INDEX:
                    data.loc[i, c] = scoreDataFrame[c]

        # give micro mini average from mini and semester long course
        unitsDf = \
            data[data.apply(lambda x: x[scoring.OVERALL_COURSE] > 0.01 and x['Units'] in ['3', '6', '12'],
                            axis=1)].groupby(
                ['Units'])[
                DATAFRAME_ADDITIONAL_INDEX].mean()
        for unit in ['3', '6', '12']:
            if unit in unitsDf.index:
                for col in DATAFRAME_ADDITIONAL_INDEX:
                    unitsDf.loc[unit, col] = unitsDf[col][unit] * 3 / int(unit)
        unitsDf = unitsDf.mean()
        for i in data.index:
            for col in DATAFRAME_ADDITIONAL_INDEX:
                if data[col][i] <= 0.01:
                    data.loc[i, col] = unitsDf[col]

        data.to_csv(merged_filename, index=False)
    # end for


def main():
    generateSchedule()


if __name__ == '__main__':
    main()
