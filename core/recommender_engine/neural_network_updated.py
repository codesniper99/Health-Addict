from ..models import Trainee
import numpy as np
import pandas as pd
from keras.models import model_from_json
from keras.models import Sequential
from keras.layers import Dense
from sklearn.preprocessing import StandardScaler


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
        x.score = 0.5
        x.save()
    else:
        d = {'1': academic_score, '2': honesty, '3': emotionality, '4': extraversion, '5': agreeableness,
             '6': conscientiousness, '7': openness, '8': iq, '9': verbal_ability, '10': project_score, '11': course_score,
             '12': qa_score, '13':score}
        df = pd.DataFrame(data=d)
        X = df.iloc[:, 0:12].values
        y = df.iloc[:, 12].values

        sc = StandardScaler()
        X = sc.fit_transform(X)

        classifier = Sequential()
        classifier.add(Dense(output_dim=10, init='uniform', activation='sigmoid', input_dim=12))
        classifier.add(Dense(output_dim=10, init='uniform', activation='sigmoid'))
        classifier.add(Dense(output_dim=1, init='uniform', activation='sigmoid'))
        classifier.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        classifier.fit(X, y, batch_size=5, nb_epoch=100)

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
        new_prediction = classifier.predict(test_pred_1)

        y = np.insert(y, y.size, new_prediction)
        y_temp_for_argsort = np.asarray(y)
        y_temp_for_argsort = np.argsort(y_temp_for_argsort)

        for j in range(len(y_temp_for_argsort)):
            idx = y_temp_for_argsort[j]
            val = j + 1
            val = val / (len(y_temp_for_argsort) + 1.0)
            y[idx] = val

        X = np.concatenate((X, test_pred_1), axis=0)

        # update the scores of all people
        ctr = 0
        for p in Trainee.objects.all():
            p.score = y[ctr]
            p.save()
            ctr += 1
