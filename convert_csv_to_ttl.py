# Date: from 22/10/2021 to ...
# Authors: Gabriel ENRIQUEZ - Ilan SOUSSAN - Antoine DARRAS - Aurélien NICOLLE

# Importation of CSV module
import csv


tryFile = open('test1.csv', encoding="utf8") # Opening of test1.csv file and assignment of it to tryFile variable
reader = csv.reader(tryFile, delimiter=";") # This variable will permit us to manipulate data of test1.csv file

# we create a new TTL file using the 'a' option in open function
outfile_ttl = open('exitTTLFile.ttl', 'a', encoding="utf8")

outfile_ttl.write("@prefix d: <http://ex.org/data/> .\n")
outfile_ttl.write("@prefix p: <http://ex.org/pred#> .\n\n")

# Parameter of the start line
row_start = 3

# Python will loop through each row in the csv file
rownum = 0
for row in reader:
    if (rownum < row_start):
        pass
    else: # place the contents of the row into the 'c' variable, then create a 'd' that we will write in our TTL file
        c = row
        d = "d: p:est " + "d:"+c[0]  +", d:"+ c[1] +", d:"+  c[2] +", d:"+  c[3] +", d:"+  c[4]+".\n"
        outfile_ttl.write(d)
    rownum+=1 # add 1 to rownum to pass to following line

outfile_ttl.close()
tryFile.close()
