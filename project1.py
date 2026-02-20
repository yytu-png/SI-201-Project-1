import csv

from matplotlib import category

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


def probability_of_category(dataset, category="Ship Mode", category_value='Second Class'):
    count = 0
    for row in dataset:
        if row[category] == category_value:
            count += 1
    return count / len(dataset)


def write_output():
    pass

def main():
    file_path = "SampleSuperstore.csv"
    dataset = read_csv(file_path)
    print(dataset[0])  # Print the first row to verify the data is read correctly

    probability = {}
    while True :
        inq = input("Enter format [ category = value ] to calculate its probability or enter nothing to display default computation, enter exit to exit: ")
        if inq == "":
            probability["Ship Mode = Second Class"] = probability_of_category(dataset)
            print(f"Probability of category 'Ship Mode = Second Class': {probability['Ship Mode = Second Class']}")
            break
        elif inq == "exit":
            break
        else:
            category, value = inq.split('=')
            category = category.strip()
            value = value.strip()
            probability[f"{category} = {value}"] = probability_of_category(dataset, category, value)
            print(f"Probability of category '{category} = {value}': {probability[f'{category} = {value}']}")

if __name__ == "__main__":
    main()
    