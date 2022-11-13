import sys
import time
import psutil


def time_and_memory_wrapper(f):
    def wrapped(*args, **kwargs):
        start_time = time.time()
        result = f(*args, **kwargs)
        end_time = time.time()
        total_time = (end_time - start_time) * 1000
        process = psutil.Process()
        memory_info = process.memory_info()
        memory_consumed = int(memory_info.rss / 1024)
        return total_time, memory_consumed, result

    return wrapped


def generate_input_string(base_str: str, l: list[int]) -> str:
    new_str = base_str
    for el in l:
        new_str = new_str[: el + 1] + new_str + new_str[el + 1 :]
    return new_str


def read_input_file(file_path):
    with open(file_path, "r") as f:
        data = f.read().split("\n")

    base_str1, base_str2 = data[0].strip(), None
    l1, l2 = [], []
    for i in range(1, len(data)):
        line = data[i].strip()
        if line == "":
            continue
        if base_str2 is None and line.isnumeric():
            l1.append(int(line))
        elif base_str2 is None and not line.isnumeric():
            base_str2 = line
        else:
            l2.append(int(line))

    new_str1 = generate_input_string(base_str1, l1)
    new_str2 = generate_input_string(base_str2, l2)

    return new_str1, new_str2


char2index = {"A": 0, "C": 1, "G": 2, "T": 3}
alphas = [[0, 110, 48, 94], [110, 0, 118, 48], [48, 118, 0, 110], [94, 48, 110, 0]]

delta = 30


def get_dp_table(s1, s2, alphas, delta):
    m = len(s1)
    n = len(s2)

    dp = [[0 for i in range(n + 1)] for i in range(m + 1)]

    for i in range(n + 1):
        dp[0][i] = i * delta
    for j in range(m + 1):
        dp[j][0] = j * delta

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = min(
                    dp[i - 1][j - 1]
                    + alphas[char2index[s1[i - 1]]][char2index[s2[j - 1]]],
                    dp[i - 1][j] + delta,
                    dp[i][j - 1] + delta,
                )
    return dp


def sequenceAlignment(s1, s2, alphas, delta):
    m = len(s1)
    n = len(s2)
    dp = get_dp_table(s1, s2, alphas, delta)

    l = m + n

    s1pos = l
    s2pos = l

    a1ans = [0 for i in range(l + 1)]
    a2ans = [0 for i in range(l + 1)]

    i = m
    j = n

    while i != 0 and j != 0:
        if s1[i - 1] == s2[j - 1]:
            a1ans[s1pos] = s1[i - 1]
            s1pos -= 1
            a2ans[s2pos] = s2[j - 1]
            s2pos -= 1
            i -= 1
            j -= 1
        elif (
            dp[i - 1][j - 1] + alphas[char2index[s1[i - 1]]][char2index[s2[j - 1]]]
            == dp[i][j]
        ):
            a1ans[s1pos] = s1[i - 1]
            s1pos -= 1
            a2ans[s2pos] = s2[j - 1]
            s2pos -= 1
            i -= 1
            j -= 1
        elif dp[i - 1][j] + delta == dp[i][j]:
            a1ans[s1pos] = s1[i - 1]
            s1pos -= 1
            a2ans[s2pos] = "_"
            s2pos -= 1
            i -= 1
        elif dp[i][j - 1] + delta == dp[i][j]:
            a1ans[s1pos] = "_"
            s1pos -= 1
            a2ans[s2pos] = s2[j - 1]
            s2pos -= 1
            j -= 1

    while s1pos > 0:
        if i > 0:
            i -= 1
            a1ans[s1pos] = s1[i]
            s1pos -= 1
        else:
            a1ans[s1pos] = "_"
            s1pos -= 1

    while s2pos > 0:
        if j > 0:
            j -= 1
            a2ans[s2pos] = s2[j]
            s2pos -= 1
        else:
            a2ans[s2pos] = "_"
            s2pos -= 1

    idd = 1

    for i in range(l, 0, -1):
        if a2ans[i] == "_" and a1ans[i] == "_":
            idd = i + 1
            break
    a1 = []
    for i in range(idd, l + 1):
        a1.append(a2ans[i])
    a2 = []
    for i in range(idd, l + 1):
        a2.append(a1ans[i])
    a1 = "".join(a1)
    a2 = "".join(a2)
    return dp[m][n], a1, a2


@time_and_memory_wrapper
def sequenceAlignmentEfficient(string1, string2, alphas, delta):
    def NWScore(string1, string2, alphas, delta):
        m = len(string1)
        n = len(string2)

        lastline = [0 for i in range(n + 1)]

        table = [[0 for i in range(n + 2)] for j in range(2)]

        table[0][0] = 0

        for j in range(1, n + 2):
            table[0][j] = table[0][j - 1] + delta

        for i in range(1, m + 1):
            table[1][0] = table[0][0] + delta
            for j in range(1, n + 1):
                table[1][j] = min(
                    table[0][j - 1]
                    + alphas[char2index[string1[i - 1]]][char2index[string2[j - 1]]],
                    table[0][j] + delta,
                    table[1][j - 1] + delta,
                )
            table[0][:] = table[1][:]

        for j in range(n + 1):
            lastline[j] = table[1][j]

        return lastline

    def PartitionY(scoreL, scoreR):
        zipped_lists = zip(scoreL, scoreR)
        sum_lists = [x + y for (x, y) in zipped_lists]
        return sum_lists.index(min(sum_lists)), min(sum_lists)

    def Hirschberg(string1, string2, alphas, delta):
        Z = ""
        W = ""
        m = len(string1)
        n = len(string2)

        # Base cases
        if m <= 2 or n <= 2:
            minScore, Z, W = sequenceAlignment(string1, string2, alphas, delta)
            # minScoreList.append(minScore)
            # print(minScoreList)
        else:

            # Divide Step
            string1mid = m // 2
            scoreL = NWScore(string1[:string1mid], string2, alphas, delta)
            revString1 = string1[string1mid:]
            scoreR = NWScore(revString1[::-1], string2[::-1], alphas, delta)
            string2mid, minScore = PartitionY(scoreL, scoreR[::-1])
            # minScoreList.append(minScore)

            # Conquer step
            minScore1, Z1, W1 = Hirschberg(
                string1[:string1mid], string2[:string2mid], alphas, delta
            )
            minScore2, Z2, W2 = Hirschberg(
                string1[string1mid:], string2[string2mid:], alphas, delta
            )

            # Combine step
            Z = str(Z1) + str(Z2)
            W = str(W1) + str(W2)

            minScore = minScore1 + minScore2

        return minScore, Z, W

    return Hirschberg(string1, string2, alphas, delta)


if __name__ == "__main__":
    fpath = sys.argv[1]
    out_path = sys.argv[2]
    string1, string2 = read_input_file(fpath)
    totalt, totalm, (mincost, a1, a2) = sequenceAlignmentEfficient(
        string2, string1, alphas, delta
    )

    out_str = []
    out_str.append(str(mincost))
    out_str.append(a1)
    out_str.append(a2)
    out_str.append(str(totalt))
    out_str.append(str(totalm))
    out_str = "\n".join(out_str)

    with open(out_path, "w") as f:
        f.write(out_str)
