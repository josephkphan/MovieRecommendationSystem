from src.trainingset import *
from src.users import *
from src.prediction import *
from src.myjsonhandler import *

import pprint

training_set = TrainingSet()
training_set.read_from_json()

prediction = Prediction(training_set.training_set)
test_name = 'test5'
user = Users(test_name + '.txt', 1000)
k = 20

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(user.user_prediction_queue)
print user.user_prediction_queue

predictions = {}
for u in user.user_prediction_queue:
    if u not in predictions:
        predictions[u] = []
    print u
    print user.user_vector[u]
    for missing_movie_prediction in user.user_prediction_queue[u]:
        p = prediction.user_user_cosine_similarity(user.user_vector[u], int(missing_movie_prediction) - 1, 5)
        #p = prediction.user_user_pearson(user.user_vector[u], int(missing_movie_prediction) - 1, k)
        p = MyMathHelper.custom_rounding(p)
        print 'Rounded Prediction:', p
        predictions[u].append(p)

pp.pprint(predictions)

MyJsonHandler.save_data_to_json_file(predictions, '../data/output/' + test_name + '_predictions.json')
user.write_user_output_file(predictions)
