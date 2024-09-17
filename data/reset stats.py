import pickle

file = open('data', 'wb')
data = [0, 0, 0]
pickle.dump(data, file)
file.close()
