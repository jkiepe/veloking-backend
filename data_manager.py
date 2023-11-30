import json

def read_data(name: str):
    with open(f"./database/{name}.json", "r") as file:
        data = json.loads(file.read())
    return data
