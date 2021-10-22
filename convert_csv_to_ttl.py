# Date: from 22/10/2021 to ...
# Authors: Gabriel ENRIQUEZ - Ilan SOUSSAN - Antoine DARRAS - Aurélien NICOLLE

# Importation du module CSV
import csv


tryFile = open('test1.csv') # Ouverture du fichier test1.csv et assignation de celui-ci à la variable tryFile
reader = csv.reader(tryFile) # Cette variable va nous permettre de manipuler les données du fichier test1.csv

# we create a new TTL file using the 'a' option in open function
outfile_ttl = open('exitTTLFile.ttl', 'a')