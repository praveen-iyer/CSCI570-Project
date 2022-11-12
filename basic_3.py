import os
import time
import psutil

delta = 30
alpha = {}
alpha["AA"] = 0
alpha["AC"] = 110
alpha["AG"] = 48
alpha["AT"] = 94
alpha["CC"] = 0
alpha["CG"] = 118
alpha["CT"] = 48
alpha["GG"] = 0
alpha["GT"] = 110
alpha["TT"] = 0


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


def calculate_alignment_value_and_dp_table(s1, s2):
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for i in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i * delta
    for j in range(n + 1):
        dp[0][j] = j * delta

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            dp[i][j] = min(
                dp[i - 1][j - 1] + alpha["".join(sorted(s1[i - 1] + s2[j - 1]))],
                dp[i][j - 1] + delta,
                dp[i - 1][j] + delta,
            )
    return dp[m][n], dp


def get_actual_alignment(s1, s2, dp):
    m, n = len(s1), len(s2)
    as1, as2 = ["0"] * (m + n + 1), ["0"] * (m + n + 1)
    pos1, pos2, i, j = m + n, m + n, m, n
    while i != 0 and j != 0:
        t = [float("inf"), float("inf"), float("inf")]
        if i > 0 and j > 0:
            t[0] = dp[i - 1][j - 1] + alpha["".join(sorted(s1[i - 1] + s2[j - 1]))]
        if i > 0:
            t[1] = dp[i - 1][j] + delta
        if j > 0:
            t[2] = dp[i][j - 1] + delta
        min_ind = t.index(min(t))
        if min_ind == 0:
            as1[pos1] = s1[i - 1]
            as2[pos2] = s2[j - 1]
            i, j = i - 1, j - 1
        elif min_ind == 1:
            as1[pos1] = s1[i - 1]
            as2[pos2] = "_"
            i -= 1
        else:
            as1[pos1] = "_"
            as2[pos2] = s2[j - 1]
            j -= 1
        pos1 -= 1
        pos2 -= 1

    while pos1 > 0:
        if i > 0:
            i -= 1
            as1[pos1] = s1[i - 1]
            pos1 -= 1
        else:
            as1[pos1] = "_"
            pos1 -= 1
    while pos2 > 0:
        if j > 0:
            j -= 1
            as2[pos2] = s2[j - 1]
            pos2 -= 1
        else:
            as2[pos2] = "_"
            pos2 -= 1

    as1, as2 = "".join(as1), "".join(as2)
    start_ind = 1
    while s1[start_ind] == "_" and s2[start_ind] == "_":
        start_ind += 1
    as1, as2 = as1[start_ind:], as2[start_ind:]

    return as1, as2


if __name__ == "__main__":
    # print(generate_input_string("ACTG",[3,6,1]))
    fpath = os.path.join(
        os.path.dirname(__file__),
        "./UploadedProject/UploadedProject/SampleTestCases/input1.txt",
    )
    s1, s2 = read_input_file(fpath)
    # s1, s2 = "A", "C"
    print(s1, "\n", s2, "\n", len(s1), len(s2))
    min_cost, dp = calculate_alignment_value_and_dp_table(s1, s2)
    as1, as2 = get_actual_alignment(s1, s2, dp)
    print(min_cost)
    # print(dp)
    print(as1, "\n", as2)
    print(len(as1), len(as2))

