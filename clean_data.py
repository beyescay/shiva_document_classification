import os, sys, glob
import shutil as SH
from distutils.dir_util import copy_tree


class DataCleaning:
    def __init__(self, path_to_20_newsgroups_dir):
        self.path_to_20_newsgroups_dir = path_to_20_newsgroups_dir
        data_dir = self.create_training_and_testing_data_set()
        training_data_dir = os.path.join(data_dir, "training")
        self.remove_header_lines(data_dir)
        self.merge_and_clean_training_data(training_data_dir)

    def create_training_and_testing_data_set(self):

        if os.path.exists(os.path.join(os.getcwd(), "data")):
            SH.rmtree(os.path.join(os.getcwd(), "data"))
            
        os.makedirs(os.path.join(os.getcwd(), "data", "training"))
        os.makedirs(os.path.join(os.getcwd(), "data", "testing"))

        key_words = ["comp", "politics", "rec", "sport"]

        for key_word in key_words:
            os.mkdir(os.path.join(os.getcwd(), "data", "training", key_word))
            os.mkdir(os.path.join(os.getcwd(), "data", "testing", key_word))

        test_data_folder = os.path.join(os.path.join(os.getcwd(), "data", "testing"))
        train_data_folder = os.path.join(os.path.join(os.getcwd(), "data", "training"))

        testing_directories = ["comp.windows.x", "rec.sport.baseball", "talk.politics.misc", "rec.autos"]

        data_directories = glob.glob(os.path.join(self.path_to_20_newsgroups_dir, "*"))

        print("\nClassifying the news groups into training and testing data sets...\n")
        for data_dir in data_directories:
            print("Classifying: {}".format(data_dir))

            news_group_folder_name = os.path.basename(data_dir)

            if news_group_folder_name in testing_directories:

                for test_key_word in news_group_folder_name.split('.'):
                    if test_key_word in key_words:
                        if test_key_word == 'rec' and len(news_group_folder_name.split('.')) == 3:
                            continue
                        copy_tree(data_dir, os.path.join(test_data_folder, test_key_word, news_group_folder_name))

            else:
                for train_key_word in news_group_folder_name.split('.'):
                    if train_key_word in key_words:
                        if train_key_word == 'rec' and len(news_group_folder_name.split('.')) == 3:
                            continue
                        copy_tree(data_dir, os.path.join(train_data_folder, train_key_word, news_group_folder_name))

        print("\nFinished classifying the data set\n")
        return os.path.join(os.getcwd(), "data")

    def remove_header_lines(self, data_directory):

        print("\nRemoving header lines from all data articles...\n")

        for root, dir, files in os.walk(data_directory):
            if len(files) > 0:
                for file_basename in files:
                    file_name = os.path.join(root, file_basename)
                    print("Removing {}".format(file_name))
                    file_name_to_write = os.path.join(root, file_basename + ".txt")
                    with open(file_name, 'r') as file_reader:
                        lines = file_reader.readlines()

                    with open(file_name_to_write, 'w') as file_writer:
                        first_empty_line_found = False
                        for line in lines:
                            if not first_empty_line_found and len(line.strip()) == 0:
                                first_empty_line_found = True
                                continue

                            if first_empty_line_found:
                                file_writer.write("{}\n".format(line.strip()))

                    os.remove(file_name)
        print("\nFinished removing header lines from all data articles.\n")

    def merge_and_clean_training_data(self, training_data_directory):

        print("\nMerging and removing unnecessary files from training data...\n")

        for root, dir, files in os.walk(training_data_directory):
            if len(files) > 0:

                merged_file_name_to_write = os.path.join(root, "{}.txt".format(os.path.basename(root)))

                for file_basename in files:

                    file_name = os.path.join(root, file_basename)
                    print("Merging {}".format(file_name))

                    with open(file_name, 'r') as file_reader:
                        lines = file_reader.readlines()

                    with open(merged_file_name_to_write, 'a') as file_writer:
                        for line in lines:
                            file_writer.write("{}\n".format(line.strip()))

                SH.copy(merged_file_name_to_write, os.path.join(root, "..", "{}.txt".format(os.path.basename(root))))

        for root, dirs, files in os.walk(training_data_directory):
            if len(files) > 0:
                for dir in dirs:
                    SH.rmtree(os.path.join(root, dir))

                merged_file_name_to_write = os.path.join(root, "{}.txt".format(os.path.basename(root)))

                for file_basename in files:
                    file_name = os.path.join(root, file_basename)
                    print("Removing {}".format(file_name))
                    with open(file_name, 'r') as file_reader:
                        lines = file_reader.readlines()

                    with open(merged_file_name_to_write, 'a') as file_writer:
                        for line in lines:
                            file_writer.write("{}\n".format(line.strip()))

                    os.remove(file_name)

        print("\nFinished merging and removing unnecessary files from training data.\n")


if __name__ == "__main__":
    DataCleaning("../20_newsgroups")
