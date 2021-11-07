from fcm import Fcm
import sys
import random
import argparse

class Generator:

    def __init__(self, fcm):
        self.fcm = fcm
    
    def generate(self, size=100, seq=None):
        if not seq:
            seq = ""
            for i in range(k):
                seq += self.fcm.alphabet[random.randint(0, self.fcm.alphabet_size - 1)]

        if len(seq) != self.fcm.k:
            print("the initial sequence must have the size k")
            exit(1)

        text = seq
        for i in range(size):
            row = self.fcm.get_table_row(seq)
            total = self.fcm.get_row_sum(seq) + self.fcm.alphabet_size * self.fcm.alpha
            r = random.random() * (total)
            for i, v in enumerate(row):
                r -= v + self.fcm.alpha
                if r <= 0:
                    text += self.fcm.alphabet[i]
                    break
            
            seq = seq[1:] + text[-1]

        return text

    def generate_to_file(self, filename, size=100, seq=None):
        f = open(filename, "w")
        f.write(self.generate(size, seq))
        f.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate some text.')
    parser.add_argument("file", metavar="file", type=str)
    parser.add_argument('-k', type=int,
                    help='size of the sequence', default=1)
    parser.add_argument('-a', '--alpha', type=float, default=0.01,
                    help='alpha parameter')
    parser.add_argument('-l', '--length', type=int, default=100, help="length of the generated text")
    parser.add_argument('-s', '--seq', type=str, default=None, help="initial sequence of the generated text")

    args = vars(parser.parse_args())
        
    filename = args["file"]
    k = args["k"]
    alpha = args["alpha"]
    size = args["length"]
    seq = args["seq"]

    if k <= 0:
        print("k must be a positive integer number")
        exit(1)
    if alpha <= 0:
        print("alpha must be a float number higher than 0")
        exit(1)

    # new fcm model
    fcm = Fcm(filename, k, alpha)
    generator = Generator(fcm)
    print(generator.generate(size, seq))
    