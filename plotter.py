import matplotlib.pyplot as plt

with open("plot_values.txt", "r") as f:
    raw_data = f.read().split("\n")

basic = raw_data[1:16]
basic = list(map(lambda a: [float(x) for x in a[3:].strip().split(",")], basic))

basic_time, basic_memory = zip(*basic)

efficient = raw_data[18:33]
efficient = list(map(lambda a: [float(x) for x in a[3:].strip().split(",")], efficient))
efficient_time, efficient_memory = zip(*efficient)
xs = [16, 64, 128, 256, 384, 512, 768, 1024, 1280, 1536, 2048, 2560, 3072, 3584, 3968]

plt.figure()
plt.plot(xs, basic_time)
plt.plot(xs, efficient_time)
plt.title("Time for different algorithm")
plt.xlabel("Size of problem (m+n)")
plt.ylabel("Time (in milli seconds)")
plt.legend(("Basic", "Efficient"))
plt.show()
# plt.savefig("time.png")

plt.figure()
plt.plot(xs, basic_memory)
plt.plot(xs, efficient_memory)
plt.title("Memory for different algorithm")
plt.xlabel("Size of problem (m+n)")
plt.ylabel("Memory (in kilo bytes)")
plt.legend(("Basic", "Efficient"))
plt.show()
# plt.savefig("memory.png")

