# -*- coding: utf-8 -*-

from def_features import *

# Previous word and current tag pair
preWordFeature = UniSurrFeature([-1])
# Next word and current tag pair
nextWordFeature = UniSurrFeature([1])

# pre pre word and current tag pair
prepreWordFeature = UniSurrFeature([-2])
# next next word and current tag pair
nextnextWordFeature = UniSurrFeature([2])

# pre pre pre word and current tag pair
preprepreWordFeature = UniSurrFeature([-3])
# next next next word and current tag pair
nextnextnextWordFeature = UniSurrFeature([3])

# [-1, 0] and current tag pair
precuWordFeature = UniSurrFeature([-1, 0])
# [0, 1] and current tag pair
cunextWordFeature = UniSurrFeature([0, 1])

# [-2, -1, 0] and current tag pair
preprecuWordFeature = UniSurrFeature([-2, -1, 0])
# [-1, 0, 1] and current tag pair
precunextWordFeature = UniSurrFeature([-1, 0, 1])
# [0, 1, 2] and current tag pair
cunextnextWordFeature = UniSurrFeature([0, 1, 2])

# Previous word and bigram tags
preWordBiFeature = BiSurrFeature([-1])
# Next word and bigram tags
nextWordBiFeature = BiSurrFeature([1])

# number feature
hasNumberFeature = ContainsFeature('0123456789$', 'NUM')
# special symbols
hasSpecialSymbolFeatures = \
    [ContainsFeature(*arg) for arg in [('.',), ('-',), ('&^%@#^!?[](){}*+/=', 'OTHER')]] + [hasNumberFeature]

#========= Feature template combination samples ==========
SUFFIX = lambda len1, len2, case=False : [SuffixFeature(leng, case) for leng in range(len1, len2 + 1)]
PREFIX = lambda len1, len2, case=False : [PrefixFeature(leng, case) for leng in range(len1, len2 + 1)]

#features = [TagFeature(False), preWordFeature, nextWordFeature, prepreWordFeature, nextnextWordFeature, \
#    precuWordFeature, cunextWordFeature, preprecuWordFeature, precunextWordFeature, cunextnextWordFeature]

features = [TagFeature(False), preWordFeature, nextWordFeature] + SUFFIX(1, 1) + PREFIX(1, 1)
