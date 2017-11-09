import joblib

def __get_courses(proba, already_done, number_of_courses):
    l = []
    proba = list(proba[0])
    for i in range(number_of_courses):
        if proba is None:
            break
        while True:
            mp = max(proba)
            if mp in proba:
                if not proba.index(mp) in already_done:
                    l.append(proba.index(mp))
                    proba.pop(proba.index(mp))
                    break
            proba.pop(proba.index(mp))
    return l


def __load_model():
    return joblib.load('mldata\\model.pkl')


def advice(data, already_done, number_of_courses):
    ada = __load_model()
    proba = ada.predict_proba(data)
    return __get_courses(proba, already_done, number_of_courses)
