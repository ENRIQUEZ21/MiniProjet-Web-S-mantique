# Date: from 22/10/2021 to ...
# Authors: Gabriel ENRIQUEZ - Ilan SOUSSAN - Antoine DARRAS - Aurélien NICOLLE

# Importation du module CSV
import csv


tryFile = open('test1.csv', encoding="utf8") # Ouverture du fichier test1.csv et assignation de celui-ci à la variable tryFile
reader = csv.reader(tryFile, delimiter=";") # Cette variable va nous permettre de manipuler les données du fichier test1.csv

# we create a new TTL file using the 'a' option in open function
outfile_ttl = open('exitTTLFile.ttl', 'a', encoding="utf8")

outfile_ttl.write("@prefix d: <http://ex.org/data/> .\n")
outfile_ttl.write("@prefix p: <http://ex.org/pred#> .\n\n")

rownum = 0
for row in reader:
    if (rownum == 0 or rownum == 1 or rownum == 2):
        pass
    else:
        c = row
        d = "d: p:est " + "d:"+c[0]  +", d:"+ c[1] +", d:"+  c[2] +", d:"+  c[3] +", d:"+  c[4]+".\n"
        outfile_ttl.write(d)
    rownum+=1

outfile_ttl.close()
tryFile.close()
