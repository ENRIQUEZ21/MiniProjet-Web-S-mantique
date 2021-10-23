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
    else:
        size = len(row)
        l=[] # l is an array that we will use to produce our final string of characters of TTL code
        l.append("d:L"+str(rownum-row_start))
        for i in range(size): # In function of the different cases: end of line, type of the value, we add an appropriate TTL code to our l variable
            # Depending of type of values
            if type(row[i].__class__) == float.__class__ or type(row[i].__class__) == int.__class__:
                l.append(" p:P" + str(i) + " \"" + row[i] + "\"")
            else:
                l.append(" p:P" + str(i) + " d:" + row[i])
            # Depending of if it is end of line or no
            if i == (size-1):
                l.append(".\n")
            else:
                l.append(";\n\t")

        d = ''.join(l)
        outfile_ttl.write(d)
    rownum+=1 # add 1 to rownum to pass to following line

outfile_ttl.close()
tryFile.close()
