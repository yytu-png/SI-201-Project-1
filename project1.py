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


def sublist(dataset, category="Ship Mode", category_value='Second Class'):
    sublist = []

    for row in dataset:
        if row[category] == category_value:
            sublist.append(row)
    return sublist

def conditional_probability(dataset, category1, value1, category2, value2):
    sublist_category1 = sublist(dataset, category1, value1)
    count_category1 = len(sublist_category1)
    count_both = sum(1 for row in sublist_category1 if row[category2] == value2)

    if count_category1 == 0:
        return 0  
    return count_both / count_category1


def write_output():
    pass

def continuous_sublist(dataset, category1, lower_bound, upper_bound):
    sublist = []
    total = len(dataset)
    for row in dataset:
        value = float(row[category1])
        if lower_bound <= value <= upper_bound:
            sublist.append(row)
    
    return sublist



def main():
    file_path = "SampleSuperstore.csv"
    dataset = read_csv(file_path)


    answer = [] 
    while True :
        inq = input("Input query \" category1 = value1 | category2 = value2 \" to compute conditional probability \npress enter to do default computation. input exit to exit\n").strip()
        if inq == "":
            result = conditional_probability(dataset, "Ship Mode", "Second Class", "Segment", "Consumer")
            answer.append(f"Conditional probability: {result}")
            print(answer[-1])
            break
        elif inq == "exit":
            break
        else:
            try:
                category1, value1, category2, value2 = inq.replace(" ", "").split("|")
                category1, value1 = category1.split("=")
                category2, value2 = category2.split("=")
                result = conditional_probability(dataset, category1, value1, category2, value2)
                answer.append(f"Conditional probability: {result}")
                print(answer[-1])
            except Exception as e:                
                print("Invalid input format. Please try again.")

    print("\nSummary of results:")
    write_output()

if __name__ == "__main__":
    main()
    