import math, collections


# Vector math functions

def magnitude(v):
    return math.sqrt(sum(v[i]*v[i] for i in range(len(v))))

def add(u, v):
    return [(a+b) for (a, b) in zip(u, v)]

def sub(u, v):
    return [(a-b) for (a, b) in zip(u, v)]

def dot(u, v):
    if isinstance(u, collections.Iterable):
        return sum((a*b) for a, b in zip(u, v))
    else:
        return 0

def length(v):
    return math.sqrt(dot(v, v))

def angle(v1, v2):
    if (length(v1) * length(v2)) != 0:
        return math.acos(dot(v1, v2) / (length(v1) * length(v2)))
    else:
        return 0

def normalize(v):
    vmag = magnitude(v)
    if vmag != 0:
        return [ v[i]/vmag  for i in range(len(v)) ]
