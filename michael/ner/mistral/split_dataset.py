import pickle
import sys
sys.path.append('../../')
from summarizers.get_complaints import get_complaint_only_cases

def split_pickle(pickle_path):
    """
    Zhu-Li! Do the thing!
    """
    with open(pickle_path, 'rb') as cases_file:
        cases = pickle.load(cases_file)

    print(len(cases))
    print(len(cases[:int(.8 * len(cases))]))
    print(len(cases[int(.8 * len(cases)):]))

    with open('./train_cases.pkl', 'wb') as file:
        pickle.dump(cases[:int(.8 * len(cases))], file)
    with open('./val_cases.pkl', 'wb') as file:
        pickle.dump(cases[int(.8 * len(cases)):], file)

if __name__ == '__main__':
    split_pickle('../../all_cases_clearinghouse.pkl')
