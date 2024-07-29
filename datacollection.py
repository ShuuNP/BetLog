import json

data_log = []

def log_data(action, position, time):
    data_log.append({
        "action": action,
        "position": position,
        "time": time
    })

def save_data_log(filename="data_log.json"):
    with open(filename, "w") as f:
        json.dump(data_log, f)
