from src.myjsonhandler import *
from src.mymathhelper import *


class TrainingSet:
    def __init__(self):
        # Initialize Variables
        self.training_set = []  # List of Lists containing input data from file
        self.training_set_transposed = []  # Transposed of training set - used to calculate similarity matrix
        self.net_training_set = []
        self.movie_popularity = []  # Static Movie Popularity - no personalization
        self.movie_movie_similarity_matrix = []  # Keeps the similarity between every movie
        self.user_user_similarity_matrix = []
        self.user_ratings_count = []
        self.movie_ratings_count = []
        self.file_paths = {
            'training_set': '../data/json/training_set.json',
            'training_set_transposed': '../data/json/training_set_transposed.json',
            'movie_popularity': '../data/json/movie_popularity.json',
            'movie_movie_similarity_matrix': '../data/json/movie_movie_similarity_matrix.json',
            'user_user_similarity_matrix': '../data/json/user_user_similarity_matrix.json',
            'movie_ratings_count': '../data/json/movie_ratings_count.json',
            'user_ratings_count': '../data/json/user_ratings_count.json',
            'net_training_set': '../data/json/net_training_set.json'
        }

    # Will read from files and save to json
    def read_from_files(self, file_path):
        """
        Read Input from file and create all matrix
        """
        self.read_training_file(file_path)
        self.create_transposed_training_set()
        self.create_movie_popularity_list()
        self.create_movie_movie_similarity_matrix()
        self.create_user_user_similarity_matrix()
        self.create_user_ratings_count_list()
        self.create_movie_ratings_count_list()
        self.create_net_training_file()

    def read_from_json(self):
        """
        Already created Matrix - read from json file
        """
        self.training_set = MyJsonHandler.get_data_from_json_file(self.file_paths['training_set'])
        self.training_set_transposed = MyJsonHandler.get_data_from_json_file(self.file_paths['training_set_transposed'])
        self.movie_popularity = MyJsonHandler.get_data_from_json_file(self.file_paths['movie_popularity'])
        self.movie_movie_similarity_matrix = MyJsonHandler.get_data_from_json_file(
            self.file_paths['movie_movie_similarity_matrix'])
        self.user_user_similarity_matrix = MyJsonHandler.get_data_from_json_file(
            self.file_paths['user_user_similarity_matrix'])
        self.movie_ratings_count = MyJsonHandler.get_data_from_json_file(self.file_paths['movie_ratings_count']),
        self.user_ratings_count = MyJsonHandler.get_data_from_json_file(self.file_paths['user_ratings_count']),
        self.net_training_set = MyJsonHandler.get_data_from_json_file(self.file_paths['net_training_set'])

    def read_training_file(self, file_path):
        """
        Read Training data file from input file and saves it in json format
        """
        with open(file_path) as f:
            for line in f:
                row = []
                split = line.split('\t')
                for value in split:
                    row.append(int(value))
                self.training_set.append(row)
        MyJsonHandler.save_data_to_json_file(self.training_set, self.file_paths['training_set'])

    def create_net_training_file(self):
        """
        creates the matrix for the net values for self.training_set
        """
        for i in range(0, len(self.training_set)):
            my_list = MyMathHelper.net_list(self.training_set[i], self.user_ratings_count[i])
            self.net_training_set.append(my_list)
        MyJsonHandler.save_data_to_json_file(self.net_training_set, self.file_paths['net_training_set'])

    # Transposes Training set so its 1000 rows (# movies) and 200 columns (# users)
    def create_transposed_training_set(self):
        """
        transposes self.training set
        """
        for i in range(0, len(self.training_set[0])):
            my_list = []
            for j in range(0, len(self.training_set)):
                my_list.append(self.training_set[j][i])
            self.training_set_transposed.append(my_list)
        MyJsonHandler.save_data_to_json_file(self.training_set_transposed, self.file_paths['training_set_transposed'])

    def create_user_ratings_count_list(self):
        """
        counts the number of movies that the user rated
        """
        for row in self.training_set:
            counter = MyMathHelper.nonzero_count(row)
            self.user_ratings_count.append(counter)
        MyJsonHandler.save_data_to_json_file(self.user_ratings_count, self.file_paths['user_ratings_count'])

    def create_movie_ratings_count_list(self):
        """
        counts the number of users that rated the movie
        """
        for row in self.training_set_transposed:
            counter = 0
            for value in row:
                if value != 0:
                    counter += 1
            self.movie_ratings_count.append(counter)
        MyJsonHandler.save_data_to_json_file(self.movie_ratings_count, self.file_paths['movie_ratings_count'])

    def create_movie_popularity_list(self):
        """
         This produces a list of the average ratings for every movie
         *Note: This average does not include the '0's or non-explicit ratings
        """
        for i in range(0, len(self.training_set)):
            counter = 0
            total_popularity = 0
            for j in range(0, len(self.training_set[i])):
                if self.training_set[i][j] != 0:
                    counter += 1
                    total_popularity += self.training_set[i][j]
            if counter == 0:
                counter += 1
            avg = total_popularity / counter
            self.movie_popularity.append(avg)
            MyJsonHandler.save_data_to_json_file(self.movie_popularity, self.file_paths['movie_popularity'])

    def create_movie_movie_similarity_matrix(self):
        """
        Creates the cosine similarity matrix for Movie to Movie and saves to json file
        """
        counter = 0
        for i in range(0, len(self.training_set_transposed)):
            my_list = []
            for j in range(0, len(self.training_set_transposed)):
                counter += 1
                print counter
                my_list.append(MyMathHelper.custom_cosine_similarity(self.training_set_transposed[i],
                                                                  self.training_set_transposed[j])[0])
            self.movie_movie_similarity_matrix.append(my_list)
        MyJsonHandler.save_data_to_json_file(self.movie_movie_similarity_matrix,
                                             self.file_paths['movie_movie_similarity_matrix'])

    def create_user_user_similarity_matrix(self):
        """
        Creates the cosine similarity matrix for User to User
        """
        counter = 0
        for i in range(0, len(self.training_set)):
            my_list = []
            for j in range(0, len(self.training_set)):
                counter += 1
                print counter
                my_list.append(MyMathHelper.custom_cosine_similarity(self.training_set[i], self.training_set[j])[0])
            self.user_user_similarity_matrix.append(my_list)
        MyJsonHandler.save_data_to_json_file(self.user_user_similarity_matrix,
                                             self.file_paths['user_user_similarity_matrix'])
