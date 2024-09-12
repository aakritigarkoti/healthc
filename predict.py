import pandas as pd
import numpy as np
import joblib
import csv
import re
from sklearn.tree import _tree

# Load the saved model and label encoder
clf = joblib.load('trained_model.pkl')
le = joblib.load('label_encoder.pkl')

# Load the necessary data
testing = pd.read_csv('D:\\Study material\\Python\\Healthcare\\Data\\Testing.csv')
cols = testing.columns[:-1]

# Load the dictionaries
severityDictionary = {}
description_list = {}
precautionDictionary = {}

def load_data():
    global description_list, severityDictionary, precautionDictionary
    with open('D:\\Study material\\Python\\Healthcare\\MasterData\\symptom_Description.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if len(row) == 2:
                description_list[row[0]] = row[1]

    with open('D:\\Study material\\Python\\Healthcare\\MasterData\\Symptom_severity.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if len(row) == 2:
                try:
                    severityDictionary[row[0]] = int(row[1])
                except ValueError:
                    print(f"Invalid data: {row}")

    with open('D:\\Study material\\Python\\Healthcare\\MasterData\\symptom_precaution.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if len(row) == 5:
                precautionDictionary[row[0]] = [row[1], row[2], row[3], row[4]]

def calc_condition(exp, days):
    sum = 0
    for item in exp:
        sum += severityDictionary.get(item, 0)
    if ((sum * days) / (len(exp) + 1) > 13):
        return "You should take the consultation from doctor."
    else:
        return "It might not be that bad but you should take precautions."

def sec_predict(symptoms_exp):
    df = pd.read_csv('D:\\Study material\\Python\\Healthcare\\Data\\Training.csv')
    X = df.iloc[:, :-1]
    y = df['prognosis']
    symptoms_dict = {symptom: index for index, symptom in enumerate(X.columns)}
    input_vector = np.zeros(len(symptoms_dict))
    for item in symptoms_exp:
        input_vector[symptoms_dict[item]] = 1

    return clf.predict([input_vector])

def get_disease_description(disease):
    if disease in description_list:
        return description_list[disease]
    else:
        return "No description available for the predicted disease."

def get_precautions(disease):
    if disease in precautionDictionary:
        return precautionDictionary[disease]
    else:
        return ["No precautions available for the predicted disease."]

def check_pattern(dis_list, inp):
    pred_list = []
    inp = inp.replace(' ', '_')
    patt = f"{inp}"
    regexp = re.compile(patt)
    pred_list = [item for item in dis_list if regexp.search(item)]
    if len(pred_list) > 0:
        return 1, pred_list
    else:
        return 0, []

# Call this function to load data when the script is run
load_data()
