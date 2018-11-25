import json

with open('12.txt') as f:
    max_weight, _volume = [float(x) for x in next(f).split()]
    data = []
    for line in f:
        data.append([float(x) for x in line.split()])
