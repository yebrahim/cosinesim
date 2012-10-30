#!/usr/bin/env python
# encoding: utf-8

"""
File: cosinesim.py
Author: Yasser Ebrahim
Date: Oct 2012

Calculate consine similarity between given users, represented as two vectors of liked items
Items are documents which should be given to the script, contained in a directory, and labeled by
    the IDs similar to the ones in the user vectors

"""

import sys, re, math, csv
from optparse import OptionParser

# globals
user_documents  = {}
user_features   = {}
doc_pattern     = '.txt'
user_vectors    = ''
doc_directory   = './'
out_file        = 'cosinesim.out'

def scalar(arr):
    total = 0
    for (term,relev) in arr.items():
        total += relev * relev
    return math.sqrt(total)

# this function takes two feature vectors, which are dictionaries,
# mapping a term to its relevance, and representing two users,
# and computes the cosine similarity between them
def cosine_similarity(A,B):
    total = 0
    for term in A:
        if term in B:
            total += float(A[term]) * float(B[term])
    a = scalar(A)
    b = scalar(B)
    if a == 0 or b == 0:
        return 0
    return float(total) / (a * b)

# this function takes a user ID, opens his corresponding files,
# and builds a concatenated feature vector out of his liked items
def build_features(u):
    docs = user_documents[u]
    user_features[u] = {}
    for d in docs:
        d = d.strip()
        path = doc_directory + str(d) + doc_pattern
        try:
            f = open(path, 'r')
            #print('parsing file: ' + path)
            for line in f.xreadlines():
                c1, c2 = line.split()
                if c1 in user_features[u]:
                    user_features[u][c1] += float(c2)
                else:
                    user_features[u][c1]  = float(c2)
        except:
            pass

# __main__ execution

parser = OptionParser(usage='usage: %prog [options] user_vectors doc_directory')
parser.add_option('-u', '--user', dest='user1',
        help='user to compute all similarities against')
parser.add_option('-v', '--user2', dest='user2',
        help='**can only be used with -u\nuser v to compute similarity against u')
parser.add_option('-o', '--output', dest='output',
        help='output file name. default is consinesim.out')
parser.add_option('-s', '--suffix', dest='suffix',
        help='document suffixes. this is sometimes desirable to change. default is .txt')

(options, args) = parser.parse_args()

if len(args) < 2:
    print(parser.print_help())
    quit()

user_vectors = args[0]
doc_directory = args[1]
if doc_directory[-1] != '/':
    doc_directory += '/'
user1 = options.user1
user2 = options.user2
if options.output:
    out_file = options.output
if options.suffix:
    doc_pattern = options.suffix

# load user vectors
f = open(user_vectors, 'r')
for line in f:
    (u, vec) = line.split(': ')
    vec = vec.split(', ')
    user_documents[u] = vec

# pre-compute all user features
print('building user features..')
for u in user_documents:
    build_features(u)
    print('generated features for ' + str(u) + ': ' + str(user_features[u]))

f = open(out_file, 'w')

ranked_result = []

# compute similarity between user1 and all other users
if user1 and not user2:
    U = user_features[user1]
    for v in user_features:
        if v != user1:
            V = user_features[v]
            ranked_result.append((cosine_similarity(U,V), str(user1) + ', ' + str(v)))
elif user1 and user2:
    U = user_features[user1]
    V = user_features[user2]
    ranked_result.append((cosine_similarity(U,V), str(user1) + ', ' + str(user2)))
elif not user1 and not user2:
    print('computing similarity between all users..')
    for u in user_features:
        for v in user_features:
            # don't repeat computation
            if int(u) < int(v):
                U = user_features[u]
                V = user_features[v]
                ranked_result.append((cosine_similarity(U,V), str(u) + ', ' + str(v)))
else:
    parser.print_help()

ranked_result = sorted(ranked_result, reverse=True)
for res,key in ranked_result:
    f.write(key + ': ' + str(res) + '\n')

print('done.')

