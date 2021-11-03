import matplotlib.pyplot as plt
from fcm import Fcm


ks = [1,2,3,4,5]
alphas = [0.0001, 0.001, 0.1, 1, 2]
entropies = [[0]*len(alphas) for _ in range(len(ks))]

for ki, k in enumerate(ks):
    fcm = Fcm("../example/example.txt", k, 0)
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

for k in range(len(ks)):
    plt.plot(ks, [entropies[k][i] for i in range(len(alphas))], label="k="+str(k))

plt.legend()
plt.show()