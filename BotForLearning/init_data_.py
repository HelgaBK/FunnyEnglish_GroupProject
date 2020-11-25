import csv
global words
global w
global anything
global count_
words__ = []
words = []

with open( 'words.csv', newline='' ) as File:
    reader = csv.reader( File )
    for row in reader:
        words__.append(row[0].split(";"))

for y in words__:
    words.append(y)

anything = []
word = []
words_taken = []
count_ = [0]
pass_ = [0]