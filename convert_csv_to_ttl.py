# Date: from 22/10/2021 to ...
# Authors: Gabriel ENRIQUEZ - Ilan SOUSSAN - Antoine DARRAS - Aurélien NICOLLE

# Importation of csv module to use CSV file and re module to see if a word contains valid characters
import csv
import re


tryFile = open('test1.csv', encoding="utf8") # Opening of CSV file and assignment of it to tryFile variable
reader = csv.reader(tryFile, delimiter=";") # This variable will permit us to manipulate data of CSV file

# we create a new TTL file using the 'a' option in open function
outfile_ttl = open('exitTTLFile.ttl', 'a', encoding="utf8")

outfile_ttl.write("@prefix d: <http://ex.org/data/> .\n")
outfile_ttl.write("@prefix p: <http://ex.org/pred#> .\n\n")

# Parameter of the start and end line
row_start = 5
row_end = 10

# Boolean if there is title (true) or no (false)
if_title = False
# In case of title, we put into row_title the index of the row of title
row_title = 0

# Python will loop through each row in the csv file
rownum = 0
c=[] # c will be used to represent the row of title if it exists
for row in reader:
    if rownum < row_start:
        if if_title:
            if rownum == row_title:
                c = row
                # We delete all undedirable elements in title row from our CSV file
                for i in range(len(c)):
                    c[i] = ''.join(filter(str.isalnum, c[i]))
            else:
                pass
        else:
            pass
    elif row_start <= rownum <= row_end:
        size = len(row)
        l = []  # l is an array that we will use to produce our final string of characters of TTL code
        l.append("d:L" + str(rownum - row_start))
        for i in range(size):
            # In function of the different cases:
            # end of line, type of the value, there is or no a title in our CSV file,
            # we will add an appropriate TTL code to our l variable
            if re.match("^[a-zA-Z0-9_]*$", row[i]):
                if if_title:
                    l.append(" p:P" + c[i] + " d:" + row[i])
                else:
                    l.append(" p:P" + str(i) + " d:" + row[i])
            else:
                if if_title:
                    l.append(" p:P" + c[i] + " \"" + row[i] + "\"")
                else:
                    l.append(" p:P" + str(i) + " \"" + row[i] + "\"")
            if i == (size - 1):
                l.append(".\n")
            else:
                l.append(";\n\t")
        d = ''.join(l)
        outfile_ttl.write(d)
    rownum += 1  # add 1 to rownum to pass to following line


outfile_ttl.close()
tryFile.close()
