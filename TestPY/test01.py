from django.test import TestCase

# Create your tests here.
import csv


movie_labels_index = set([])
with open("mysite_movielabel.csv",encoding='utf-8') as cf:
    lines = csv.reader(cf)
    for line in lines:
        print(line)
# with open("mysite_movietype.csv") as cf:
#         lines=csv.reader(cf)
#         for line in lines:
#                 line = line[0].split('|')
#                 movietype.append(line)
#
# with open("mysite_moive.csv", "w", newline="") as cf:
#     writer = csv.writer(cf)
#     i = 0
#     for line in movietype:
#         i = i + 1
#         for x in line:
#             writer.writerow([i, x])