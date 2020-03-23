import Constants
import Paraphrase
import Constants

from Similarity import Similarity


def distance(source, target):
    init_similarity()

    if source == target:
        return (0,0,0)

    slen, tlen = len(source), len(target)
    dist = [[(0,0,0) for i in range(tlen + 1)] for x in range(slen + 1)]
    for i in range(slen + 1):
        dist[i][0] = (i,0,0)
    for j in range(tlen + 1):
        dist[0][j] = (0,j,0)

    for i in range(slen):
        for j in range(tlen):
            cost = (0,0,0) if equals(source[i],target[j]) else (0,0,1)
            dist[i + 1][j + 1] = min(
                add(dist[i][j + 1], (1,0,0)),  # deletion
                add(dist[i + 1][j], (0,1,0)),  # insertion
                add(dist[i][j], cost)  # substitution
                , key=lambda x: total(x)
            )

    return dist[-1][-1]


def total(tup):
    (a,b,c) = tup
    return a + b + c


def add(tup,tup2):
    (a,b,c) = tup
    (x,y,z) = tup2
    return (a+x,b+y,c+z)


def equals(source, target):
    if source == target:
        return True
    if Constants.PARAPHRASE:
        return is_paraphrase(source,target) or \
               is_substring(source,target) or \
               is_similar(source,target)
    else:
        return False


def is_paraphrase(source, target):
    paraphrases = Paraphrase.Ppdb.get_ppdb()
    similar = paraphrases.get(source, [])
    return target in similar


def is_substring(source: str,target: str):
    return target in source or source in target


def is_similar(source,target):
    return Constants.similarity.similarity(source,target)


def init_similarity():
    if Constants.PARAPHRASE and Constants.similarity is None:
        Constants.similarity = Similarity()
