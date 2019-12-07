import os
import pandas as pd

NUM_RESPONDENT_LABEL = 'Num of respondents'
HOURS_PER_WEEK = 'Hrs Per Week'
HOURS_PER_WEEK_IDX = 12
HOURS_PER_WEEK_DEFAULT = 0
INTEREST_IN_STUDENT = 'Interest in student learning'
COURSE_REQ = 'Clearly explain course requirements'
CLEAR_LEARNING = 'Clear learning objectives'
FEEDBACK = 'Instructor provides feedback'
IMPORTANCE_SUBJECT = 'Importance of subject'
SUBJECT_MATTER = 'Explains subject matter of course'
SHOW_RESPECT = 'Show respect for all students'
OVERALL_TEACHING = 'Overall teaching rate'
OVERALL_COURSE = 'Overall course rate'
DATAFRAME_INDEX = [NUM_RESPONDENT_LABEL, HOURS_PER_WEEK, INTEREST_IN_STUDENT, COURSE_REQ,
                   CLEAR_LEARNING, FEEDBACK, IMPORTANCE_SUBJECT, SUBJECT_MATTER,
                   SHOW_RESPECT, OVERALL_TEACHING, OVERALL_COURSE]


def fceScore(courseId, instName):
    filename = os.getcwd() + os.sep + 'fce' + os.sep + 'fce_' + courseId + '.csv'
    defaultReturn = {i: 0 for i in DATAFRAME_INDEX}
    defaultReturn[HOURS_PER_WEEK] = HOURS_PER_WEEK_DEFAULT
    try:
        df = None
        with open(filename, 'r') as f:
            for line in f:
                x = line.strip().split(',')
                y = []
                for e in x:
                    if len(y) == 0:
                        y.append(e)
                    elif y[-1][0] == '"':
                        # convert '"HYATT,' , ' KIM"' into 'HYATT,KIM'
                        y[-1] = y[-1] + "," + e
                        if y[-1][-1] == '"':
                            y[-1] = y[-1][1:-1]
                    else:
                        y.append(e)
                if y[6].lower() == instName.lower():
                    sss = {
                        NUM_RESPONDENT_LABEL: float(y[9]),
                        HOURS_PER_WEEK: float(y[HOURS_PER_WEEK_IDX] if y[HOURS_PER_WEEK_IDX] != ' '
                                              else HOURS_PER_WEEK_DEFAULT),
                        INTEREST_IN_STUDENT: float(y[15]),
                        COURSE_REQ: float(y[16]),
                        CLEAR_LEARNING: float(y[17]),
                        FEEDBACK: float(y[18]),
                        IMPORTANCE_SUBJECT: float(y[19]),
                        SUBJECT_MATTER: float(y[20]),
                        SHOW_RESPECT: float(y[21]),
                        OVERALL_TEACHING: float(y[22]),
                        OVERALL_COURSE: float(y[23])
                    }
                    if df is None:
                        df = pd.DataFrame(sss,
                                          index=DATAFRAME_INDEX, dtype='float')
                    else:
                        df = df.append(sss, ignore_index=True)
        if df is None:
            return defaultReturn
        else:
            return dict(df.mean())
    except FileNotFoundError:
        print(filename + ' not found')
        return defaultReturn



def main():
    courseIds = ['93852', '94701', '94701','94701','94700','94700']
    names = ['Flower, Hello', 'Hyatt, Kim', 'Massaro, Haylee','Tentacles, Squidward','KRACKHARDT, DAVID','LASSMAN, DAVID']
    for i in range(0, len(courseIds)):
        courseId = courseIds[i]
        name = names[i]
        print(courseId, ' ', name, ' ', fceScore(courseId, name))


if __name__ == '__main__':
    main()
