# -*- coding: utf-8 -*-

class Feature(object):
    case = True
    def __init__(self, name, case = None):
        self.name = name
        self.case = case

    @staticmethod
    def setAllCase(case):
        Feature.case = case

    def setCase(self, case):
        self.case = case
        return self

    def getCase(self):
        return Feature.case if self.case == None else self.case

    def _hash_str(self, *values):
        hashstr = self.name
        for val in values:
            hashstr += ':' + (str(val) if self.getCase() else str(val).lower())
        return hashstr

    def __call__(self, tag_seq, line, i):
        pass

    def __str__(self):
        return ('' if self.getCase() else '*') + self.name


class TagFeature(Feature):
    def __init__(self, case=None):
        Feature.__init__(self, 'TAG', case)

    def __call__(self, tag_seq, line, i):
        return self._hash_str(line[i], tag_seq[-1])


class BigramFeature(Feature):
    def __init__(self):
        Feature.__init__(self, 'BIGRAM', case=True)

    def __call__(self, tag_seq, line, i):
        return self._hash_str(*tag_seq[-2:])


class SuffixFeature(Feature):
    def __init__(self, suffixLen, case=None):
        Feature.__init__(self, 'SUFFIX', case)
        self.len = suffixLen


    def __call__(self, tag_seq, line, i):
        return self._hash_str(line[i][-self.len:], tag_seq[-1])


    def __str__(self):
        return Feature.__str__(self) + str(self.len)


class PrefixFeature(Feature):
    def __init__(self, prefixLen, case=None):
        Feature.__init__(self, 'PREFIX', case)
        self.len = prefixLen


    def __call__(self, tag_seq, line, i):
        return self._hash_str(line[i][:self.len], tag_seq[-1])


    def __str__(self):
        return Feature.__str__(self) + str(self.len)


class SurrFeature(Feature):
    def __init__(self, indices, ngram, case=None):
        Feature.__init__(self, 'SURR', case)
        self.ngram = ngram
        self.indices = indices


    def __call__(self, tag_seq, line, i):
        wordList = ['*' if i + shift < 0 \
                    else ('&' if i + shift >= len(line)\
                          else line[i + shift]) for shift in self.indices]
        return self._hash_str(*(self.indices + wordList + tag_seq[-self.ngram:]))


    def __str__(self):
        return Feature.__str__(self) + str(self.indices) + 'N' + str(self.ngram)


class UniSurrFeature(SurrFeature):
    def __init__(self, indices, case=None):
        SurrFeature.__init__(self, indices, 1, case)
    def __str__(self):
        return SurrFeature.__str__(self)[:-2] + 'Uni'


class BiSurrFeature(SurrFeature):
    def __init__(self, indices, case=None):
        SurrFeature.__init__(self, indices, 2, case)
    def __str__(self):
        return SurrFeature.__str__(self)[:-2] + 'Bi'


class ContainsFeature(Feature):
    def __init__(self, containList, containerName=None, dual=True, case=True):
        Feature.__init__(self, 'HAS', case)
        self.tokens = set(containList) if case else {token.lower() for token in containList}
        self.name += ':' + (containerName or '|'.join(containList))
        self.dual = dual


    def __call__(self, tag_seq, line, i):
        word = line[i] if self.case else line[i].lower()
        found = len(set(word) & self.tokens) > 0
        if self.dual: return self._hash_str(['n', 'y'][found], tag_seq[-1])
        else: return self._hash_str(tag_seq[-1]) if found else ''


class ContainsCapital(ContainsFeature):
    def __init__(self):
        ContainsFeature.__init__(self, [chr(c) for c in range(ord('A'), ord('Z')+1)], 'CAP', dual=False, case=True)


    def __call__(self, tag_seq, line, i):
        return ContainsFeature.__call__(self, tag_seq, line, i) if i > 0 else ''
