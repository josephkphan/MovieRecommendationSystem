from src.trainingset import *

training_set = TrainingSet()
# training_set.read_from_files('../data/input/train.txt')
training_set.read_from_json()
print len(training_set.movie_movie_similarity_matrix)
print len(training_set.movie_movie_similarity_matrix[0])

