import json
import os

import numpy


def matrix_factorization(R, P, Q, K, steps=5000, alpha=0.0002, beta=0.02):
    '''
    R: rating matrix
    P: |U| * K (User features matrix)
    Q: |D| * K (Item features matrix)
    K: latent features
    steps: iterations
    alpha: learning rate
    beta: regularization parameter'''
    Q = Q.T

    for step in range(steps):
        for i in range(len(R)):
            for j in range(len(R[i])):
                if R[i][j] > 0:
                    # calculate error
                    eij = R[i][j] - numpy.dot(P[i,:],Q[:,j])

                    for k in range(K):
                        # calculate gradient with a and beta parameter
                        P[i][k] = P[i][k] + alpha * (2 * eij * Q[k][j] - beta * P[i][k])
                        Q[k][j] = Q[k][j] + alpha * (2 * eij * P[i][k] - beta * Q[k][j])

        eR = numpy.dot(P,Q)

        e = 0

        for i in range(len(R)):

            for j in range(len(R[i])):

                if R[i][j] > 0:

                    e = e + pow(R[i][j] - numpy.dot(P[i,:],Q[:,j]), 2)

                    for k in range(K):

                        e = e + (beta/2) * (pow(P[i][k],2) + pow(Q[k][j],2))
        # 0.001: local minimum
        if e < 0.001:

            break

    return P, Q.T


class FoodScores():

    LAST_EAT_DAYS = 'LastEatDays'
    FOOD_NAME = 'food_name'
    TIME = 'time'
    SCORE = 'score'

    def __init__(self, food_features=3):
        self.food_index = {}
        self.user_index = {}
        self.user_score_matrix_data = []
        self.food_dir_path = f'../resource/'
        self.create_user_score_matrix()
        self.calculate_user_score_matrix(food_features)

    def create_user_score_matrix(self):
        food_index = 0
        user_index = 0
        for user_json_path in os.listdir(self.food_dir_path):
            with open(user_json_path, 'r') as file:
                data = json.load(file)
                #todo parse user name
                self.user_index[user_json_path] = user_index
                user_index += 1
            #todo
            temp = [0]*food_index
            for food in data['foods']:
                if not self.food_index.get(food[self.FOOD_NAME]):
                    self.food_index[food[self.FOOD_NAME]] = food_index
                    if len(temp) <= food_index:
                        temp.append(self.food_index.get(food[self.SCORE]))
                    #todo this case should not happen
                    else:
                        temp[self.food_index.get(food[self.FOOD_NAME])] = self.food_index.get(food[self.SCORE])
                    food_index += 1
                else:
                    temp[self.food_index.get(food[self.FOOD_NAME])] = self.food_index.get(food[self.SCORE])

            #todo adjast matrix sizes

    def user_scores(self, user_name):
        return self.user_score_matrix[self.user_index[user_name]]

    def calculate_user_score_matrix(self, food_features):
        self.user_score_matrix_data = numpy.array(self.user_score_matrix_data)
        # N: num of User
        N = len(self.user_score_matrix_data)
        # M: num of Movie
        M = len(self.user_score_matrix_data[0])
        # Num of Features
        K = food_features
        P = numpy.random.rand(N, K)
        Q = numpy.random.rand(M, K)
        nP, nQ = matrix_factorization(self.user_score_matrix_data, P, Q, K)
        self.user_score_matrix = numpy.dot(nP, nQ.T)

if __name__ == '__main__':
    food_score = FoodScores()
    print(food_score.user_scores('user_name'))