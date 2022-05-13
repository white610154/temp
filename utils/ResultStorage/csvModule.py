import os, csv

class UsingCsv():
    def __init__(self, fileName: str, path: str, title: list):
        super(UsingCsv, self).__init__()
        self.title = title
        self.file = os.path.join(path, fileName)

    def create_csv(self):
        with open(self.file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(self.title)  
            csvfile.close()
    
    def writing(self, result, mode='w'): 
        with open(self.file, mode, newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(result)
            csvfile.close()
