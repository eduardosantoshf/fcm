from fcm import get_alphabet, fill_table, init_table, get_table_index, get_table_row
import sys
import random

def main():
    filename = sys.argv[1]
    k = 1 if len(sys.argv) < 3 else int(sys.argv[2])
    alphabet = get_alphabet(filename)
    table = fill_table(init_table(alphabet, k), alphabet, k, filename)

    seq = ""
    for i in range(k):
        seq += alphabet[random.randint(0, len(alphabet) - 1)]

    size = 10000
    text = seq
    alpha = 0.01
    for i in range(size):
        row = get_table_row(seq, alphabet, table)
        total = sum(row) + len(alphabet) * alpha
        r = random.random() * (total)
        for i, v in enumerate(row):
            r -= v + alpha
            if r <= 0:
                text += alphabet[i]
                break
        
        seq = seq[1:] + text[-1]

    print(text)

if __name__ == "__main__":
    main()