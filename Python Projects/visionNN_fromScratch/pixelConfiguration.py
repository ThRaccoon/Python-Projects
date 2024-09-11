import ast
import random


print("Enter 'training' to format and shuffle the training data")
print("or enter 'testing' to format the cpu&gpu_testing data")
user_input = input(":")

# Formating and shuffling the training data
if user_input == "training":
    shuffled = []
    with (open("training&testing_data/raw_training_data.csv", "r") as starting_data,
          open("training&testing_data/formatted_training_data.csv", "w") as final_data):
        for line in starting_data:
            shuffled.append(list(ast.literal_eval(line.strip())))
        random.shuffle(shuffled)

        for row in shuffled:
            first_element = row.pop(0)

            for i in range(len(row)):
                if row[i] > 0:
                    row[i] = 0.01
                else:
                    row[i] = 0.00

            row.append(first_element)
            final_data.write(f"{row}\n")
        print("Training data was formatted and shuffled!")

# Formating the cpu&gpu_testing data
elif user_input == "testing":
    testing_data = []
    with (open("training&testing_data/raw_testing_data.csv", "r") as raw_data,
          open("training&testing_data/formatted_testing_data.csv", "w") as formatted_data):
        for line in raw_data:
            testing_data.append(list(ast.literal_eval(line.strip())))

        for row in testing_data:
            first_element = row.pop(0)

            for i in range(len(row)):
                if row[i] > 0:
                    row[i] = 0.01
                else:
                    row[i] = 0.00

            row.append(first_element)
            formatted_data.write(f"{row}\n")
        print("Testing data was formatted!")

# Error
else:
    print(f"{user_input} was not a valid input!")
    exit(0)
