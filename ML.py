def get_courses(proba, already_done, ada):
    l = []
    proba = list(proba[0])
    for i in range(3):
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


def load_model():
    return joblib.load('model.pkl')


def advice(data,already_done):
    ada = load_model()
    proba = ada.predict_proba(data)
    return get_courses(proba,already_done,ada)