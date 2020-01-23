from methods import get_data
from items import Items
from simulated_annealing import SA
from os.path import join


def main():
    for z in range(1, 7):
        # Get file name
        file_name = join("instances", "instance{0}.txt".format(z))
        print("\n{0} file : {1}".format(z, file_name))

        # Read file data
        number_of_items, weight_constraint, items = get_data(file=file_name)

        # Display number of lines, weight and the volume
        print("\nNumber of Items:{0}, Weight constraint:{1}\n".format(number_of_items,
                                                                      weight_constraint))

        # Initialize item class
        item_object = Items(items=items)

        # Constants
        initial_temperature = 10000
        cooling_rate = 0.75
        iteration = 5
        epoch = 3
        termination_criteria = 0.001
        acceptance_criterion = 0.90

        sa_object = SA(items=items,
                       number_of_items=number_of_items,
                       item_object=item_object,
                       weight_constraint=weight_constraint,
                       initial_temperature=initial_temperature,
                       cooling_rate=cooling_rate,
                       iteration=iteration,
                       epoch=epoch,
                       termination_criteria=termination_criteria,
                       acceptance_criterion=acceptance_criterion)

        # Randomly initialed solution
        sa_object.first_improvement(initial_solution=sa_object.initial_solution)


if __name__ == "__main__":
    main()
