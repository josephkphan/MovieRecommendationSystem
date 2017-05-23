import math, json


class TrainingSet():
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
        self.training_set = self.get_data_from_json_file(self.file_paths['training_set'])
        self.training_set_transposed = self.get_data_from_json_file(self.file_paths['training_set_transposed'])
        self.movie_popularity = self.get_data_from_json_file(self.file_paths['movie_popularity'])
        self.movie_movie_similarity_matrix = self.get_data_from_json_file(
            self.file_paths['movie_movie_similarity_matrix'])
        self.user_user_similarity_matrix = self.get_data_from_json_file(self.file_paths['user_user_similarity_matrix'])
        self.movie_ratings_count = self.get_data_from_json_file(self.file_paths['movie_ratings_count']),
        self.user_ratings_count = self.get_data_from_json_file(self.file_paths['user_ratings_count']),
        self.net_training_set = self.get_data_from_json_file(self.file_paths['net_training_set'])

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
        print len(self.training_set)
        self.save_data_to_json_file(self.training_set, self.file_paths['training_set'])

    def create_net_training_file(self):
        """
        creates the matrix for the net values for self.training_set
        """
        for i in range(0, len(self.training_set)):
            avg = sum(self.training_set[i]) / self.user_ratings_count[i]
            list = self.create_net_list(self.training_set[i], self.user_ratings_count[i])
            self.net_training_set.append(list)
        self.save_data_to_json_file(self.net_training_set, self.file_paths['net_training_set'])

    def create_net_list(self, list, count):
        """
        Finds the average of the list
        count is used for the denominator for the average equation (# non zero values for list for movie case)
        """
        avg = sum(list) / count
        net_list = []
        for i in range(0, len(list)):
            net_list.append(list[i] - avg)
        return net_list

    # Transposes Training set so its 1000 rows (# movies) and 200 columns (# users)
    def create_transposed_training_set(self):
        """
        transposes self.training set
        """
        for i in range(0, len(self.training_set[0])):
            list = []
            for j in range(0, len(self.training_set)):
                list.append(self.training_set[j][i])
            self.training_set_transposed.append(list)
        print len(self.training_set_transposed)
        print len(self.training_set_transposed[0])
        self.save_data_to_json_file(self.training_set_transposed, self.file_paths['training_set_transposed'])

    def get_nonzero_count(self, list):
        """
        takes in a list an returns the amount of non zero values in the list
        """
        counter = 0
        for value in list:
            if value != 0:
                counter += 1
        return counter

    def create_user_ratings_count_list(self):
        """
        counts the number of movies that the user rated
        """
        for row in self.training_set:
            counter = self.get_nonzero_count(row)
            self.user_ratings_count.append(counter)
        self.save_data_to_json_file(self.user_ratings_count, self.file_paths['user_ratings_count'])

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
        self.save_data_to_json_file(self.movie_ratings_count, self.file_paths['movie_ratings_count'])

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
            self.save_data_to_json_file(self.movie_popularity, self.file_paths['movie_popularity'])

    def cosine_similarity(self, v1, v2):
        """
        compute cosine similarity of v1 to v2: (v1 dot v2)/{||v1||*||v2||)
        **Note: This cosine similarity only compares the similar dimensions of the two vectors
        """
        temp = self.get_common_dimensions(v1, v2)
        v1 = temp[0]        # Reduces to common dimensions
        v2 = temp[1]        # Reduces to common dimensions
        sumxx, sumxy, sumyy, cosine = 0, 0, 0, 0
        for i in range(len(v1)):
            x = v1[i]
            y = v2[i]
            sumxx += x * x
            sumyy += y * y
            sumxy += x * y
            try:
                cosine = sumxy / math.sqrt(sumxx * sumyy)   # Calculate Cosine Similarity
            except Exception, e:
                cosine = 0      # Edge case when denominator is 0
        return cosine

    def get_common_dimensions(self, v1, v2):
        """
        takes in two vectors and returns a tuple of the vectors with both non zero dimensions
        i.e.
        v1 : [ 1, 2, 3, 0 ]        -->      return [2, 3]
        v2 : [ 0, 4, 5, 6 ]        -->      return [4, 5]
        """
        list1, list2 = [], []
        for i in range(0, len(v1)):
            if v1[i] != 0 and v2[i] != 0:
                list1.append(v1[i])
                list2.append(v2[i])
        return list1, list2

    def get_euclidean_distance(self, vector1, vector2):
        """
        calculate and return the euclidean distance
        """
        dist = [(a - b) ** 2 for a, b in zip(vector1, vector2)]
        dist = math.sqrt(sum(dist))
        return dist

    def create_movie_movie_similarity_matrix(self):
        """
        Creates the cosine similarity matrix for Movie to Movie and saves to json file
        """
        counter = 0
        for i in range(0, len(self.training_set_transposed)):
            list = []
            for j in range(0, len(self.training_set_transposed)):
                counter += 1
                print counter
                list.append(self.cosine_similarity(self.training_set_transposed[i], self.training_set_transposed[j]))
            self.movie_movie_similarity_matrix.append(list)
        self.save_data_to_json_file(self.movie_movie_similarity_matrix,
                                    self.file_paths['movie_movie_similarity_matrix'])

    def create_user_user_similarity_matrix(self):
        """
        Creates the cosine similarity matrix for User to User
        """
        counter = 0
        for i in range(0, len(self.training_set)):
            list = []
            for j in range(0, len(self.training_set)):
                counter += 1
                print counter
                list.append(self.cosine_similarity(self.training_set[i], self.training_set[j]))
            self.user_user_similarity_matrix.append(list)
        self.save_data_to_json_file(self.user_user_similarity_matrix, self.file_paths['user_user_similarity_matrix'])

    @staticmethod
    def save_data_to_json_file(data, file_path):
        """
        Store data as json in designated file_path
        """
        out_file = open(file_path, "w")
        json.dump(data, out_file, indent=4)
        out_file.close()

    @staticmethod
    def get_data_from_json_file(file_path):
        """
        get data as json in designated file_path
        """
        try:
            with open(file_path) as f:
                return json.load(f)
        except IOError as e:
            print 'could not read ' + file_path

            #####################################################################################################

    def find_closest_users(self, user_vector, movie, k):
        """
        This is the Kth- nearest neighbor algorithm
        """
        closest_users = [0] * k  # top K user
        for i in range(0, len(self.training_set)):
            if self.training_set[i][
                movie] != 0:  # Makes sure the user has that movie rating todo DO WE NEED TO CONSIDER MOVIE?
                value = self.cosine_similarity(self.training_set[i], user_vector)
                if value > closest_users[0]:
                    del closest_users[0]
                    closest_users.append((i, value))  #
                    closest_users = sorted(closest_users, key=lambda tup: tup[1])  # sort in increasing order

        return closest_users
