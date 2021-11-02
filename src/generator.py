from fcm import Fcm
import sys
import random
import argparse

def main(size):

    seq = ""
    for i in range(k):
        seq += fcm.alphabet[random.randint(0, fcm.alphabet_size - 1)]

    text = seq
    alpha = 0.01
    for i in range(size):
        row = fcm.get_table_row(seq)
        total = sum(row) + fcm.alphabet_size * fcm.alpha
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
    parser.add_argument('-s', '--size', type=int, default=100, help="size of the generated text")

    args = vars(parser.parse_args())
    print(args)
        
    filename = args["file"]
    k = args["k"]
    alpha = args["alpha"]
    size = args["size"]

    # new fcm model
    fcm = Fcm(filename, k, alpha)

    main(size)
    