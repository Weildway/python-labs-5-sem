import numpy as np


def GtoP(G):
    k = np.shape(G)[0]
    n = np.shape(G)[1]
    P = G[::, n - k + 1:]
    return P.astype(int)


def GtoH(G):
    k = np.shape(G)[0]
    n = np.shape(G)[1]
    P = GtoP(G)
    PT = np.transpose(P)
    Ik = np.eye(n - k)
    H = np.concatenate((PT, Ik), axis=1)
    return H.astype(int)


G = np.matrix([[1, 0, 0, 0, 1, 1, 1],
               [0, 1, 0, 0, 1, 1, 0],
               [0, 0, 1, 0, 1, 0, 1],
               [0, 0, 0, 1, 0, 1, 1]])
H = GtoH(G)
print(H)
