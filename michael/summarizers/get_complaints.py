import pickle
import argparse
#tbh we probably could have just done all this while the training was happenenig but hind sight 2020

def get_complaint_only_cases(pickle_path):
    """
    filters cases for those which only contain complaints
    """
    with open(pickle_path, 'rb') as cases_file:
        cases = pickle.load(cases_file)
    complaint_cases = []
    for case in cases:
        documents = [doc.document_type for doc in case.case_documents]
        if set(documents) == {'Complaint'}:
            print(documents)
            complaint_cases.append(case)
    return complaint_cases

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog = 'Filter out cases with only complaints in them')
    parser.add_argument('picklepath', help = 'path to pickle file with Cases in them')
    args = parser.parse_args()
    print(len(get_complaint_only_cases(args.picklepath)))
