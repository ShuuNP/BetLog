from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import json
import numpy as np

with open('data_log.json', 'r') as f:
    data_log = json.load(f)


features = []
labels = []

for entry in data_log:

    features.append([entry['position'], entry['time']])
    labels.append(0 if entry['action'] == 'move_left' else 1)

# Convert lists to numpy arrays
features = np.array(features)
labels = np.array(labels)
X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)

model = DecisionTreeClassifier()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
