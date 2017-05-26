from src.mymathhelper import *


class Prediction():
    def __init__(self, training_set):
        self.training_set = training_set

    def custom_all_static_weighted_average(self, user_cf_weight, movie_cf_weight, movie_popularity_weight,
                                           user_cf_value, movie_cf_value, movie_popularity):
        value = user_cf_weight * user_cf_value + movie_cf_value * movie_cf_weight + movie_popularity * movie_popularity_weight
        value /= (user_cf_weight + movie_cf_weight + movie_popularity_weight)
        return value

    ###############################################################################################################
    #                                               Movie Avg                                                     #
    ###############################################################################################################
    def movie_average(self):
        return 0

    ###############################################################################################################
    #                                                 Cosine                                                      #
    ###############################################################################################################

    def find_closest_users_cosine(self, user_vector, movie, k):
        """
        This is the Kth- nearest neighbor algorithm
        """
        closest_users = [(0, 0, 0, 0, 0)] * k
        # ( User Index, Cosine Similarity Weight, Movie Rating, V1, V2) Note* V1, V2 after common_dimensions()
        for i in range(0, len(self.training_set)):
            # print 'i:',i
            # print movie
            if self.training_set[i][movie] != 0:  # Makes sure the user has that movie rating
                # print 'v1_before:' , v1
                # print 'v2_after:', v2
                temp = MyMathHelper.common_dimensions(self.training_set[i], user_vector)
                v1 = temp[0]  # Reduces to common dimensions
                v2 = temp[1]  # Reduces to common dimensions
                print 'v1:', v1
                print 'v2:', v2
                value = MyMathHelper.custom_cosine_similarity(v1, v2)[1]
                # print value
                # print closest_users
                if abs(value) > closest_users[0][1]:  # Absolute Value
                    del closest_users[0]  # Delete smallest value
                    closest_users.append((i, value, self.training_set[i][movie], v1, v2))  # Add new value to end
                    # print closest_users
                    closest_users = sorted(closest_users, key=lambda tup: tup[1])  # sort in increasing order
        return closest_users

    def user_user_cosine_similarity(self, user_vector, movie, k):
        """
        Calculates the Weighted Average
        k = top k for nearest neighbor algorithm
        movie - movie index to only include close users that rated that specific movie
        """
        closest_users = self.find_closest_users_cosine(user_vector, movie, k)
        print 'Closest users:', closest_users
        prediction = 0
        denominator = 0
        for u in closest_users:
            if u == (0, 0, 0,0,0):
                continue
            weight = MyMathHelper.custom_case_amplification(u[1])
            movie_rating = u[2]
            prediction += (weight * movie_rating)
            denominator += weight
        try:
            prediction /= denominator
        except Exception, e:
            print 'Error in user_user_cosine_similarity:',e
            return 3
        print prediction
        return prediction

    ###############################################################################################################
    #                                                 PEARSON                                                     #
    ###############################################################################################################

    def user_user_pearson(self, user_vector, movie, k):
        """
        Calculates the Weighted Average
        k = top k for nearest neighbor algorithm
        movie - movie index to only include close users that rated that specific movie
        """

        closest_users = self.find_closest_users_pearson(user_vector, movie, k)
        print closest_users
        prediction = 0
        denominator = 0
        for u in closest_users:

            weight = u[1]
            weight = MyMathHelper.custom_case_amplification(weight)
            training_set_user_movie_score = u[2]
            training_set_user_avg = u[3]
            testing_user_avg = u[4]
            if weight != 0:  # todo THIS SHOULD BE HAPPENING???
                denominator += abs(weight)
                prediction += (testing_user_avg +
                               ((weight * (training_set_user_movie_score - training_set_user_avg)) / abs(weight)))
        if denominator == 0:  # todo CASE WHEN NOBODY RATED THE MOVIE?
            print 3
            return 3
        prediction /= denominator
        print prediction
        prediction = MyMathHelper.custom_rounding(prediction)
        print 'Rounded Predicion:', prediction
        return prediction

    def find_closest_users_pearson(self, user_vector, movie, k):
        """
        This is the Kth- nearest neighbor algorithm
        """
        closest_users = [(0, 0, 0, 0, 0,0,0)] * k  # top K user
        for i in range(0, len(self.training_set)):
            # print 'i:',i
            # print movie
            if self.training_set[i][movie] != 0:  # Makes sure the user has that movie rating
                # print 'v1_before:' , v1
                # print 'v2_after:', v2
                temp = MyMathHelper.common_dimensions(self.training_set[i], user_vector)
                v1 = temp[0]
                v2 = temp[1]
                net_v1 = MyMathHelper.net_list(v1, MyMathHelper.nonzero_count(v1))  # Reduces to common dimensions
                net_v2 = MyMathHelper.net_list(v2, MyMathHelper.nonzero_count(v2))  # Reduces to common dimensions
                value = MyMathHelper.custom_cosine_similarity(net_v1, net_v2)[1]
                # print value
                # print closest_users
                if abs(value) > closest_users[0][1]:  # Absolute Value
                    del closest_users[0]  # Delete smallest value
                    closest_users.append((i, value, self.training_set[i][movie],
                                          MyMathHelper.get_average(self.training_set[i]),
                                          MyMathHelper.get_average(user_vector),
                                          v1,v2))  # Add new value to end
                    # print closest_users
                    closest_users = sorted(closest_users, key=lambda tup: tup[1])  # sort in increasing order
        return closest_users

