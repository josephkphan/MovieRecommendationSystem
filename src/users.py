import re


class Users():
    def __init__(self, file_name, num_movies):
        self.file_name = file_name
        self.input_file_path = '../data/input/' + file_name
        self.output_file_path = '../data/output/' + file_name
        self.user_vector = {}
        self.user_known_ratings = {}
        self.user_prediction_queue = {}
        self.user_calculated_prediction = {}

        with open(self.input_file_path) as f:
            for line in f:
                split = line.split(' ')
                if split[0] not in self.user_vector:
                    self.user_vector[split[0]] = [0] * num_movies
                    self.user_prediction_queue[split[0]] = []
                    self.user_known_ratings[split[0]] = []
                value = int(re.sub('\r\n', '', split[2]))
                self.user_vector[split[0]][int(split[1]) - 1] = value
                if value == 0:
                    self.user_prediction_queue[split[0]].append(value)
                else:
                    self.user_known_ratings[split[0]].append(value)
        print self.user_vector['300'][201]
        print len(self.user_vector)
        # print self.user

    def write_user_output_file(self):
        out_file = open(self.output_file_path, 'w')
        with open(self.input_file_path) as in_file:
            for line in in_file:
                split = line.split(' ')
                value = int(re.sub('\r\n', '', split[2]))
                if value == 0:
                    out_file.write(split[0] + ' ' + split[1] + ' ' + split[2])  #todo Change split[2] here!
                else:
                    out_file.write(split[0] + ' ' + split[1] + ' ' + split[2])
        out_file.close()
