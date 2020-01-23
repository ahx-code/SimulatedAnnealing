from random import choice
from math import exp


class SA:
    def __init__(self,
                 items,
                 number_of_items,
                 item_object,
                 weight_constraint,
                 initial_temperature,
                 cooling_rate,
                 iteration,
                 epoch,
                 termination_criteria,
                 acceptance_criterion):
        self.items = items
        self.number_of_items = number_of_items
        self.item_object = item_object
        self.weight_constraint = weight_constraint
        self.initial_temperature = initial_temperature
        self.cooling_rate = cooling_rate
        self.iteration = iteration
        self.epoch = epoch
        self.termination_criteria = termination_criteria
        self.acceptance_criterion = acceptance_criterion
        self.all_keys = [item[0] for item in self.items]
        self.item_x_keys = []
        self.item_y_keys = []
        self.initial_solution, self.total_profit, self.total_weight = self.random_initial_solution()

    def random_initial_solution(self):
        """

        :return: Randomly initialized solution
        """
        solution = {}

        total_weight = 0
        total_profit = 0

        while total_weight <= self.weight_constraint:
            item_x_id = choice(self.all_keys)
            if item_x_id not in solution.keys():
                item_profit, item_weight = self.item_object.get_data_by_id(item_id=item_x_id)
                if total_weight + item_weight <= self.weight_constraint:
                    total_weight += item_weight
                    total_profit += item_profit
                    #  Add item profit with the acceptance percent
                    solution[item_x_id] = [item_profit, 100.0]
                else:
                    break

        print("\nInitial Solution: {0}\nTotal Profit: {1}\nTotal Weight: {2}\n\n".format(solution,
                                                                                         total_profit,
                                                                                         total_weight))

        return solution, total_profit, total_weight

    def first_improvement(self, initial_solution):
        self.item_x_keys = [key for key in initial_solution.keys()]
        self.item_y_keys = self.add_item_y_keys(item_x_keys=self.item_x_keys)
        sa_solution = initial_solution.copy()

        sa_weight = self.total_weight
        sa_profit = self.total_profit

        for i in range(0, self.iteration):
            for _ in range(0, self.epoch):

                # Algorithm should stop when the temperature achieves a very small value
                if self.initial_temperature <= self.termination_criteria:
                    break

                try:
                    item_x_id = choice(self.item_x_keys)
                    item_y_id = choice(self.item_y_keys)
                except IndexError as i_error:
                    print("\nKey list is empty: {0} \n".format(i_error))
                    return

                item_x_profit, item_x_weight = self.item_object.get_data_by_id(item_id=item_x_id)
                item_y_profit, item_y_weight = self.item_object.get_data_by_id(item_id=item_y_id)

                # Check whether swapping the selected items are feasible with respect to the capacity
                check_capacity = (sa_weight - item_x_weight + item_y_weight <= self.weight_constraint)
                check_feasibility = item_y_profit > item_x_profit

                # Metropolis criterion
                if check_capacity and check_feasibility:
                    # Swap
                    sa_solution.pop(item_x_id)

                    # Add
                    sa_solution[item_y_id] = item_y_profit

                    # Update weight and profit
                    sa_weight = sa_weight - item_x_weight + item_y_weight
                    sa_profit = sa_profit - item_x_profit + item_y_profit

                    # Update key list
                    self._update_keys(item_x_id=item_x_id,
                                      item_y_id=item_y_id)

                elif check_capacity:
                    # When item profit is not feasible, accept with the metropolis criterion
                    metropolis_criterion = exp(((item_y_profit - item_x_profit) / self.initial_temperature))

                    if metropolis_criterion > self.acceptance_criterion:
                        # Swap
                        sa_solution.pop(item_x_id)

                        # Add
                        sa_solution[item_y_id] = [item_y_profit, metropolis_criterion]
                        self.initial_temperature *= self.cooling_rate

                        # Update weight and profit
                        sa_weight = sa_weight - item_x_weight + item_y_weight
                        sa_profit = sa_profit - item_x_profit + item_y_profit

                        # Update key list
                        self._update_keys(item_x_id=item_x_id,
                                          item_y_id=item_y_id)

            print("\nIteration#{0} SA Solution: {1}\nSA Profit: {2}\nSA Weight: {3}\n\n".format(str(i + 1),
                                                                                                sa_solution,
                                                                                                sa_profit,
                                                                                                sa_weight))

        return sa_solution, sa_profit, sa_weight

    def _update_keys(self, item_x_id, item_y_id):
        self.item_x_keys.remove(item_x_id)
        self.item_y_keys.remove(item_y_id)
        self.item_x_keys.append(item_y_id)
        self.item_y_keys.append(item_x_id)

    def add_item_y_keys(self, item_x_keys):
        item_y_keys = []
        for key in range(0, self.number_of_items):
            if key not in item_x_keys:
                item_y_keys.append(key)

        return item_y_keys
