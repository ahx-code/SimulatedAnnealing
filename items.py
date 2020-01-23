class Items:
    def __init__(self, items):
        self.items = items

    def get_data_by_id(self, item_id):
        for item in self.items:
            _id = item[0]

            if item_id == _id:
                profit = item[1]
                weight = item[2]

                return profit, weight
