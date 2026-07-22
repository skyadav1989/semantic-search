
from time import perf_counter

class ProgressReporter:
    def __init__(self):
        self.start=perf_counter()
        self.total=0

    def tick(self):
        self.total+=1
        if self.total%100==0:
            print(f"Processed: {self.total}")

    def finish(self):
        print(f"Completed {self.total} products in {perf_counter()-self.start:.2f}s")
