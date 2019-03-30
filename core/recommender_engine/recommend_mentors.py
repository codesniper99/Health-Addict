
class X:
    def __init__(self, id,pref_count, current_count, score):
        self.id = id
        self.pref_count = pref_count
        self.current_count = current_count
        self.score = score

def cmp_to_key(mycmp):
    'Convert a cmp= function into a key= function'
    class K:
        def __init__(self, obj, *args):
            self.obj = obj
        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0
        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0
        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0
        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0
        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0
        def __ne__(self, other):
            return mycmp(self.obj, other.obj) != 0
    return K
"""
score -> total score/rating
pref_count -> maximum students he/she can handle
current_count -> the current count
"""
def comparator_for_mentors(a , b):
    if (a.pref_count - a.current_count) == (b.pref_count - b.current_count):
        return b.score - a.score
    else:
        return (b.pref_count - b.current_count) - (a.pref_count - a.current_count)

def recommend_the_mentors(list_of_mentors):
    xx = sorted(list_of_mentors , key=cmp_to_key(comparator_for_mentors))
    return xx

p = []

with open("input.txt") as f:
    for line in f:
        currentline = line.split(",")
        temp = currentline[3]
        temp = temp.rstrip()
        p.append(X((int)(currentline[0]) , (int)(currentline[1]) , (int)(currentline[2]) , (float)(temp)))

for q in p:
    print(q.id,end=' ')

p = recommend_the_mentors(p)

print('\n')

for q in p:
    print(q.id,end=' ')