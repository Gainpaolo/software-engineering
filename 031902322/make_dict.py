import numpy as np

path = 'E:/大三上/软件工程/第一次编程作业/randl.txt'
dictionary = {}
with open(path, 'r', encoding="utf-8") as file:
    for line in file:
        a = line.strip()[1]
        dictionary[a] = line.strip()[6] + line.strip()[7]
print(dictionary)
# Save

np.save('my_words.npy', dictionary)
