from keras.models import Sequential
from keras.layers import Dense
import math
from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from ..models import Trainee
import numpy as np
import pandas as pd
from keras.models import model_from_json


###

def baseline_model():
    model = Sequential()
    model.add(Dense(output_dim=10, input_dim=12, kernel_initializer='normal', activation='relu'))
    model.add(Dense(output_dim=10, kernel_initializer='normal', activation='relu'))
    model.add(Dense(output_dim=1, kernel_initializer='normal'))
    model.compile(loss='mean_squared_error', optimizer='adam')
    return model


def calculateSD(data):
    sum, mean, standardDeviation = 0
    for i in range(len(data)):
        sum = sum + data[i]
    mean = sum / len(data)
    for i in range(len(data)):
        standardDeviation = standardDeviation + (data[i] - mean) * (data[i] - mean)
    return math.sqrt(standardDeviation / len(data))


def calculateAverage(data):
    sum, mean = 0
    for i in range(len(data)):
        sum = sum + data[i]
    mean = sum / len(data)
    return mean


def update_trainee_score(x):
    print('Updating Profile Scores ...')
    academic_score = []
    honesty = []
    emotionality = []
    extraversion = []
    agreeableness = []
    conscientiousness = []
    openness = []
    iq = []
    verbal_ability = []
    score = []
    course_score = []
    qa_score = []
    project_score = []

    for p in Trainee.objects.all().exclude(pk=x.pk):

        if p.academic_score is None or p.personality_c is None or p.personality_h is None or p.personality_a is None or p.personality_e is None or p.personality_o is None or p.personality_x is None or p.iq_score is None or p.course_score is None or p.project_score is None or p.verbal_ability_score is None or p.qa_score is None or p.score is None:
            continue
        academic_score.append(p.academic_score)
        honesty.append(p.personality_h)
        emotionality.append(p.personality_e)
        extraversion.append(p.personality_x)
        agreeableness.append(p.personality_a)
        conscientiousness.append(p.personality_c)
        openness.append(p.personality_o)
        iq.append(p.iq_score)
        verbal_ability.append(p.verbal_ability_score)
        score.append(p.score)
        project_score.append(p.project_score)
        course_score.append(p.course_score)
        qa_score.append(p.qa_score)

    if len(academic_score) == 0:
        x.score = 0.6
        x.save()

    else:

        d = {'1': academic_score, '2': honesty, '3': emotionality, '4': extraversion, '5': agreeableness,
             '6': conscientiousness, '7': openness, '8': iq, '9': verbal_ability, '10': project_score,
             '11': course_score,
             '12': qa_score, '13': score}
        df = pd.DataFrame(data=d)
        X = df.iloc[:, [0, 1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12]].values
        y = df.iloc[:, 4].values

        sc = StandardScaler()
        X = sc.fit_transform(X)
        estimator = KerasRegressor(build_fn=baseline_model, batch_size=50, epochs=100, verbose=0)
        estimator.fit(X, y)

        test_pred_temp = []
        test_pred = []
        test_pred_temp.append(x.academic_score)
        test_pred_temp.append(x.personality_h)
        test_pred_temp.append(x.personality_e)
        test_pred_temp.append(x.personality_x)
        test_pred_temp.append(x.personality_a)
        test_pred_temp.append(x.personality_c)
        test_pred_temp.append(x.personality_o)
        test_pred_temp.append(x.iq_score)
        test_pred_temp.append(x.verbal_ability_score)
        test_pred_temp.append(x.project_score)
        test_pred_temp.append(x.course_score)
        test_pred_temp.append(x.qa_score)

        test_pred.append(test_pred_temp)
        test_pred_1 = np.asarray(test_pred)
        new_prediction = estimator.predict(test_pred_1)

        y = np.insert(y, y.size, new_prediction)
        X = np.concatenate((X, test_pred_1), axis=0)

        y_new = []
        for x in y:
            y_new.append(x)

        tot = 0
        for i in y_new:
            tot = tot + i
        mn = tot / len(y_new)
        std = 0
        for i in y_new:
            std = std + (i - mn) * (i - mn)
        sd = math.sqrt(std / len(y_new))
        avg = mn

        y_final = []

        for i in range(len(y_new)):
            pp = (y_new[i] - avg) / sd * 0.1 + 0.8
            if pp >= 1.0:
                pp = 0.9999
            if pp <= 0.6:
                pp = 0.0001
            y_final.append(pp)

        ctr = 0
        for p in Trainee.objects.all():
            p.score = y_final[ctr]
            p.save()
            ctr += 1
