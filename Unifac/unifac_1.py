import numpy as np
import pandas as pd


U = 5

# m = Es el número de moléculas en la mezcla
m = 2

# g = Es el número de grupos funcionales en la mezcla
# g = 3
g = 7

# T = 331.15  # K
T = 328
#     Etanol - n-Hexano
# xj = [0.332 , 0.668]
xj = np.array([0.383, 0.617])

# --------------------------------------------------------
# Agua - Isoamil alcohol - ácido acético
#     H2O CH3 CH2 CH  OH  COOH  COOCH3
# Agua
# Isoamil acetato
# Ácido acético
v1 = np.array([1, 0, 0, 0, 0, 0, 0])
v2 = np.array([0, 2, 2, 1, 0, 0, 1])
v3 = np.array([0, 1, 0, 0, 0, 1, 0])

# v = np.array([v1, v2, v3])
v = np.array([v1, v3])

print("v = ", v)

# Agua - Isoamil acetato - ácido acético
#               H2O     CH3    CH2    CH     OH    COOH   COOCH3
R = np.array([0.9200, 0.9011, 0.6744, 0.4469, 1.0000, 1.3013, 1.9031])
Q = np.array([1.4000, 0.8480, 0.5400, 0.2280, 1.2000, 1.2240, 1.7280])

print("R = ", R)
filasRQ = ["R", "Q"]
labelsRQ = ["H2O", "CH3", "CH2", "CH", "OH", "COOH", "COOCH3"]

dfRQ = pd.DataFrame(data=[R, Q], index=filasRQ, columns=labelsRQ)
print(dfRQ)

# --------------------------------------------------------

# Agua - Isoamil alcohol - Ácido acético
# H2O     CH3     CH2     CH      OH      COOH    COOCH3
labels = ["H2O", "CH3", "CH2", "CH", "OH", "COOH", "COOCH3"]
a = np.array([[0, 300, 300, 300, -229.1, -14.09, 72.8700],
				[1318, 0, 0, 0, 986.5, 663.5, 232.100],
				[1318, 0, 0, 0, 986.5, 663.5, 232.100],
				[1318, 0, 0, 0, 986.5, 663.5, 232.100],
				[353.5, 156.4, 156.4, 156.4, 0, 199, 101.100],
				[-66.17, 315.3, 315.3, 315.3, -151, 0, -256.300],
				[200.800, 114.800, 114.800, 114.800, 245.400, 660.200, 0]])


df = pd.DataFrame(a, index=labels, columns=labels)
print(df)

# ----------------------------------------------------------------------
A = np.exp(-a / T)
r = np.sum(R * v, axis=1)
q = np.sum(Q * v, axis=1)

rxj = r * xj
rx = np.sum(rxj)
J = rxj / rx

qxj = q * xj
qx = np.sum(qxj)
L = qxj / qx

li = 5 * (r - q) - (r - 1)
lnYCi = np.log(J / xj) + 5 * q * np.log(L / J) + li - (J / xj) * (np.sum(xj * li))

xg = (v.T / np.sum(v, axis=1)).T
Lg = ((Q * xg).T / np.sum(Q * xg, axis=1)).T

print("A = ", A)
print("r = ", r)
print("q = ", q)
print("rxj = ", rxj)
print("rx = ", rx)
print("J = ", J)
print("qxj = ", qxj)
print("qx = ", qx)
print("L = ", L)
print("li = ", li)
print("lnYCi = ", lnYCi)
print("xg = ", xg)
print("Lg = ", Lg)

# J = 0.20591   0.79409
# L = 0.29549   0.70451
# li = -2.32000  -0.55040
# lnYCi = 0.248043   0.042572

# ----------------------------------------------------------------------

# Lg =

#   1.00000   0.00000
#   0.00000   0.40927
#   0.00000   0.00000
#   0.00000   0.00000
#   0.00000   0.00000
#   0.00000   0.59073
#   0.00000   0.00000

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
ST = Lg @ A


# ST =

#   1.00000   0.40066   0.40066   0.40066   2.01069   1.04389   0.80078
#   0.73014   0.63516   0.63516   0.63516   0.95633   0.64487   1.49217


# --------------------------------------------

# STa = Lg[1, :] * A
# STa = Lg[1, :] * A

STa = np.array([lg * A for lg in Lg])

print("A = ", A)
print("Lg = ", Lg[1, :])

print("STa = ", STa)


# STa =

#   1.00000   0.00000   0.00000   0.00000   0.00000   0.00000   0.00000
#   0.01798   0.00000   0.00000   0.00000   0.00000   0.00000   0.00000
#   0.01798   0.00000   0.00000   0.00000   0.00000   0.00000   0.00000
#   0.01798   0.00000   0.00000   0.00000   0.00000   0.00000   0.00000
#   0.34036   0.00000   0.00000   0.00000   0.00000   0.00000   0.00000
#   1.22353   0.00000   0.00000   0.00000   0.00000   0.00000   0.00000
#   0.54216   0.00000   0.00000   0.00000   0.00000   0.00000   0.00000
#   0.00000   0.16398   0.00000   0.00000   0.00000   0.61666   0.00000
#   0.00000   0.40927   0.00000   0.00000   0.00000   0.07814   0.00000
#   0.00000   0.40927   0.00000   0.00000   0.00000   0.07814   0.00000
#   0.00000   0.40927   0.00000   0.00000   0.00000   0.07814   0.00000
#   0.00000   0.25405   0.00000   0.00000   0.00000   0.32203   0.00000
#   0.00000   0.15650   0.00000   0.00000   0.00000   0.59073   0.00000
#   0.00000   0.28841   0.00000   0.00000   0.00000   0.07893   0.00000


k = 1
i = 1

wwww = Q * (1 - np.log(ST[0, :]))
ppp = STa[0][0, :] / ST[0, :]


lnTg = Q * (1 - np.log(ST[0, :]) - np.sum(STa[0][0, :] / ST[0, :]))

# lnTg = (STa[0][0,:]  / ST[0, :])

print("Q = ", Q[0])
print("ST = ", ST[0, :])
print("STa = ", STa[0][0, :])
print("lnTg = ", lnTg)
print("wwww = ", wwww)
print("ppp = ", ppp)

# www =

#   1.40000   1.62361   1.03390   0.43654   0.36183   1.17142   2.11190

# for i = 1 : 1 : m      %Molécula (i)

#   for k = 1 : 1 : g   %Grupo funcional (k)

#      if i == 1
#         lnTg(i,k) = Q(k,1).*(1 - log(ST(i,k)) - sum(STa(k,:)./ST(i,:)));
#      elseif i == 2
#         lnTg(i,k) = Q(k,1).*(1 - log(ST(i,k)) - sum(STa(k+g,:)./ST(i,:)));
#      elseif i == 3
#         lnTg(i,k) = Q(k,1).*(1 - log(ST(i,k)) - sum(STa(k+2*g,:)./ST(i,:)));
#      end

#   end

# end
# %lnT(1,k) = Q(k,1).*(1 - log(STg(1,k)) - sum(STga(k,:)./STg));

# lnTg






