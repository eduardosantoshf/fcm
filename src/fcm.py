import sys
import math
import argparse

class Fcm:
    
    def __init__(self, filename, k, alpha):

        # initial variables
        self.filename = filename
        self.k = k
        self.alpha = alpha
        self.times = dict()

        self.alphabet = self.get_alphabet()
        self.alphabet_size = len(self.alphabet)

        self.is_hash = False
        # fill table with number of occurences
        self.filled_table = self.fill_table(self.init_table())

        # final entropy variable
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
            self.is_hash = True
            table = {}
        else:
            self.is_hash = False
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

        if not self.is_hash:
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

    def get_table_row(self, seq):

        if not self.is_hash:
            return self.filled_table[self.get_table_index(seq)]
        else:
            if seq in self.filled_table:
                temp = []
                for c in self.alphabet:
                    if c in self.filled_table[seq]:
                        temp.append(self.filled_table[seq][c])
                    else:
                        temp.append(0)
                return temp
            else:
                return [0 for _ in range(self.alphabet_size)]

    def calculate_each_probability(self, row):
        # list of probabilities for each letter to appear after context
        prob_list = []

        if self.is_hash:
            # sum of the occurences of the row
            total = sum(row.values()) + self.alphabet_size * self.alpha

            # some symbols might not be in the hashtable,
            # so we need to iterate the alphabet and add alpha to every symbol
            for c in self.alphabet:
                if c in row:
                    prob_list.append((row[c] + self.alpha) / total)
                else:
                    prob_list.append(self.alpha/total)
            return prob_list
        else:
            total = sum(row) + self.alphabet_size * self.alpha
            return [(c + self.alpha)/total for c in row]


    def calculate_each_entropy(self, prob_list):
        entropy = 0.0

        # calculate the entropy in the row
        for x in prob_list:
            entropy += x * math.log2(x)

        return - entropy

    def get_sum_table_values(self):
        
        if self.is_hash:
            total = 0
            # sum of all probabilities of the table
            for k in self.filled_table:
                for j in self.filled_table[k]:
                    total += self.filled_table[k][j]
            return total
        else:
            return sum([sum(x) for x in self.filled_table])

    def calculate_global_entropy(self):
        
        self.total_counter = self.get_sum_table_values()
        final_entropy = 0
        if self.is_hash:
            # for each row
            for x in self.filled_table:

                # calculate the probabilities
                probs = self.calculate_each_probability(self.filled_table[x])

                # calculate the entropy of the row
                entropy_row = self.calculate_each_entropy(probs)

                # calculate the entropy of the entire text
                final_entropy += sum(self.filled_table[x].values()) / self.total_counter * entropy_row

        else:
            for row in self.filled_table:
                probs = self.calculate_each_probability(row)
                entropy_row = self.calculate_each_entropy(probs)
                final_entropy += sum(row) / self.total_counter * entropy_row
        return final_entropy

if __name__== "__main__":
    
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument("file", metavar="file", type=str)
    parser.add_argument('-k', type=int,
                    help='size of the sequence', default=1)
    parser.add_argument('-a', '--alpha', type=float, default=0.01,
                    help='alpha parameter')

    args = vars(parser.parse_args())
        
    filename = args["file"]
    k = args["k"]
    alpha = args["alpha"]

    if k <= 0:
        print("k must be a positive integer number")
    if alpha <= 0:
        print("alpha must be a float number higher than 0")

    # new fcm model
    fcm = Fcm(filename, k, alpha)

    # get the entropy
    print("Entropy of the text: ", fcm.calculate_global_entropy())
