import random as r
import enum

# [loc (x,y), length, deltaH, difficulty, terrain]

class Hikes(enum.Enum):
    Rocky = 0
    mountains = 1
    lake = 2
    river = 3
    beach = 4
    forest = 5
    bike = 6

numClasses = 6

def avgPoint(vectors):
    Xs = 0
    Ys = 0
    for vec in vectors:
        Xs += vec[0][0]
        Ys += vec[0][1]

    return (Xs/len(vectors), Ys/len(vectors))

def avgHike(vectors):
    res = 0
    for item in vectors:
        res += item[4]
    return res/len(vectors)

def avgNum(vectors):
    length = 0
    height = 0
    diff = 0
    for vec in vectors:
        length += vec[1]
        height += vec[2]
        diff += vec[3]

    return length/len(vectors), height/len(vectors), diff/len(vectors)

def avg(vectors):
    a = avgPoint(vectors)
    b, c, d = avgNum(vectors)
    e = avgHike(vectors)
    return [a,b,c,d,e]

def distance(A, B):
    assert(len(A) == len(B))
    values = [0 for x in range(len(A))]

    for index in range(len(A)):

        if isinstance(A[index], tuple):
            values[index] = ((B[index][0]-A[index][0])**2+(B[index][1]-A[index][1])**2)**0.5

        elif isinstance(A[index], float):
            values[index] = abs(A[index]-B[index])

        elif isinstance(A[index], int):
            values[index] = abs(A[index]-B[index])

        else:
            values[index] =  0 if A[index] == B[index] else 1

    return round(sum(values)/(len(A)+1), ndigits = 5)

def normalize(x, mn, mx):

    if isinstance(x, tuple):
        return (round((x[0]-mn[0])/max(1,mx[0]-mn[0]), ndigits = 5),round((x[1]-mn[1])/max(1, mx[1]-mn[1]), ndigits = 5))

    elif isinstance(x, Hikes):
        return round(int(x.value)/numClasses, ndigits = 5)

    else:
        return round((x-mn)/(mx-mn), ndigits = 5)

def generateFrame():
    a = (r.random()*90,r.random()*180)
    b = r.random() * 20
    c = r.random()
    d = r.randint(0,5)
    e = Hikes(r.randrange(0,7))
    return [a,b,c,d,e]

def minmaxArrs(data):
    mins = [(-90,-180), 0, 0, 0, 0]
    maxs = [(90,180), 0, 0, 5, 6]
    for x in range(len(data)):
        if data[x][1] > maxs[1]:
            maxs[1] = data[x][1]

        if data[x][2] > maxs[2]:
            maxs[2] = data[x][2]

    return mins, maxs

def normalizeVector(vec, mins, maxs):
    result = []
    for item in range(len(vec)):
        result.append(normalize(vec[item], mins[item], maxs[item]))
    return result

def normAll(data, min, max):
    newData = []

    for item in data:
        newData.append(normalizeVector(item, min, max))

    return newData

def predict(frame, data, k= 3):
    keyframes = []
    for item in data:
        keyframes.append((distance(frame, item), item))
    keyframes.sort(key = lambda x: x[0])
    return keyframes[1:k+1]

#testing_data = [ [, , r.randrange(20,300), r.randint(0,5), Hikes[r.randrange(0,7)] ] for _ in range(100)]
testing_data = [generateFrame() for _ in range(100)]
minimum, maximum = minmaxArrs(testing_data)

testing_data = normAll(testing_data, minimum, maximum)
print('predicting: ', testing_data[26])
vals = predict(testing_data[26], testing_data, k =3)

for val in vals:
    print("val ", val)

#print(r.sample(testing_data, k=5))

print(avg(r.sample(testing_data, k = 5)))
#testA = [(1,6), 5.6, 240, 4, Hikes.beach]
#testB = [(2,-3), 8.2, 100, 3, Hikes.mountains]

#print(distance(testA, testB))

#for i in range(88):
#    print(distance(testing_data[i], testing_data[i+1]))
