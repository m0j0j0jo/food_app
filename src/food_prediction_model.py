import time
from keras import layers
import keras
import numpy as np
import json
import queue


def get_key_from_value(d, val):
    bla = [k for k, v in d.items() if v == val]
    if len(bla) > 0:
        return bla[0]
    return None


class FoodPrediction():

    LAST_EAT_DAYS = 'LastEatDays'
    FOOD_NAME = 'food_name'
    TIME = 'time'

    def __init__(self, user_name):
        self.food_names = {}
        self.duration = 2
        self.food_json_path = f'../resource/{user_name}.json'
        self.parse_food_json()
        self.number_of_foods = len(self.food_names)
        self.size_x = self.number_of_foods + 3 # number of foods, time of day
        self.current_food_vector = [0] * self.size_x
        self.food_queue = queue.Queue(maxsize=self.duration)
        self.prepare_input()
        self.scores = []
        self.err = []

    def parse_food_json(self):
        with open(self.food_json_path, 'r') as file:
            self.data_dict = json.load(file)
        food_index = 0
        for food in self.data_dict['foods']:
            if self.food_names.get(food.get(self.FOOD_NAME)) is None:
                self.food_names[food.get(self.FOOD_NAME)] = food_index
                food_index += 1

    def prepare_input(self):
        self.input_file = []
        collect_x = np.array([])
        collect_y = np.array([])
        food_data = self.data_dict['foods']
        for food_data_index in range(len(food_data)-1):
            food_index = self.food_names[food_data[food_data_index+1].get(self.FOOD_NAME)]
            temp = np.zeros(self.number_of_foods)
            temp[food_index] = 1
            collect_y = np.append(collect_y, temp)
            collect_x = np.append(collect_x, self.get_data(food_data[food_data_index].get(self.FOOD_NAME),
                                                _time=food_data[food_data_index+1].get(self.TIME)))
        self.input_X = np.array(collect_x).reshape(-1, self.size_x)
        self.input_Y = np.array(collect_y).reshape(-1, self.number_of_foods)

    def get_model(self):
        self.model = keras.models.Sequential()
        self.model.add(keras.layers.Dense(25, input_dim=self.size_x, activation='relu'))
        self.model.add(keras.layers.Dense(10, activation='relu'))
        self.model.add(keras.layers.Dense(self.number_of_foods, activation='linear'))
        self.model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    def get_time_index(self, _time=None):
        if _time is None:
            food_time = time.localtime().tm_hour
        else:
            food_time = int(_time)

        if 5 <= food_time < 10:
            return self.number_of_foods
        elif 10 <= food_time < 15:
            return self.number_of_foods + 1
        else:
            return self.number_of_foods + 2

    def get_prediction_data(self, _time=None):
        food_time_index = self.get_time_index(_time)
        data = np.zeros(self.size_x)
        data[food_time_index] = 1
        return data + np.array(self.current_food_vector)

    def predict_food(self):
        """"
            data <vector of foods> <number of meal in day> <cold or hot weather>
        """
        prediction = self.model.predict(self.get_prediction_data().reshape(-1, self.size_x))
        food_prediction = get_key_from_value(self.food_names, np.argmax(prediction))
        return food_prediction

    def get_data(self, food_name, _time=None):
        data = np.zeros(self.size_x)
        data[self.get_time_index(_time)] = 1
        food_index = self.food_names[food_name]
        if self.food_queue.full():
            qfood_name = self.food_queue.get()
            qfood_index = self.food_names[qfood_name]
            self.current_food_vector[qfood_index] -= 1
        self.food_queue.put(food_name)
        self.current_food_vector[food_index] += 1
        data = data + np.array(self.current_food_vector)
        return data

    def input_data(self):
        collect_x = np.array([])
        collect_y = np.array([])
        for line in self.input_file:
            collect_x = np.append(collect_x, [line[0:self.size_x]])
            collect_y = np.append(collect_y, line[self.size_x:])
        self.input_X = np.array(collect_x).reshape(-1, self.size_x)
        self.input_Y = np.array(collect_y).reshape(-1, self.number_of_foods)

    def train_model(self):
        self.model.fit(self.input_X, self.input_Y)

    def run(self):
        self.get_model()
        self.train_model()


if __name__ == '__main__':
    food_perdication = FoodPrediction('user_name')
    food_perdication.run()
    print(food_perdication.predict_food())
