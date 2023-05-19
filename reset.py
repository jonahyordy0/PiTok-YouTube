import pickle
with open("info.pkl", "wb") as f:
    pickle.dump([0, 1], f)