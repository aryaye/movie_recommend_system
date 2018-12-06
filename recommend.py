# -*- coding: utf-8 -*-
from math import log


class HHMRecommend:
    def __init__(self):
        self.n_users = 0
        self.n_films = 0
        self.users = 0
        self.films = 0
        self.rating_matrix = []
        self.films_rating_average = []
        self.k = 0
        self.probZ = []
        self.probRgivenZ = []

    def add_matrix(self, matrixs):
        self.rating_matrix = matrixs
        self.n_users = len(matrixs)
        self.n_films = len(matrixs[0])

    def add_title(self, users, films):
        self.users = users
        self.films = films

    def trivial_model(self):
        ans = []
        for j in range(self.n_films):
            good = 0
            know = 0
            for i in range(self.n_users):
                if self.rating_matrix[i][j] >= 0:
                    know += 1
                    if self.rating_matrix[i][j] == 1:
                        good += 1
            self.films_rating_average.append(1.0*good/know)
            ans.append([1.0*good/know, self.films[j]])
        ans.sort()
        return ans

    def hhm_algorithms(self, probZ, probRgivenZ):
        self.probZ = probZ
        self.probRgivenZ = probRgivenZ
        k = len(probZ)
        self.k = k
        rti = [[0 for _ in range(k)] for _ in range(self.n_users)]
        iterations = 0
        while True:
            # E_step
            if iterations in [0, 1, 2, 4, 8, 16, 32, 64, 128]:
                print('log_likelihood', iterations, self.log_likelihood())
            for t in range(self.n_users):
                pzv = []
                for i in range(k):
                    temp = 1
                    for j in range(self.n_films):
                        if self.rating_matrix[t][j] == 1:
                            temp *= self.probRgivenZ[j][i]
                        elif self.rating_matrix[t][j] == 0:
                            temp *= (1-self.probRgivenZ[j][i])
                    pzv.append(self.probZ[i]*temp)
                sums = sum(pzv)
                rti[t] = [x/sums for x in pzv]
            # M-step
            err = 0
            # p(z=i)
            for i in range(k):
                temp = 0
                for t in range(self.n_users):
                    temp += rti[t][i]
                # calculate err between two iterations
                err += (self.probZ[i]-temp/self.n_users)**2
                self.probZ[i] = temp/self.n_users
            # p(rj = 1 | z=i)
            for i in range(k):
                for j in range(self.n_films):
                    temp = 0
                    for t in range(self.n_users):
                        if self.rating_matrix[t][j] == 1:
                            temp += rti[t][i]
                        elif self.rating_matrix[t][j] == -1:
                            temp += rti[t][i]*self.probRgivenZ[j][i]
                    # calculate err between two iterations
                    err += (self.probRgivenZ[j][i] - temp/(self.n_users*probZ[i]))**2
                    self.probRgivenZ[j][i] = temp/(self.n_users*probZ[i])
            iterations += 1
            if err <= 0.01 and iterations >= 129:
                break

    def log_likelihood(self):
        logs = 0
        for t in range(self.n_users):
            temp = 0
            for i in range(self.k):
                multi = 1
                for j in range(self.n_films):
                    if self.rating_matrix[t][j] == 1:
                        multi *= self.probRgivenZ[j][i]
                    elif self.rating_matrix[t][j] == 0:
                        multi *= (1 - self.probRgivenZ[j][i])
                temp += self.probZ[i]*multi
            logs += log(temp)
        return logs/self.n_users

    def personal_recommend(self, pid):
        t = self.users.index(pid)
        ans = []
        pzv = []
        for i in range(self.k):
            temp = 1
            for j in range(self.n_films):
                if self.rating_matrix[t][j] == 1:
                    temp *= self.probRgivenZ[j][i]
                elif self.rating_matrix[t][j] == 0:
                    temp *= (1 - self.probRgivenZ[j][i])
            pzv.append(self.probZ[i] * temp)
        sums = sum(pzv)
        pzv = [x / sums for x in pzv]
        for j in range(self.n_films):
            if self.rating_matrix[t][j] == -1:
                temp = 0
                for i in range(self.k):
                    temp += pzv[i]*self.probRgivenZ[j][i]
                ans.append([temp, j])
        ans.sort()
        ans = [[p, self.films[j]] for p, j in ans]
        return ans


def main():
    with open(r'C:\\Users\Haiya Ye\PycharmProjects\EM_recsys\hw8_movieTitles_fa18.txt', 'r') as f:
        movieTitles = f.read().split('\n')
    with open(r'C:\\Users\Haiya Ye\PycharmProjects\EM_recsys\hw8_probRgivenZ_init.txt', 'r') as f:
        probRgivenZ = f.read().split('\n')
    probRgivenZ = [[float(a) for a in x.split('   ')[1:]] for x in probRgivenZ]
    with open(r'C:\\Users\Haiya Ye\PycharmProjects\EM_recsys\hw8_ratings_fa18.txt', 'r') as f:
        ratings = f.read().split('\n')
    for i in range(len(ratings)):
        ratings[i] = ratings[i].split(' ')
        for j in range(len(ratings[i])):
            if ratings[i][j] == '?':
                ratings[i][j] = -1
            else:
                ratings[i][j] = int(ratings[i][j])
    with open(r'C:\\Users\Haiya Ye\PycharmProjects\EM_recsys\hw8_probZ_init.txt', 'r') as f:
        probZ = f.read().split('\n')[:-1]
    probZ = [float(x) for x in probZ]
    with open(r'C:\\Users\Haiya Ye\PycharmProjects\EM_recsys\hw8_studentPIDs_fa18.txt', 'r') as f:
        studentPIDs = f.read().split('\n')

    recommend = HHMRecommend()
    recommend.add_matrix(ratings)
    recommend.add_title(studentPIDs,movieTitles)
    task1 = recommend.trivial_model()
    for k in task1:
        print(k[1])
    recommend.hhm_algorithms(probZ, probRgivenZ)
    task2 = recommend.personal_recommend('A53290644')
    for k in task2:
        print(k[1])


if __name__ == '__main__':
    main()