import pandas as pd
from sklearn import preprocessing
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
import joblib

# Loading
training = pd.read_csv('D:\\Study material\\Python\\Healthcare\\Data\\Training.csv')
cols = training.columns[:-1]
x = training[cols]
y = training['prognosis']

# Label encode the target variable
le = preprocessing.LabelEncoder()
le.fit(y)
y = le.transform(y)

# Split the data into training and testing sets
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.33, random_state=42)

# Train the Decision Tree Classifier
clf = DecisionTreeClassifier()
clf.fit(x_train, y_train)

# Save the trained model and the label encoder
joblib.dump(clf, 'trained_model.pkl')
joblib.dump(le, 'label_encoder.pkl')
print("Model and label encoder saved.")
