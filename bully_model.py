import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import model_selection
import joblib

df = pd.read_csv('data/aggression_parsed_dataset.csv')
df2 = pd.read_csv('data/twitter_parsed_dataset.csv')
df3 = pd.read_csv('data/toxicity_parsed_dataset.csv')

data = df[df['oh_label']==0]
data = data.append(df[df['oh_label']==1])
data = data.append(df2[df2['oh_label']==0])
data = data.append(df2[df2['oh_label']==1])
data = data.append(df3[df3['oh_label']==0])
data = data.append(df3[df3['oh_label']==1])

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer

X_train, X_test, y_train, y_test = train_test_split(data['Text'], data['oh_label'], test_size = 0.3, random_state=0, shuffle= True, stratify=data['oh_label'])
clf = Pipeline([('tfidf', TfidfVectorizer()), ('clf', LogisticRegression(max_iter=4000))])

clf.fit(X_train, y_train)
print(clf.predict(["you're useless"]))
joblib.dump(clf,'bully_model.sav')
