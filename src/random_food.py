import json
import random


class FoodProbability:

    FOOD_NAME = 'food_name'
    TIME = 'time'
    SCORE = 'score'

    def __init__(self, user_name):
        self.food_data = {}
        self.food_json_path = f'../resource/{user_name}.json'
        self.create_food_data()
        food_sum = sum(self.food_data.values())
        self.probability = {key: val / food_sum for key, val in self.food_data.items()}

    def create_food_data(self):
        with open(self.food_json_path, 'r') as file:
            data = json.load(file)
            for food in data['foods']:
                number_of_food = self.food_data.get(food[self.FOOD_NAME], 0) + 1
                self.food_data[food[self.FOOD_NAME]] = number_of_food

    def random_food(self):
        random_0_to_1 = random.random()
        p_sum = 0
        for food, p in self.probability.items():
            p_sum += p
            if random_0_to_1 < p_sum:
                return food
        return None


if __name__ == '__main__':
    food_probability_class = FoodProbability('user_name')
    print(food_probability_class.random_food())
