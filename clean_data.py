import os, sys


def clean_data(data_directory):
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


if __name__ == "__main__":
    clean_data("/home/sarath/Documents/Shiva/032618/data")
