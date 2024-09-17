import pickle

class Main():
    def __init__(self):
        file = open('data', 'rb')
        data = pickle.load(file)
        print(data)
        file.close()
    def getting_data(self):
        return data
    
Main()