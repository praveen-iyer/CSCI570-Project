import os
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


@time_and_memory_wrapper
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
    pass


def get_actual_alignment(s1, s2, dp_table):
    pass


if __name__ == "__main__":
    # print(generate_input_string("ACTG",[3,6,1]))
    fpath = os.path.join(
        os.path.dirname(__file__),
        "./UploadedProject/UploadedProject/datapoints/in1.txt",
    )
    print(read_input_file(fpath))
