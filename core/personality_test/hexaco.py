#   HEXACO Score Evaluation


def evaluate_score(x):
    print('Generating HEXACO Score ...')
    simple = [0, 1, 2, 3, 4, 5]
    reverse = [0, 5, 4, 3, 2, 1]
    a, b, c, d, e, f = 0, 0, 0, 0, 0, 0
    cta, ctb, ctc, ctd, cte, ctf = 0, 0, 0, 0, 0, 0
    for i in range(len(x)):
        p = i + 1
        if p in (12, 24, 30, 42, 48, 60):
            a += reverse[x[i]]
            cta += 1
        if p in (6, 18, 36, 54):
            a += simple[x[i]]
            cta += 1
        if p in (35, 41, 53, 59):
            b += reverse[x[i]]
            ctb += 1
        if p in (5, 11, 17, 23, 29, 47):
            b += simple[x[i]]
            ctb += 1
        if p in (10, 28, 46, 52):
            c += reverse[x[i]]
            ctc += 1
        if p in (4, 16, 22, 34, 40, 58):
            c += simple[x[i]]
            ctc += 1
        if p in (9, 15, 21, 57):
            d += reverse[x[i]]
            ctd += 1
        if p in (3, 27, 29, 33, 45, 51):
            d += simple[x[i]]
            ctd += 1
        if p in (14, 20, 26, 32, 44, 56):
            e += reverse[x[i]]
            cte += 1
        if p in (2, 8, 38, 50):
            e += simple[x[i]]
            cte += 1
        if p in (1, 19, 31, 49, 55):
            f += reverse[x[i]]
            ctf += 1
        if p in (13, 25, 37, 43):
            f += simple[x[i]]
            ctf += 1
    resa = float(a) / float(cta)
    resb = float(b) / float(ctb)
    resc = float(c) / float(ctc)
    resd = float(d) / float(ctd)
    rese = float(e) / float(cte)
    resf = float(f) / float(ctf)
    return [resa, resb, resc, resd, rese, resf]
