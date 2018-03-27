import clean_data as DC
import model_20newsgroup as MD
import argparse as A

if __name__ == "__main__":

    parser = A.ArgumentParser()
    parser.add_argument('-d', '--newsgroup_dir', help="Complete path to 20_newsgroups directory - The directory"
                                                         "containing the news group articles data set", type=str)

    args = parser.parse_args()

    data_set_dir = args.newsgroup_dir

    print("\nCleaning and setting up the training and test data sets...\n")
    DC.DataCleaning(data_set_dir)
    print("\nFinished data cleaning and set up.\n")
    print("\nPreparing to train model...\n")
    MD.main()
    print("\nProgram finished.\n")