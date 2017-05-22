import math, json


class TrainingSet():
    def __init__(self):
        # Initialize Variables
        self.training_set = []  # List of Lists containing input data from file
        self.training_set_transposed = []  # Transposed of training set - used to calculate similarity matrix
        self.movie_popularity = []  # Static Movie Popularity - no personalization
        self.movie_movie_similarity_matrix = []  # Keeps the similarity between every movie
        self.user_user_similarity_matrix = []
        self.file_paths = {
            'training_set': '../data/json/training_set.json',
            'training_set_transposed': '../data/json/training_set_transposed.json',
            'movie_popularity': '../data/json/movie_popularity.json',
            'movie_movie_similarity_matrix': '../data/json/movie_movie_similarity_matrix.json',
            'user_user_similarity_matrix': '../data/json/user_user_similarity_matrix.json'
        }

    # Will read from files and save to json
    def read_from_files(self, file_path):
        self.read_training_file(file_path)
        self.create_transposed_training_set()
        self.create_movie_popularity_list()
        self.create_movie_movie_similarity_matrix()
        self.create_user_user_similarity_matrix()

    def read_from_json(self):
        self.training_set = self.get_data_from_json_file(self.file_paths['training_set'])
        self.training_set_transposed = self.get_data_from_json_file(self.file_paths['training_set_transposed'])
        self.movie_popularity = self.get_data_from_json_file(self.file_paths['movie_popularity'])
        self.movie_movie_similarity_matrix = self.get_data_from_json_file(self.file_paths['movie_movie_similarity_matrix'])
        self.user_user_similarity_matrix = self.get_data_from_json_file(self.file_paths['user_user_similarity_matrix'])

    # Read Training data file and store data in self.training_set
    def read_training_file(self, file_path):
        with open(file_path) as f:
            for line in f:
                row = []
                split = line.split('\t')
                for value in split:
                    row.append(int(value))
                self.training_set.append(row)
        print len(self.training_set)
        self.save_data_to_json_file(self.training_set, self.file_paths['training_set'])

    # Transposes Training set so its 1000 rows (# movies) and 200 columns (# users)
    def create_transposed_training_set(self):
        for i in range(0, len(self.training_set[0])):
            list = []
            for j in range(0, len(self.training_set)):
                list.append(self.training_set[j][i])
            self.training_set_transposed.append(list)
        print len(self.training_set_transposed)
        print len(self.training_set_transposed[0])
        self.save_data_to_json_file(self.training_set_transposed, self.file_paths['training_set_transposed'])

    # Takes the Average Rating for every movie. This does not consider '0' or non-explicit ratings
    def create_movie_popularity_list(self):
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
            # print self.movie_popularity
            # print len(self.movie_popularity)
            self.save_data_to_json_file(self.movie_popularity, self.file_paths['movie_popularity'])

    def cosine_similarity(self,v1, v2):
            # "compute cosine similarity of v1 to v2: (v1 dot v2)/{||v1||*||v2||)"
            sumxx, sumxy, sumyy, cosine = 0, 0, 0, 0
            for i in range(len(v1)):
                x = v1[i];
                y = v2[i]
                sumxx += x * x
                sumyy += y * y
                sumxy += x * y
                try:
                    cosine = sumxy / math.sqrt(sumxx * sumyy)
                except Exception, e:
                    cosine = 0
            return cosine

    # Creates the cosine similarity matrix for Movie to Movie
    def create_movie_movie_similarity_matrix(self):
        print 'Calculating movie movie similarity matrix'

        counter = 0
        for i in range(0, len(self.training_set_transposed)):
            list = []
            for j in range(0, len(self.training_set_transposed)):
                counter += 1
                print counter
                list.append(self.cosine_similarity(self.training_set_transposed[i], self.training_set_transposed[j]))
            self.movie_movie_similarity_matrix.append(list)
        self.save_data_to_json_file(self.movie_movie_similarity_matrix, self.file_paths['movie_movie_similarity_matrix'])

    # Creates the cosine similarity matrix for User to User
    def create_user_user_similarity_matrix(self):
        print 'Calculating user user similarity matrix'

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
        out_file = open(file_path, "w")
        json.dump(data, out_file, indent=4)
        out_file.close()

    @staticmethod
    def get_data_from_json_file(file_path):
        try:
            with open(file_path) as f:
                return json.load(f)
        except IOError as e:
            print 'could not read ' + file_path


