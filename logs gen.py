import os, pickle
logs = "test"
main_path = os.path.dirname(os.path.realpath(__file__))

PATH = f"{main_path}/resources/"
with open(f"{PATH}/log.txt", "wb") as f:
    pickle.dump(logs, f)  