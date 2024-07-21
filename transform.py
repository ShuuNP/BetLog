import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

#nag copy paste lang kay GPT pero baka tapon ko kasi buggy AHHAHAHAHAH need talaga all by hand

def transform_and_train(json_path, model_path):
    # Load JSON data into a DataFrame
    data = pd.read_json(json_path)

    # Split 'position' into 'position_x' and 'position_y'
    data[['position_x', 'position_y']] = pd.DataFrame(data['position'].tolist(), index=data.index)

    # Prepare features and labels
    X = data[['position_x', 'position_y', 'time']]
    y = data['action']

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the model
    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    # Save the trained model
    joblib.dump(model, model_path)

if __name__ == "__main__":
    transform_and_train("data_log.json", "player_behavior_model.pkl")
