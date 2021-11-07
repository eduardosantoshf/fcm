import matplotlib.pyplot as plt
from fcm import Fcm
from generator import Generator
import os
import shutil

ks = [1,2,3,4,5]
alphas = [0.0001, 0.001, 0.1, 1, 2]
entropies = [[0]*len(alphas) for _ in range(len(ks))]

for ki, k in enumerate(ks):
    fcm = Fcm("../example/example.txt", k, 0, 0)
    for a,alpha in enumerate(alphas):
        fcm.alpha = alpha
        entropies[ki][a] = fcm.calculate_global_entropy()

# dividir a lista para saber a variacao do k e do alpha

plt.plot(ks, [entropies[i][0] for i in range(len(ks))])
plt.title("entropy change relative to k with alpha=" + str(alphas[0]))
plt.xlabel("k")
plt.ylabel("entropy")
plt.show()

plt.plot(alphas, [entropies[2][i] for i in range(len(alphas))])
plt.title("entropy change relative to alpha with k=" + str(ks[2]))
plt.xlabel("alpha")
plt.ylabel("entropy")
plt.show()


# entropia entre dois ficheiros diferentes
entropies1 = [[0]*len(alphas) for _ in range(len(ks))]
for ki, k in enumerate(ks):
    fcm = Fcm("../example/example1.txt", k, 0, 0)
    for a,alpha in enumerate(alphas):
        fcm.alpha = alpha
        entropies1[ki][a] = fcm.calculate_global_entropy()

plt.plot(ks, [entropies1[i][0] for i in range(len(ks))])
plt.title("entropy change relative to k with alpha=" + str(alphas[0]))
plt.xlabel("k")
plt.ylabel("entropy")
plt.show()

plt.plot(alphas, [entropies1[2][i] for i in range(len(alphas))])
plt.title("entropy change relative to alpha with k=" + str(ks[2]))
plt.xlabel("alpha")
plt.ylabel("entropy")
plt.show()


for ki, k in enumerate(ks):
    plt.plot(ks, [entropies[ki][i] for i in range(len(alphas))], label="k="+str(k))

plt.legend()
plt.show()

# comparação da entropia de textos gerados com base no tamanho
os.mkdir("./.tmp/")
fcm = Fcm("../example/example.txt", 3, 0.1, 0)
sizes = [10000, 50000, 100000, 500000, 1000000, 5000000, 10000000]
gen = Generator(fcm)
entropies = []
for size in sizes:
    filename = "./.tmp/gen" + str(size) + ".txt"
    gen.generate_to_file(filename, size, "1:1")
    n_fcm = Fcm(filename, 3, 0.1, 0)
    entropies.append(n_fcm.calculate_global_entropy())

shutil.rmtree("./.tmp/")

plt.plot(sizes, entropies, label="generated")
plt.plot(sizes, [fcm.calculate_global_entropy() for _ in range(len(sizes))], label="original")
plt.legend()
plt.xlabel("number of generated chars")
plt.ylabel("entropy")
plt.title("Variance of entropy based on the number of chars of the text")
plt.show()


# importancia do alpha na geração de texto
os.mkdir("./.tmp/")
entropies = []
alphas = [0.0001, 0.001, 0.1, 0.3, 0.5, 0.7, 1]
size = 100000
fcm = Fcm("../example/example.txt", 3, 0, 0)
for alpha in alphas:
    fcm.alpha = alpha
    gen = Generator(fcm)
    filename = "./.tmp/gen" + str(size) + ".txt"
    gen.generate_to_file(filename, size, "1:1")
    n_fcm = Fcm(filename, 3, alpha, 0)
    entropies.append(n_fcm.calculate_global_entropy())

shutil.rmtree("./.tmp/")

plt.plot(alphas, entropies)
plt.xlabel("alpha")
plt.ylabel("entropy")
plt.title("Variance of entropy of generated text based on the alpha")
plt.show()

