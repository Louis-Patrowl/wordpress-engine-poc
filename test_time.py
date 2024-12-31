import time

class testtime():
    def __init__(self, id):
        self.begin  = time.time()
        self.id = id

    def end(self):
        print(f"Elasped time {self.id}: {time.time() - self.begin}" )