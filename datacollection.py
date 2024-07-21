import json

# Initialize data log
data_log = []

# Function to log data
def log_data(action, position, time):
    data_log.append({
        "action": action,
        "position": position,
        "time": time
    })

# Function to save data log to a file
def save_data_log(filename="data_log.json"):
    with open(filename, "w") as f:
        json.dump(data_log, f)
