from scipy.stats import norm
import numpy as np
import math
import random

def callpayoff(S):
    if S >= K:
        return S - K
    else:
        return 0
def putpayoff(S):
    if S <= K:
        return K - S
    else:
        return 0
def combination(n, j, p):
    ans = 0
    for i in range(j + 1, n + 1):
        ans += math.log(i)
    for i in range(1, n - j + 1):
        ans -= math.log(i)
    ans += (n - j) * math.log(p) + j * math.log(1 - p)
    ans = math.exp(ans)
    return ans
def CRR_basic(sd):
    dt = T / n
    u = math.exp(sd * math.sqrt(dt))
    d = math.exp(-sd * math.sqrt(dt))
    prob = (math.exp((r - q) * dt) - d) / (u - d)
    return dt, u, d, prob
def CRR_EU(sd, callornot):
    dt, u, d, prob = CRR_basic(sd)
    value = 0.0
    for j in range(n + 1):
        S = math.log(S0) + (n - j) * math.log(u) + j * math.log(d)
        S = math.exp(S)
        if callornot == True:
            value += combination(n, j, prob) * callpayoff(S)
        else:
            value += combination(n, j, prob) * putpayoff(S)
    value = value * math.exp(-r * T)
    return value
def CRR_AM(sd, callornot):
    dt, u, d, prob = CRR_basic(sd)
    value = [0]
    for j in range(n + 2):
        S = math.log(S0) + (n - j) * math.log(u) + j * math.log(d)
        S = math.exp(S)
        if callornot == True:
            value.append(callpayoff(S))
        else:
            value.append(putpayoff(S))
    for t in range(1, n + 1):
        i = n - t
        for j in range(1, i + 2):
            S = math.log(S0) + (i - j + 1) * math.log(u) + (j - 1) * math.log(d)
            S = math.exp(S)
            tmp = prob * value[j] + (1 - prob) * value[j + 1]
            tmp = tmp / math.exp(r * dt)
            if callornot == True:
                value[j] = max(tmp, callpayoff(S))
            else:
                value[j] = max(tmp, putpayoff(S))
    return value[1]
def BS_basic(sd):
    d1 = (math.log(S0 / K) + (r - q + sd ** 2 / 2) * T) / (sd * math.sqrt(T))
    d2 = (math.log(S0 / K) + (r - q - sd ** 2 / 2) * T) / (sd * math.sqrt(T))
    return d1, d2
def BS(sd, callornot):
    d1, d2 = BS_basic(sd)
    if callornot == True:
        value = S0 * math.exp(-q * T) * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)
    else:
        value = K * math.exp(-r * T) * norm.cdf(-d2) - S0 * math.exp(-q * T) * norm.cdf(-d1)
    return value
def normfirst(d, sd):
    ans = math.exp(-(d ** 2) / 2) / math.sqrt(2 * math.pi)
    ans = ans * ((-math.log(S0/K) - (r - q) * T) / (sd ** 2 * math.sqrt(T)) + (math.sqrt(T) / 2))
    return ans
def BSfirst(sd, callornot):
    d1, d2 = BS_basic(sd)
    if callornot == True:
        ans = S0 * math.exp(-q * T) * normfirst(d1, sd) - K * math.exp(-r * T) * normfirst(d2, sd)
    else:
        ans = K * math.exp(-r * T) * normfirst(-d2, sd) - S0 * math.exp(-q * T) * normfirst(-d1, sd)
    
    return ans

S0 = 50
K = 50
r = 0.1
q = 0.05
T = 0.5
P = 6.04
n = 10000
criterion = 0.0001

#for CRR


#Bisection
a = 0.00001
b = 2
ans = []
for i in range(6):
    BSornot = True
    EUornot = True
    callornot = True
    if i in [2,3,4,5]:
        BSornot = False
    if i in [4,5]:
        EUornot = False
    if i in [1,3,5]:
        callornot = False
    diff = criterion + 1
    while(diff >= criterion):
        x = (a + b) / 2
        if BSornot == True:
            f1 = BS(a, callornot) - P
            f2 = BS(x, callornot) - P
        elif EUornot == True:
            f1 = CRR_EU(a, callornot) - P
            f2 = CRR_EU(x, callornot) - P
        else:
            f1 = CRR_AM(a, callornot) - P
            f2 = CRR_AM(x, callornot)
        if f1 * f2 < 0:
            b = x
        else:
            a = x
        diff = b - a
    ans.append(x)

print("Implied volatility by Bisection method:")
print("-BS.European.Call:  %0.4f" % ans[0])
print("-BS.European.Put:   %0.4f" % ans[1])
print("-CRR.European.Call: %0.4f" % ans[2])
print("-CRR.European.Put:  %0.4f" % ans[3])
print("-CRR.American.Call: %0.4f" % ans[4])
print("-CRR.American.Put:  %0.4f" % ans[5])
print("Continue by Newton's method:")

#Newton's
for i in range(6):
    BSornot = True
    EUornot = True
    callornot = True
    if i in [2,3,4,5]:
        BSornot = False
    if i in [4,5]:
        EUornot = False
    if i in [1,3,5]:
        callornot = False
    x = ans[i]
    diff = criterion + 1
    while(diff >= criterion):
        x_next = x - BS(x, callornot) / BSfirst(x, callornot)
        diff = abs(x_next - x)
        x = x_next
    ans[i] = x

print("-BS.European.Call:  %0.4f" % ans[0])
print("-BS.European.Put:   %0.4f" % ans[1])
print("-CRR.European.Call: %0.4f" % ans[2])
print("-CRR.European.Put:  %0.4f" % ans[3])
print("-CRR.American.Call: %0.4f" % ans[4])
print("-CRR.American.Put:  %0.4f" % ans[5])