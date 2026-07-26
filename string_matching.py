import time

# -------------------- Naive Algorithm --------------------
def naive_search(text, pattern):
    n = len(text)
    m = len(pattern)
    count = 0

    for i in range(n - m + 1):
        if text[i:i + m] == pattern:
            count += 1

    return count


# -------------------- Rabin-Karp Algorithm --------------------
def rabin_karp(text, pattern):
    d = 256
    q = 101

    n = len(text)
    m = len(pattern)

    if m > n:
        return 0

    h = pow(d, m - 1, q)

    p = 0
    t = 0

    for i in range(m):
        p = (d * p + ord(pattern[i])) % q
        t = (d * t + ord(text[i])) % q

    count = 0

    for i in range(n - m + 1):

        if p == t:
            if text[i:i + m] == pattern:
                count += 1

        if i < n - m:
            t = (d * (t - ord(text[i]) * h) + ord(text[i + m])) % q
            if t < 0:
                t += q

    return count


# -------------------- KMP Algorithm --------------------
def compute_lps(pattern):
    lps = [0] * len(pattern)

    length = 0
    i = 1

    while i < len(pattern):

        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1

        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    return lps


def kmp_search(text, pattern):
    lps = compute_lps(pattern)

    i = 0
    j = 0
    count = 0

    while i < len(text):

        if text[i] == pattern[j]:
            i += 1
            j += 1

        if j == len(pattern):
            count += 1
            j = lps[j - 1]

        elif i < len(text) and text[i] != pattern[j]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

    return count


# -------------------- Main Program --------------------
text = "ABABDABACDABABCABABABABCABAB"
pattern = "ABABCABAB"

# Naive
start = time.perf_counter()
naive_matches = naive_search(text, pattern)
naive_time = (time.perf_counter() - start) * 1_000_000

# Rabin-Karp
start = time.perf_counter()
rk_matches = rabin_karp(text, pattern)
rk_time = (time.perf_counter() - start) * 1_000_000

# KMP
start = time.perf_counter()
kmp_matches = kmp_search(text, pattern)
kmp_time = (time.perf_counter() - start) * 1_000_000

# Results
print("=" * 50)
print("STRING MATCHING ALGORITHM COMPARISON")
print("=" * 50)

print(f"Text    : {text}")
print(f"Pattern : {pattern}\n")

print("{:<15}{:<10}{:<15}".format("Algorithm", "Matches", "Time (µs)"))
print("-" * 45)

print("{:<15}{:<10}{:<15.2f}".format("Naive", naive_matches, naive_time))
print("{:<15}{:<10}{:<15.2f}".format("Rabin-Karp", rk_matches, rk_time))
print("{:<15}{:<10}{:<15.2f}".format("KMP", kmp_matches, kmp_time))