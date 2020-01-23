def get_data(file):
    """
    Get the data from the text file
    :param file: HW2 Input text files
    :return: number of lines, Weight, Volume and Item details
    """

    # Open question-2 input texts
    f = open(file=file)

    # Initialize the variables
    number_of_items = 0
    weight_constraint = 0
    items = []

    # Read from the text file
    for i, line in enumerate(f):
        if i == 0:
            number_of_items = int(line)
        elif i == number_of_items+1:
            weight_constraint = int(line)
        else:
            if line != "\n":
                item_id, profit, weight = line.split('\t')
                items.append([int(item_id), float(profit), float(weight)])

    # Close the text file
    f.close()

    return number_of_items, weight_constraint, items


def greedy_initial_solution(items):
    """

    :param items: Data's in the instance text files.
    :return: Weight / profit
    """

    greedy_procedure = []
    ratio_list = []
    weight_list = []
    profit_list = []

    for item in items:
        item_id = item[0]
        profit = item[1]
        weight = item[2]

        ratio = round(profit / weight, 2)

        greedy_procedure.append([item_id, ratio])
        ratio_list.append(ratio)
        weight_list.append(weight)
        profit_list.append(profit)

    return greedy_procedure, ratio_list, weight_list, profit_list


def dictionary_to_binary_list(solution, number_of_items):
    binary_array = []

    sorted_keys = sorted(solution.keys())
    key_counter = 0

    items_taken = sorted_keys

    for counter in range(0, number_of_items):
        if counter == sorted_keys[key_counter]:
            binary_array.append(1)
            if key_counter + 1 <= len(sorted_keys) - 1:
                key_counter += 1
        else:
            binary_array.append(0)

    return items_taken, binary_array


def print_result(version, total_profit, binary_array, total_weight, items_taken):
    print("\nLocal Search version-{0}\n".format(version))
    print("total_profit:{0}\titems taken:{1}\ttotal weight:{2}".format(total_profit, binary_array, total_weight))
    print("\nsimplified items taken:{0}\n".format(items_taken))
