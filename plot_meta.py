import matplotlib.pyplot as plt
import numpy as np

def smooth(scalars, weight: float):  # Weight between 0 and 1
    last = scalars[0]  # First value in the plot (first timestep)
    smoothed = list()
    for point in scalars:
        smoothed_val = last * weight + (1 - weight) * point  # Calculate smoothed value
        smoothed.append(smoothed_val)                        # Save it
        last = smoothed_val                                  # Anchor the last smoothed value

    return np.array(smoothed)

files = [
    "results_meta",
    "results_no_meta",
]

data = {}

for file in files:
    data[file] = {
        "x": [],
        "y": [],
    }

    with open("./%s.txt" % file, 'r') as f:
        lines = f.readlines()
        cur = -1
        for line in lines:
            if line[:5] == "#test":
                data[file]["x"].append([])
                data[file]["y"].append([])
                cur += 1
            elif cur >= 0:
                line = line.strip().split(' ')
                if len(line) == 2: 
                    line = [float(x) for x in line]
                    data[file]["x"][cur].append(line[0])
                    data[file]["y"][cur].append(line[1])

#print(data)
colors = ["orange", "gray"]

for file, color in zip(files, colors):
    for x,y in zip(data[file]["x"], data[file]["y"]):
        x, y = x[:10], y[:10]
        y = smooth(y, 0.0)
        plt.plot(x, y, color=color)

plt.xlabel("Timesteps")
plt.ylabel("Reward")
plt.title("Few-shot learning of new opponent. Orange: meta, Grey: no meta")
plt.savefig("meta.png")
