def get_courses(proba, already_done, ada):
    l = []
    proba = list(proba[0])
    for i in range(3):
        if proba is None:
            break
        while True:
            mp = max(proba)
            if mp in proba:
                proba.pop(proba.index(mp))
                if not ada.classes_[proba.index(mp)] in already_done:
                    l.append(proba.index(mp))
                    break
    return l        


def load_model():
    return joblib.load('model.pkl')


def encoded(data):
    dict_of_courses = get_dict()
    for i in range(len(data)):
        data.loc[i] = [dict_of_courses[j] for j in data.loc[i]]
    return data   


def get_dict():
    import pickle
    f=open('../dict_of_courses.picke','rb')# 'n' - new 
    return pickle.load(f)


def advice(data,already_done):
    ada = load_model()
    proba = ada.predict_proba(encoded(data))
    list_of_three_courses = get_courses(proba,already_done,ada)
    return [ada.classes_[i] for i in list_of_three_courses]