import os;
import re;
class FileReader:
    def __init__(self):
        return;

    def read_text_from_file(self,file_name):
        my_dir = os.path.dirname(os.path.dirname(__file__));
        file_path = os.path.join(my_dir,file_name);
        file = open(file_path,'r');
        text = file.read();
        file.close();
        return text;

    def split_words_from_text(self,text):
        tokens = re.findall("\\w+",text);
        return tokens;

    def filter_alphabets_only_from_list(self,list):
        filtered_list=[];
        for elem in list:
            if elem.isalpha():
                filtered_list.append(elem.lower());
        return filtered_list;

    def get_testing_training_data_from_file(self,file_name):
        text = self.read_text_from_file(file_name);
        tokens = self.split_words_from_text(text);
        testing_list = self.filter_alphabets_only_from_list(tokens[0:int((0.2*len(tokens)))]);
        training_list = self.filter_alphabets_only_from_list(tokens[int(0.2*len(tokens)):len(tokens)]);
        return testing_list,training_list;


