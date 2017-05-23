from src.trainingset import *
from src.users import *

training_set = TrainingSet()
# training_set.read_from_files('../data/input/train.txt')
training_set.read_from_json()

user = Users('test5.txt', 1000)
user.write_user_output_file()


# print training_set.find_closest_users([1,2,3])

list = [(1,3), (2,2), (3,1), (0,1)]
sorted_by_second = sorted(list, key=lambda tup: tup[1])
print sorted_by_second
