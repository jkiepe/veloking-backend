import pandas

def read_data(name: str):
    data = pandas.read_json(f"./database/{name}.json").to_json()
    return data
