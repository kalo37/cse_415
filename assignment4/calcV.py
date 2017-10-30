def calcV(N, S, I, a):
	return N / S * I * (2 * a - 1) - 0.01

print(calcV(6, 5, 0.3, 0.3))