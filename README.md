
# TAI First Assigment

The objective of this work was to build a Finite-Context-Model that reads the text from a file and stores the number of the times a character appears after a sequence of characters. It then can use the stored information to generate new text or to calculate the entropy of the text.

## Authors

* [Bruno Bastos](https://github.com/BrunosBastos) - 93302
* [Eduardo Santos](https://github.com/eduardosantoshf) - 93107
* [Pedro bastos](https://github.com/bastos-01) - 93150

## How to Run

The project was done using python3. 
Together with the required files, fcm.py and generator.py, there's a file
used to generate the charts for the report. In order to run it, it is necessary
to have matplotlib installed in the python environment. Be warned that charts.py 
might take a while to run.

### FCM

The fcm.py program has 4 arguments: filename, k, alpha, threshold.

```
    filename -> (Required)the text file that will be used to fill the fcm.

    -k <int> -> (Default 1) the size that is going to be used for the context.

    -a, --alpha <float> -> (Default 0.01) the value of alpha to be used. Must be higher than 0.

    -t, --threshold <int> -> (Default 1) the threshold to choose whether to use the 2D array or the hashtable. Choose 0 for the hashtable as it is faster.
```

An example on how to run:

```
    python3 fcm.py ../example/example.txt -k 3 -a 0.1 -t 0
```

### Generator

The generator.py has 5 arguments: filename, k, alpha, length, seq.

```
    filename -> (Required)the text file that will be used to fill the fcm.

    -k <int> -> (Default 1) the size that is going to be used for the context.

    -a, --alpha <float> -> (Default 0.01) the value of alpha to be used. Must be higher than 0.

    -l, --length <int> -> (Default 100) the length of the generated text.

    -s, --seq <str> -> the initial sequence for the generated text. Must have the same size as k. If no value is provided the initial sequence will be randomly choosed from the alphabet.

```

An example on how to run:

```
    python3 generator.py ../example/example.txt -k 3 -a 0.1 -l 1000 -s "1:1"
```

Generates a text of size 1000, starting with the sequence "1:1"


### Charts

Charts takes a while to run.

```
    python3 charts.py
```
