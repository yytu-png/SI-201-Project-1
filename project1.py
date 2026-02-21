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

def probability(dataset, category, value):
    return len(sublist(dataset, category, value)) / len(dataset) if len(dataset) > 0 else 0

def sublist1(dataset, category="Ship Mode", category_value='Second Class'):
    subls = []

    for row in dataset:
        if row[category] == category_value:
            subls.append(row)
    return subls

def conditional_probability1(dataset, category1, value1, category2, value2):
    sublist_category1 = sublist(dataset, category1, value1)
    count_category1 = len(sublist_category1)
    count_both = len(sublist(sublist_category1, category2, value2))

    if count_category1 == 0:
        return 0  
    return count_both / count_category1


def sublist2(dataset, category1, lower_bound, upper_bound, inclusive_lower=True, inclusive_upper=True):
    subls = []
    if lower_bound == upper_bound:
        return sublist(dataset, category1, lower_bound)
    for row in dataset:
        value = float(row[category1])
        if ((inclusive_lower and value >= lower_bound) or (not inclusive_lower and value > lower_bound)) and \
           ((inclusive_upper and value <= upper_bound) or (not inclusive_upper and value < upper_bound)):
            subls.append(row)
    
    return subls

def sublist(*args):
    if len(args) == 3:
        return sublist1(*args)
    elif len(args) >4:
        return sublist2(*args)
    else:
        raise ValueError("Invalid number of arguments for sublist function.")

def conditional_probability2(dataset, category1, lower_bound1, upper_bound1, category2, lower_bound2, upper_bound2, inclusive_lower1=True, inclusive_upper1=True, inclusive_lower2=True, inclusive_upper2=True):
    if upper_bound1 == -1:
        upper_bound1 = float('inf')
    if upper_bound2 == -1:
        upper_bound2 = float('inf')
    sublist1 = sublist(dataset, category1, lower_bound1, upper_bound1, inclusive_lower1, inclusive_upper1)
    count_both = len(sublist(sublist1, category2, lower_bound2, upper_bound2, inclusive_lower2, inclusive_upper2))
    count_category1 = len(sublist1)

    if count_category1 == 0:
        return 0
    return count_both / count_category1

def conditional_probability(*args):
    if len(args) == 5:
        return conditional_probability1(*args)
    elif len(args) >= 7:
        return conditional_probability2(*args)
    else:
        raise ValueError("Invalid number of arguments for conditional_probability function.")
    
def write_output(answer):
    with open("output.txt", mode='w') as file:
        for item in answer:
            file.write("The probability of")
            if len(item) == 3:
                file.write(f" P({item[0]} being {item[1]}) = {item[2]}\n")
            elif len(item) == 5:
                file.write(f" P({item[0]} = {item[1]} | {item[2]} = {item[3]}) = {item[4]}\n")
            elif len(item) == 6:
                if (item[1].find("[") != -1 or item[1].find("(") != -1) and (item[3].find("[") != -1 or item[3].find("(") != -1):
                    file.write(f" P({item[0]} in {item[1]} | {item[2]} in {item[3]}) = {item[4]}\n")
                elif item[1].find("[") != -1 or item[1].find("(") != -1:
                    file.write(f" P({item[0]} in {item[1]} | {item[2]} = {item[3]}) = {item[4]}\n")
                elif item[3].find("[") != -1 or item[3].find("(") != -1:
                    file.write(f" P({item[0]} = {item[1]} | {item[2]} in {item[3]}) = {item[4]}\n")
                    
        

