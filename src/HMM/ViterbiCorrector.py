class ViterbiCorrector:
    def __init__(self,states,symbols,initial_prob,emission_matrix,transition_matrix):
        self.states=states;
        self.symbols=symbols;
        self.initial_prob=initial_prob;
        self.emission_matrix=emission_matrix;
        self.transition_matrix=transition_matrix;

    def compute_initial_prob(self,letter,viterbi_matrix):
        for index,state in enumerate(self.states):
            viterbi_matrix[0][index]=self.initial_prob[index]*self.emission_matrix[self.symbols.index(letter)][index];
        return viterbi_matrix;

    def compute_best_path(self,index,viterbi_matrix):
        best_path=None;
        max=0;
        for i,state in enumerate(self.states):
            if max<viterbi_matrix[index][i]:
                max = viterbi_matrix[index][i];
                best_path=i;
        return best_path;

    def compute_max_phi(self,viterbi_index,i,viterbi_matrix):
        max=0;
        for index,state in enumerate(self.states):
            phi=viterbi_matrix[viterbi_index-1][index]*self.transition_matrix[index][i];
            if max<phi:
                max=phi;
        return max;


    def compute_viterbi_probabilty(self,index,letter,viterbi_matrix):
        for i,state in enumerate(self.states):
            viterbi_matrix[index][i]=self.compute_max_phi(index,i,viterbi_matrix)*self.emission_matrix[self.symbols.index(letter)][i];
        return viterbi_matrix;

    def build_viterbi_matrix_for_input(self,word):
        viterbi_best_path=[0 for x in range(0,len(word))];
        viterbi_matrix=[[0 for x in range(0,len(self.states))] for x in range(0,len(word))];
        viterbi_matrix=self.compute_initial_prob(word[0],viterbi_matrix);
        viterbi_best_path[0]=self.compute_best_path(0,viterbi_matrix);

        for index,letter in enumerate(word):
            if index==0:
                continue;
            viterbi_matrix=self.compute_viterbi_probabilty(index,letter,viterbi_matrix);
            viterbi_best_path[index]=self.compute_best_path(index,viterbi_matrix);
        return viterbi_matrix,viterbi_best_path;

    def word_corrector(self,word):
        viterbi_matrix,viterbi_best_path=self.build_viterbi_matrix_for_input(word);
        correct_word='';
        for i in viterbi_best_path:
            correct_word+=self.states[i];
        return correct_word;


