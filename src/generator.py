from fcm import Fcm
import sys
import random
import argparse

def main(size, seq):

    if not seq:
        seq = ""
        for i in range(k):
            seq += fcm.alphabet[random.randint(0, fcm.alphabet_size - 1)]

    if len(seq) != k:
        print("the initial sequence must have the size k")
        exit(1)

    text = seq
    for i in range(size):
        row = fcm.get_table_row(seq)
        total = fcm.get_row_sum(seq) + fcm.alphabet_size * fcm.alpha
        r = random.random() * (total)
        for i, v in enumerate(row):
            r -= v + fcm.alpha
            if r <= 0:
                text += fcm.alphabet[i]
                break
        
        seq = seq[1:] + text[-1]

    print(text)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
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

    main(size, seq)
    