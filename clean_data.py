import os, sys, glob
import shutil as SH
from distutils.dir_util import copy_tree


class DataCleaning:
    def __init__(self, path_to_20_newsgroups_dir):
        self.path_to_20_newsgroups_dir = path_to_20_newsgroups_dir
        data_dir = self.create_training_and_testing_data_set()
        self.clean_data(data_dir)
        self.merge_data(data_dir)

    def create_training_and_testing_data_set(self):
        os.makedirs(os.path.join(os.getcwd(), "data", "training"))
        os.makedirs(os.path.join(os.getcwd(), "data", "testing"))
        os.makedirs(os.path.join(os.getcwd(), "data", "unwanted"))

        test_data_folder = os.path.join(os.path.join(os.getcwd(), "data", "testing"))
        train_data_folder = os.path.join(os.path.join(os.getcwd(), "data", "training"))
        unwanted_data_folder = os.path.join(os.path.join(os.getcwd(), "data", "unwanted"))

        testing_directories = ["comp.windows.x", "rec.sport.baseball", "talk.politics.misc", "rec.autos"]

        training_key_words = ["comp", "politics", "rec"]

        data_directories = glob.glob(os.path.join(self.path_to_20_newsgroups_dir, "*"))

        for data_dir in data_directories:
            print("Current new group folder: {}".format(data_dir))

            news_group_folder_name = os.path.basename(data_dir)

            if news_group_folder_name in testing_directories:
                print("Goes to testing")
                copy_tree(data_dir, os.path.join(test_data_folder, news_group_folder_name))

            else:
                is_training = False
                for key_word in news_group_folder_name.split('.'):
                    if key_word in training_key_words:
                        print("Goes to training")
                        copy_tree(data_dir, os.path.join(train_data_folder, news_group_folder_name))
                        is_training = True
                        break

                if not is_training:
                    print("Goes to unwanted")
                    print(os.path.join(unwanted_data_folder, news_group_folder_name))
                    copy_tree(data_dir, os.path.join(unwanted_data_folder, news_group_folder_name))

        return os.path.join(os.getcwd(), "data")

    def clean_data(self, data_directory):
        for root, dir, files in os.walk(data_directory):
            if len(files) > 0:
                for file_basename in files:
                    file_name = os.path.join(root, file_basename)
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

    def merge_data(self, data_directory):
        for root, dir, files in os.walk(data_directory):
            if len(files) > 0:
                merged_file_name_to_write = os.path.join(root, "merged.txt")
                for file_basename in files:
                    file_name = os.path.join(root, file_basename)

                    with open(file_name, 'r') as file_reader:
                        lines = file_reader.readlines()

                    with open(merged_file_name_to_write, 'a') as file_writer:

                        for line in lines:
                            file_writer.write("{}\n".format(line.strip()))


if __name__ == "__main__":
    DataCleaning("/home/sarath/Documents/Shiva/032618/20_newsgroups")
