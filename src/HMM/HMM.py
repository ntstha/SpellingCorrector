from src.FileHandler.FileReader import FileReader;
from src.HMM.ViterbiCorrector import ViterbiCorrector;
from src.HMM.PrecisionRecallCalc import PrecisionRecallCalc;
import random;
class HMM:
    def __init__(self):
        global states;
        states=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'];
        global symbols;
        symbols=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'];
        global initial_prob;
        initial_prob=[0.0384 for x in range(0,len(states))];
        global transition_probability;
        transition_probability=[[0 for x in range(len(states))] for x in range(len(states))];
        global emission_probability;
        emission_probability=[[0 for x in range(len(symbols))] for x in range(len(states))];

    def fill_transition_counter_from_training(self,training_data):
        i_j_transition_counter=[[0 for x in range(len(symbols))] for x in range(len(states))];
        for words in training_data:
            if words.isalpha():
                old_letter=None;
                for letter in words:
                    letter=letter.lower();
                    if old_letter is None:
                        old_letter=letter;
                        continue;
                    else:
                        i_j_transition_counter[states.index(old_letter)][states.index(letter)]=1+i_j_transition_counter[states.index(old_letter)][states.index(letter)];
                        old_letter=letter;

        return i_j_transition_counter;

    def increment_count_for_row(self,i,i_j_transition_counter):
        for j in range(0,len(states)):
                i_j_transition_counter[i][j]=1+i_j_transition_counter[i][j];

        return i_j_transition_counter;

    def send_for_smoothing(self,i_j_transition_counter):
        for i in range(0,len(states)):
            for j in range(0,len(states)):
                if i_j_transition_counter[i][j]==0:
                    self.increment_count_for_row(i,i_j_transition_counter);
                    break;
        return i_j_transition_counter;


    def count_outgoing_transition(self,i,i_j_transition_counter):
        count=0;
        for j in range(0,len(states)):
            count=count+i_j_transition_counter[i][j];

        return count;
    def compute_transition_matrix(self,training_data):
        transition_matrix=[[0 for x in range(0,len(states))] for x in range(len(states))];
        i_j_transition_counter=self.fill_transition_counter_from_training(training_data);
        i_j_transition_counter=self.send_for_smoothing(i_j_transition_counter);#smoothing
        for i in range(0,len(states)):
            out_going_count=self.count_outgoing_transition(i,i_j_transition_counter);
            for j in range(0,len(states)):
                transition_matrix[i][j]=i_j_transition_counter[i][j]/float(out_going_count);
        return transition_matrix;

    def get_surrounding_char(self,letter):
        corruption_dict = {
            'a': ['q', 'w', 's', 'x', 'z'],
            'b': ['f', 'g', 'h', 'n', 'v'],
            'c': ['x', 's', 'd', 'f', 'v'],
            'd': ['w', 'e', 'r', 's', 'f', 'x', 'c', 'v'],
            'e': ['w', 'r', 's', 'd', 'f'],
            'f': ['e', 'r', 't', 'd', 'g', 'c', 'v', 'b'],
            'g': ['r', 't', 'y', 'f', 'h', 'v', 'b', 'n'],
            'h': ['t', 'y', 'u', 'g', 'j', 'b', 'n', 'm'],
            'i': ['u', 'o', 'j', 'k', 'l'],
            'j': ['y', 'u', 'i', 'h', 'k', 'n', 'm'],
            'k': ['u', 'i', 'o', 'j', 'l', 'm'],
            'l': ['i', 'o', 'p', 'k'],
            'm': ['n', 'h', 'j', 'k'],
            'n': ['b', 'g', 'h', 'j', 'm'],
            'o': ['i', 'k', 'l', 'p'],
            'p': ['o', 'l'],
            'q': ['a', 's', 'w'],
            'r': ['e', 'd', 'f', 'g', 't'],
            's': ['q', 'w', 'e', 'a', 'd', 'z', 'x', 'c'],
            't': ['r', 'y', 'f', 'g', 'h'],
            'u': ['y', 'i', 'h', 'j', 'k'],
            'v': ['d', 'f', 'g', 'c', 'b'],
            'w': ['q', 'e', 'a', 's', 'd'],
            'x': ['a', 's', 'd', 'z', 'c'],
            'y': ['t', 'u', 'g', 'h', 'j'],
            'z': ['a', 's', 'x']
        };

        surrounding_char = corruption_dict.get(letter)[random.randint(0,len(corruption_dict.get(letter))-1)];
        return surrounding_char;

    def get_random_float_between_range(self,a,b):
        return random.uniform(a,b);

    def corrupt_data(self,training_data):
        corrupted_list=[];
        for word in training_data:
            corrupted_word='';
            for letter in word:
                random_number = self.get_random_float_between_range(0,1);
                if random_number<0.2:
                    surrounding_char = self.get_surrounding_char(letter);
                    corrupted_word+=surrounding_char;
                else:
                    corrupted_word+=letter;

            corrupted_list.append(corrupted_word);
        return corrupted_list;
    def fill_emission_matrix_for_count(self,corrupted_list,training_list):
        emission_count=[[0 for x in range(0,len(states))] for x in range(len(states))];
        for i in range(0,len(training_list)):
            training_word=training_list[i];
            corrupted_word=corrupted_list[i];
            for j in range(0,len(training_word)):
                training_letter = training_word[j].lower();
                corrupted_letter = corrupted_word[j].lower();
                emission_count[states.index(training_letter)][states.index(corrupted_letter)]=1+emission_count[states.index(training_letter)][states.index(corrupted_letter)];
        return emission_count;

    def compute_emission_matrix(self,corrupted_list,training_list):
        emission_matrix=[[0 for x in range(0,len(states))] for x in range(len(states))];
        emission_count = self.fill_emission_matrix_for_count(corrupted_list,training_list);
        emission_count = self.send_for_smoothing(emission_count);
        for i in range(0,len(states)):
            out_going_count=self.count_outgoing_transition(i,emission_count);
            for j in range(0,len(states)):
                emission_matrix[i][j]=emission_count[i][j]/float(out_going_count);
        return emission_matrix;

hmm = HMM();
fileReader = FileReader();
testing_list,training_list = fileReader.get_testing_training_data_from_file("docs/text.txt");
transition_matrix=hmm.compute_transition_matrix(training_list);
corrupted_list = hmm.corrupt_data(training_list);
emission_matrix=hmm.compute_emission_matrix(corrupted_list,training_list);


corrupted_test_list = hmm.corrupt_data(testing_list);
spellCorrector = ViterbiCorrector(states,symbols,initial_prob,emission_matrix,transition_matrix);
precisionRecallComp = PrecisionRecallCalc();
precisionRecallComp.computePrecisionRecall(testing_list,corrupted_test_list,spellCorrector);


