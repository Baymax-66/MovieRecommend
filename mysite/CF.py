# coding: utf-8 -*-
import math
import pandas as pd
import numpy as np
# 更改输入的接口
# input：用户的所有的信息:UserTable：UserID,Age,Sex(1:男，0:女); 类型：字典类型或者DataFrame
#       电影的所有的信息:MovieTable: MovieID,Hours,Rating,ProduceTime(eg. 1999),SearchTimes,LikeTimes；类型：字典类型或者DataFrame
#       用户记录:UserLoggingTable:UserID,MovieID,IsLike(boolean),Rating；类型：字典类型或者DataFrame
#       目标用户ID：TargetUserID
#       推荐数量： TopK


class UserCf:

    def __init__(self, targetUserID, topK,userTable, movieTable,userLoggingTable):
        self.TargetUserID = targetUserID
        self.TopK = topK
        self.UserTable = userTable
        self.FilmTable = movieTable
        self.UserLoggingTable = {'UserID':[],'MovieID':[],'Rating':[]}

        for e in userLoggingTable:
            self.UserLoggingTable['UserID'].append(e.UserID_id)
            self.UserLoggingTable['MovieID'].append(e.MovieID_id)
            self.UserLoggingTable['Rating'].append(e.Rating)


        self.top_n_movies = None
        self._init_frame()
        self.calculate()

    def _init_frame(self):

        self.frame = pd.DataFrame(self.UserLoggingTable)
        self.calculate()

    def get_target_movie_times(self):
        pass

    def get_top_n_hot_movie(self,top_n_hot = 10):
        """
        返回现在最热的前n个电影，主要根据用户的评分和来计算
        :return:
        """

        Rating = self.UserLoggingTable['Rating']
        MovieId = self.UserLoggingTable['MovieID']
        # tmp = [MovieRating()]*(len(Rating))
        # (sumRating,times)
        # 统计好之后求平均分后取前n个

        # sumRating = [(0,0)]*(max(MovieId)+1)
        sumRating = np.zeros((max(MovieId)+1,2))
        ave = np.zeros((max(MovieId)+1,))

        for i in range(len(self.UserLoggingTable)):
            sumRating[MovieId[i]][0]+=Rating[i]
            sumRating[MovieId[i]][1]+=1
        for i in range(len(sumRating)):
            if sumRating[i][0]!=0:
                ave[i] = sumRating[i][0]/sumRating[i][1]

        # >> > a = [1, 5, 1, 4, 3, 4, 4]  # First column
        # >> > b = [9, 4, 0, 4, 0, 2, 1]  # Second column
        # >> > ind = np.lexsort((b, a))  # Sort by a, then by b
        ind = np.lexsort((-ave,-sumRating[:,1],-sumRating[:,0]))
        # argRating = np.argsort(-np.array(ave))
        return ind[:top_n_hot+1]

    @staticmethod
    def _cosine_sim(target_movies, movies):
        '''

        simple method for calculate cosine distance.
        e.g: x = [1 0 1 1 0], y = [0 1 1 0 1]
             cosine = (x1*y1+x2*y2+...) / [sqrt(x1^2+x2^2+...)+sqrt(y1^2+y2^2+...)]
             that means union_len(movies1, movies2) / sqrt(len(movies1)*len(movies2))
        '''
        union_len = len(set(target_movies) & set(movies))
        if union_len == 0: return 0.0
        product = len(target_movies) * len(movies)
        cosine = union_len / math.sqrt(product)
        return cosine

    def _get_top_n_users(self, target_user_id, top_n):
        '''
        calculate similarity between all users and return Top N similar users.
        '''
        target_movies = self.frame[self.frame['UserID'] == target_user_id]['MovieID']
        # print(target_movies)
        other_users_id = [i for i in set(self.frame['UserID']) if i != target_user_id]
        # print(other_users_id)
        other_movies = [self.frame[self.frame['UserID'] == i]['MovieID'] for i in other_users_id]
        sim_list = [self._cosine_sim(target_movies, movies) for movies in other_movies]
        sim_list = sorted(zip(other_users_id, sim_list), key=lambda x: x[1], reverse=True)
        self.top_n_users = sim_list[:top_n]
        return sim_list[:top_n]

    def _get_candidates_items(self, target_user_id):
        """
        Find all movies in source data and target_user did not meet before.
        """
        target_user_movies = set(self.frame[self.frame['UserID'] == target_user_id]['MovieID'])
        # other_user_movies = set(self.frame[self.frame['UserID'] != target_user_id]['MovieID'])
        other_user_movies = set([])
        for u,_ in self.top_n_users:
            tmp = set(self.frame[self.frame['UserID'] == u]['MovieID'])
            other_user_movies = other_user_movies | tmp
        # candidates_movies = list(target_user_movies ^ other_user_movies)
        candidates_movies = list(other_user_movies - target_user_movies)
        return candidates_movies

    def _get_top_n_items(self, top_n_users, candidates_movies, top_n):
        """
        calculate interest of candidates movies and return top n movies.
        e.g. interest = sum(sim * normalize_rating)
        """
        # 前n个用户的数据
        top_n_user_data = [self.frame[self.frame['UserID'] == k] for k, _ in top_n_users]
        # 最后返回的结果
        interest_list = []
        # 针对每一个候选的电影
        for movie_id in candidates_movies:
            tmp = []
            for user_data in top_n_user_data:
                # 如果候选的电影在前n个用户的电影中
                if movie_id in user_data['MovieID'].values:
                    tmp.append(user_data[user_data['MovieID'] == movie_id]['Rating'].values[0]/5)
                else:
                    tmp.append(0)
            interest = sum([top_n_users[i][1] * tmp[i] for i in range(len(top_n_users))])
            interest_list.append((movie_id, interest))
        interest_list = sorted(interest_list, key=lambda x: x[1], reverse=True)
        return interest_list[:top_n]

    def calculate(self):
        """
        user-cf for movies recommendation.
        """
        # most similar top n users
        target_user_id = self.TargetUserID
        top_n = self.TopK

        # 找到和目标用户喜好相同的前n个用户
        top_n_users = self._get_top_n_users(target_user_id, top_n)
        # candidates movies for recommendation
        # 候选的电影主要是当前用户没看过的其他所有的用户看过的电影
        candidates_movies = self._get_candidates_items(target_user_id)
        print(len(candidates_movies))
        # most interest top n movies
        top_n_movies = self._get_top_n_items(top_n_users, candidates_movies, top_n)

        self.top_n_movies = top_n_movies
        return top_n_movies
