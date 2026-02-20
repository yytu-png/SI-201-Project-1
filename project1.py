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

def check_independence(dataset, category1, value1, category2, value2):
    p_category1 = len(sublist(dataset, category1, value1)) / len(dataset)
    p_category2 = len(sublist(dataset, category2, value2)) / len(dataset)
    p_both = len(sublist(sublist(dataset, category1, value1), category2, value2)) / len(dataset)

    stats = (p_both, p_category1, p_category2)
    return abs(p_both - (p_category1 * p_category2)) < 0.01, stats 

def write_output():
    pass

def main():
    file_path = "SampleSuperstore.csv"
    dataset = read_csv(file_path)


    answer = []
    stats = []
    while True :
        inq = input("Input query \" category1 = value1 | category2 = value2 \" to check independence \npress enter to do default computation. input exit to exit\n").strip()
        if inq == "":
            check_independence_result = check_independence(dataset, "Ship Mode", "Second Class", "Segment", "Consumer")
            if check_independence_result:
                answer.append("Ship Mode = Second Class and Segment = Consumer are independent.")
            else:
                answer.append("Ship Mode = Second Class and Segment = Consumer are not independent.")
            print(answer[-1])
            break
        elif inq == "exit":
            break
        else:
            try:
                parts = inq.split('|')

                category1, value1 = parts[0].strip().split('=', 1)
                category2, value2 = parts[1].strip().split('=', 1)
                category1, value1 = category1.strip(), value1.strip()
                category2, value2 = category2.strip(), value2.strip()
                print(f"Checking independence for {category1} = {value1} and {category2} = {value2}...")
                check_independence_result, stat = check_independence(dataset, category1, value1, category2, value2)
                if check_independence_result:
                    answer.append(f"{category1} = {value1} and {category2} = {value2} are independent.")
                else:
                    answer.append(f"{category1} = {value1} and {category2} = {value2} are not independent.")
                stats.append(stat)
                print(answer[-1])
            except Exception as e:                
                print("Invalid input format. Please try again.")

    print("\nSummary of results:")
    write_output()

if __name__ == "__main__":
    main()
    