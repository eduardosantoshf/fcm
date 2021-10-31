import sys
import math

times = {}

def get_alphabet(filename):
    with open(filename, "r") as f:
        alphabet = list(set(f.read()))

    return alphabet

def calculate_table_space(alphabet_size, k):
    # calculates the amount of RAM used by the table
    # assuming 16 bits integers
    # result in MB
    return (alphabet_size ** k) * alphabet_size * 16 / 8 / 1024 / 1024 


def init_table(alphabet, k):

    space = calculate_table_space(len(alphabet), k)
    threshold = 0.5
    if space >= threshold:
        table = {}
    else:
        table = [[0] * len(alphabet) for _ in range(len(alphabet) ** k)]
    return table

def get_table_index(seq, alphabet):
    index = 0
    n = 0
    for i in reversed(seq):
        index += len(alphabet)**n * alphabet.index(i)
        n += 1
    return index

def fill_table(table, alphabet, k, filename):
    global times

    with open(filename, "r") as f:
        seq = f.read(k)
        while True:
            c = f.read(1)
            if not c:
                break
            if c not in times:
                times[c] = 1
            else:
                times[c] += 1

            #table[get_table_index(seq, alphabet)][alphabet.index(c)] += 1 
            inc_table_index(seq, alphabet, table, c)
            seq = seq[1:] + c
    
    return table

def inc_table_index(seq, alphabet, table, c):

    if type(table) == list:
        table[get_table_index(seq, alphabet)][alphabet.index(c)] += 1 
    else:
        if seq not in table:
            table[seq] = {c: 1}
        else:
            if c not in table[seq]:
                table[seq][c] = 1
            else:
                table[seq][c] += 1

def get_table_row(seq, alphabet, table):
    global times
    if type(table) == list:
        return table[get_table_index(seq, alphabet)]
    else:
        if seq in table:
            temp = []
            for c in alphabet:
                if c in table[seq]:
                    temp.append(table[seq][c])
                else:
                    temp.append(0)
            return temp
        else:
            
            temp = []
            for c in alphabet:
                temp.append(times[c])
            return temp
            
            #return [0 for _ in range(len(alphabet))]

def calculate_each_probability(row):
    prob_list = []
    #alpha = 0.1
    for x in row:
        total = 0
        for k in row:
            total += row[k]
        
        #prob_list.append((row[x] + alpha) / (total + (abs(total) * alpha)))
        prob_list.append(row[x] / total)

    return prob_list

def calculate_each_entropy(prob_list):
    entropy = 0.0

    for x in prob_list:
        entropy += x * math.log2(x)

    return - entropy

def calculate_global_entropy(filled_table):

    final_entropy = 0.0

    total_counter = 0

    for k in filled_table:
        for j in filled_table[k]:
            total_counter += filled_table[k][j]


    for x in filled_table:
        probs = calculate_each_probability(filled_table[x])
        entropy_row = calculate_each_entropy(probs)
        #print(str(x) + " -> " + str(filled_table[x]) + str(probs))
        #print(str(x) + str(filled_table[x]) + str(probs) + str(entropy_row))
        final_entropy += sum(probs)/total_counter * entropy_row
        #print(sum(probs)/len(probs) * entropy_row)

    #print(final_entropy)

    return final_entropy






def main():
    filename = sys.argv[1]
    k = 1 if len(sys.argv) < 3 else int(sys.argv[2])
    alphabet = get_alphabet(filename)
    filled_table = fill_table(init_table(alphabet, k), alphabet, k, filename)
        
    #print("w h -> " + str(filled_table['w h']))
    probs = calculate_each_probability(filled_table['w h'])
    #print(probs)
    entropy_row = calculate_each_entropy(probs)

    print(calculate_global_entropy(filled_table))

    #print(entropy_row)

    



if __name__== "__main__":
    main()