import sys
import math

class Fcm:
    
    def __init__(self, filename, k):

        # initial variables
        self.filename = filename
        self.k = k
        self.times = dict()

        self.alphabet = self.get_alphabet()
        self.alphabet_size = len(self.alphabet)

        # fill table with number of occurences
        self.filled_table = self.fill_table(self.init_table())

        # final entropy variable
        self.final_entropy = 0.0
        # all probabilities
        self.total_counter = 0

    def get_alphabet(self):
        with open(self.filename, "r") as f:
            alphabet = list(set(f.read()))

        return alphabet

    def init_table(self):

        space = self.calculate_table_space()
        threshold = 0.5
        if space >= threshold:
            table = {}
        else:
            table = [[0] * self.alphabet_size for _ in range(self.alphabet_size ** self.k)]
        return table

    def calculate_table_space(self):
        # calculates the amount of RAM used by the table
        # assuming 16 bits integers
        # result in MB
        return (self.alphabet_size ** self.k) * self.alphabet_size * 16 / 8 / 1024 / 1024

    def fill_table(self, table):

        with open(self.filename, "r") as f:
            seq = f.read(self.k)
            while True:
                c = f.read(1)
                if not c:
                    break
                if c not in self.times:
                    self.times[c] = 1
                else:
                    self.times[c] += 1

                #table[get_table_index(seq, alphabet)][alphabet.index(c)] += 1 
                self.inc_table_index(seq, table, c)
                seq = seq[1:] + c
        
        return table

    def inc_table_index(self, seq, table, c):

        if type(table) == list:
            table[self.get_table_index(seq)][self.alphabet.index(c)] += 1 
        else:
            if seq not in table:
                table[seq] = {c: 1}
            else:
                if c not in table[seq]:
                    table[seq][c] = 1
                else:
                    table[seq][c] += 1

    def get_table_index(self, seq):
        index = 0
        n = 0
        for i in reversed(seq):
            index += len(self.alphabet)**n * self.alphabet.index(i)
            n += 1
        return index

    def get_table_row(self, seq, table):

        if type(table) == list:
            return table[self.get_table_index(seq, self.alphabet)]
        else:
            if seq in table:
                temp = []
                for c in self.alphabet:
                    if c in table[seq]:
                        temp.append(table[seq][c])
                    else:
                        temp.append(0)
                return temp
            else:
                
                temp = []
                for c in self.alphabet:
                    temp.append(self.times[c])
                return temp
                
                #return [0 for _ in range(len(alphabet))]

    def calculate_each_probability(self, row):
        # list of probabilities for each letter to appear after context
        prob_list = []
        alpha = 0.1

        # sum of the occurences of the row
        for x in row:
            total = 0
            for k in row:
                total += row[k]
            
            prob_list.append((row[x] + alpha) / (total + (abs(total) * alpha)))

            #probability of each letter
            #prob_list.append(row[x] / total)

        return prob_list

    def calculate_each_entropy(self, prob_list):
        entropy = 0.0

        # calculate the entropy in the row
        for x in prob_list:
            entropy += x * math.log2(x)

        return - entropy

    def get_sum_table_values(self):

        # sum of all probabilities of the table
        for k in self.filled_table:
            for j in self.filled_table[k]:
                self.total_counter += self.filled_table[k][j]

    def calculate_global_entropy(self):
        
        self.get_sum_table_values()

        # for each row
        for x in self.filled_table:

            # calculate the probabilities
            probs = self.calculate_each_probability(self.filled_table[x])

            # calculate the entropy of the row
            entropy_row = self.calculate_each_entropy(probs)

            #print(str(x) + " -> " + str(filled_table[x]) + str(probs))
            #print(str(x) + str(filled_table[x]) + str(probs) + str(entropy_row))
            #print(entropy_row)
            #print(sum(self.filled_table[x].values()))

            # calculate the entropy of the entire text
            self.final_entropy += sum(self.filled_table[x].values())/self.total_counter * entropy_row

            #print(sum(probs)/len(probs) * entropy_row)

if __name__== "__main__":
    
    filename = sys.argv[1]
    k = 1 if len(sys.argv) < 3 else int(sys.argv[2])

    # new fcm model
    fcm = Fcm(filename, k)

    # get the entropy
    fcm.calculate_global_entropy()

    print("Entropy of the text: " + str(fcm.final_entropy))

    # example of a row
    #probs = fcm.calculate_each_probability(fcm.filled_table['w h'])
    #print(probs)
    #entropy_row = fcm.calculate_each_entropy(probs)
    #print(entropy_row)