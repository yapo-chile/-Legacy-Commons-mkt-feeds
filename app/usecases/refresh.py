import threading


# RefreshUsecases start process to get data from source to refresh db
class RefreshUsecases():
    def __init__(self, extractDataRepo):
        self.extractDataRepo = extractDataRepo

    def generate(self):
        # self.extractDataRepo.mainExtract()
        t = threading.Thread(target=self.extractDataRepo.mainExtract)
        t.start()
