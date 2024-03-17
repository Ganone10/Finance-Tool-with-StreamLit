from math import *


def d1_compute(S, K, T, sigma, r, d):
    num = log(S / K) + (r - d + sigma ** 2 / 2) * T
    den = sigma * sqrt(T)
    d1 = num / den
    return d1


def d2_compute(S, K, T, sigma, r, d):
    d1 = d1_compute(S, K, T, sigma, r, d)
    d2 = d1 - sigma * sqrt(T)
    return d2


def approx_N(x):
    alpha = 0.2316419
    a1 = 0.319381530
    a2 = -0.356563782
    a3 = 1.781477937
    a4 = -1.821255978
    a5 = 1.330274429
    y = 1 / (1 + alpha * x)
    if (x >= 0):
        N_x = 1 - (1 / sqrt(2 * pi)) * exp(-x ** 2 / 2) * (
                    a1 * y + a2 * y ** 2 + a3 * y ** 3 + a4 * y ** 4 + a5 * y ** 5)
        return N_x
    else:
        N_x = 1 - approx_N(-x)
        return N_x


class Pricer:
    Type = "BSM"

    def __init__(self, Ticker, S, K, T, sigma, r, d):
        self.Ticker = Ticker
        self.S = S
        self.K = K
        self.T = T
        self.sigma = sigma
        self.r = r
        self.d = d

    def __str__(self):
        return f"{self.S} is  value of the stock {self.Ticker}"

    ## function to approximate the computation of gaussian cdf
    def CALL(self):
        d1 = d1_compute(self.S, self.K, self.T, self.sigma, self.r, self.d)
        d2 = d2_compute(self.S, self.K, self.T, self.sigma, self.r, self.d)
        call_0 = exp(-self.d * self.T) * self.S * approx_N(d1) - approx_N(d2) * self.K * exp(-self.r * self.T)
        return call_0

    def PUT(self):
        d1 = d1_compute(self.S, self.K, self.T, self.sigma, self.r, self.d)
        d2 = d2_compute(self.S, self.K, self.T, self.sigma, self.r, self.d)
        put_0 = approx_N(-d2) * self.K * exp(-self.r * self.T) - approx_N(-d1) * self.S * exp(-self.d * self.T)
        return put_0


class Call_Put(Pricer):
    pass


#pricer = Call_Put("MC.PA", 100, 120, 2, 0.2, 0.02, 0)
#print(pricer)
#print(pricer.CALL())
#print(pricer.PUT())
