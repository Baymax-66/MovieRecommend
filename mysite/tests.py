from django.test import TestCase

# Create your tests here.
import csv


moviedict = {
        "Action": "1",
        "Adventure": "2",
        "Animation": "3",
        "Children's": "4",
        "Comedy": "5",
        "Crime": "6",
        "Documentary": "7",
        "Drama": "8",
        "Fantasy": "9",
        "Film-Noir": "10",
        "Horror": "11",
        "Musical": "12",
        "Mystery ": "13",
        "Romance ": "14",
        "Sci-Fi ": "15",
        "Thriller": "16",
        "War ": "17",
        "Western": "18"
}


movietype = []
# with open("mysite_movietype.csv") as cf:
#         lines=csv.reader(cf)
#         for line in lines:
#                 line = line[0].split('|')
#                 movietype.append(line)

with open("mysite_moive.csv", "w", newline="") as cf:
        writer = csv.writer(cf)
        i = 0
        for line in movietype:
             i = i + 1
             for x in line:
                     writer.writerow([i, x])