#@author Nishit Shrestha
#shresn1@unlv.nevada.edu

#command line arg pattern [<string of symbols> <no of states> <state_name> <no of symbols> <symbols> <initial probabilities> <transitions probabilities> <emission probabilities>

from sys import argv;

index=1;
input_text=list(argv[index]);

print input_text;

index=index+1;
no_states = int(argv[index]);
index=index+1;
states=[None for x in range(0,no_states)];
for i in range(0,no_states):
    states[i]=argv[index+i];
index =index+no_states;

print states;

no_symbols = int(argv[index]);
index=index+1;
symbols=[None for x in range(0,no_symbols)];
for i in range(0,no_symbols):
    symbols[i]=argv[index+i]

index=index+no_symbols;

print symbols;

initial_probability=[0 for x in range(0,no_states)];
for i in range(0,no_states):
    initial_probability[i]=float(argv[index+i]);

index=index+no_states;

print initial_probability;

transition_probability=[[0 for x in range(no_states)] for x in range(no_states)];

for i in range(0,no_states):
    for j in range(0,no_states):
        transition_probability[i][j]=float(argv[index+j]);
    index=index+no_states;
print transition_probability;

print index;

emission_probability=[[0 for x in range(no_symbols)] for x in range(no_states)];
for i in range(0,no_states):
    for j in range(0,no_symbols):
        emission_probability[i][j]=float(argv[index+j]);
    index=index+no_symbols;

print emission_probability;
#Done with the input
alpha=[[0 for x in range(no_states)] for x in range(len(input_text))];

#calculating initial probability

def symbol_index(input_sym):
    return symbols.index(input_sym);

def summation(i,j):
    sum=0;
    for t in range(0,no_states):
        sum=sum+transition_probability[t][j]*emission_probability[j][symbol_index(input_text[i])]*alpha[i-1][t];
    return sum;

for i in range(0,no_states):
    alpha[0][i]=initial_probability[i]*emission_probability[i][symbol_index(input_text[0])];

for i in range(1,len(input_text)):
    for j in range(0,no_states):
        alpha[i][j]=summation(i,j);

print alpha;

total_prob=0;
for i in range(0,no_states):
    total_prob=total_prob+alpha[len(input_text)-1][i];

print "Total probability is :"+str(total_prob);