def main():
    file_path = "SampleSuperstore.csv"
    dataset = read_csv(file_path)
    print("Reading successful.")
    answer = [] 
    while True :
        inq = input("Input query\n0.\"<category1> = <value1>\" for propability \n1. \" <category1> = <value1> | <category2 = value2> \" to compute conditional probability\n2. \" <category1> = <[lower,upper]> or <value1> | category2 = <(lower2,upper2]> or <value2> \" to compute continuous conditional probability. Use \"[\" or \"(\" to indicate inclusive or exclusive bounds. Use -1 for infinity \n3.press enter to do default computation \n4.Type exit to exit\n").strip()
        if inq == "":
            result = conditional_probability(dataset, "Ship Mode", "Second Class", "Segment", "Consumer")
            answer.append(("Ship Mode", "Second Class", "Segment", "Consumer", result))
            print("probability of Ship Mode being Second Class given Segment is Consumer:", result)
            result = conditional_probability(dataset, "Ship Mode", "Second Class", "Second Class", "Profit", 15.0, -1)
            answer.append(("Ship Mode", "Second Class", "Profit", "[15.0,-1]" , result, None))
            print("probability of Ship Mode being Second Class given Profit is greater than 15.0:")
            break
        elif inq == "exit":
            break
        else:
            try:
                part = inq.split("|")
                if len(part) == 1:
                    category, value = part[0].strip().split("=")
                    category = category.strip()
                    value = value.strip()
                    result = probability(dataset, category, value)
                    print(f"Probability: {result}")
                    answer.append((category, value, result))
                    continue
                print(part)
                category1, value1 = part[0].strip().split("=")
                category2, value2 = part[1].strip().split("=")
                value1 = value1.strip()
                value2 = value2.strip()
                print(f"Parsed input: category1={category1.strip()}, value1={value1.strip()}, category2={category2.strip()}, value2={value2.strip()}")
                if value1.startswith("[") or value1.startswith("("):
                    lower_bound1, upper_bound1 = value1[1:-1].split(",")
                    lower_bound1 = float(lower_bound1)
                    upper_bound1 = float(upper_bound1)
                    inclusive_lower1 = value1.startswith("[")
                    inclusive_upper1 = value1.endswith("]")
                else:
                    lower_bound1 = value1.strip()
                    upper_bound1 = value1.strip()
                    inclusive_lower1 = True
                    inclusive_upper1 = True
                if value2.startswith("[") or value2.startswith("("):
                    lower_bound2, upper_bound2 = value2[1:-1].split(",")
                    lower_bound2 = float(lower_bound2)
                    upper_bound2 = float(upper_bound2)
                    inclusive_lower2 = value2.startswith("[")
                    inclusive_upper2 = value2.endswith("]")
                else:
                    lower_bound2 = value2.strip()
                    upper_bound2 = value2.strip()
                    inclusive_lower2 = True
                    inclusive_upper2 = True
                
                print(f"Computing conditional probability for {category1.strip()} in [{lower_bound1}, {upper_bound1}] and {category2.strip()} in [{lower_bound2}, {upper_bound2}] with inclusive bounds ({inclusive_lower1}, {inclusive_upper1}) and ({inclusive_lower2}, {inclusive_upper2})")
                if lower_bound1 == upper_bound1 and lower_bound2 == upper_bound2:
                    result = conditional_probability(dataset, category1.strip(), value1.strip(), category2.strip(), value2.strip())
                    print(f"Conditional probability: {result}")
                    answer.append((category1.strip(), value1.strip(), category2.strip(), value2.strip(), result))
                    continue

                if lower_bound1 > upper_bound1 and upper_bound1 != -1:
                    print("Invalid bounds for category1. Please try again.")
                    continue
                if lower_bound2 > upper_bound2 and upper_bound2 != -1:
                    print("Invalid bounds for category2. Please try again.")
                    continue
                
                result = conditional_probability(dataset, category1.strip(), lower_bound1, upper_bound1, category2.strip(), lower_bound2, upper_bound2, inclusive_lower1, inclusive_upper1, inclusive_lower2, inclusive_upper2)
                print(f"Conditional probability: {result}")
                answer.append((category1.strip(), value1, category2.strip(), value2, result, None))
                print(answer[-1])
            except ValueError as e:   
                print(e)
                print("Invalid input format. Please try again.")

    print("\nSummary of results is printed in output.txt")
    write_output(answer)

if __name__ == "__main__":
    main()
    