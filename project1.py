import csv

def read_csv(file_path):
    data = []
    with open(file_path, mode='r') as file:
        header = file.readline().strip().split(',')
        csv_reader = csv.DictReader(file)
        
        for row in csv_reader:
            row = list(row.values())
            d = {}
            for i in range(len(header)):
                d[header[i]]=row[i]
            data.append(d)

    return data

if __name__ == "__main__":
    file_path = "SampleSuperstore.csv"
    dataset = read_csv(file_path)
    
    print(dataset[0])