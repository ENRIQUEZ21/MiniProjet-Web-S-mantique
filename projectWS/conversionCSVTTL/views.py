# Authors: Aurélien NICOLLE - Ilan SOUSSAN - Antoine DARRAS - Gabriel ENRIQUEZ
# Date: 28/10/2021
import csv
import os
import re


from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from .forms import DocumentForm, InformationForm
from django.conf import settings


def document(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = DocumentForm(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            CSVfile = form.clean_CSVfile() # CSV File from the user's computer
            delimitation = form.clean_delimitation() # delimitation to read CSV file

            pathToCSV = settings.MEDIA_ROOT + '/CSVfiles/' + str(CSVfile) # path in which the CSV file will be put in our project
            if os.path.exists(pathToCSV): # if it exists already a CSV file with the same name, we remove it
                os.remove(pathToCSV)
            else:
                pass

            form.save() # save objects provided by the form

            csvName = str(CSVfile).replace('.csv', '') # csvName is the name of the csv file (without its extension)

            request.session['csv_name'] = csvName

            request.session['delimiter'] = delimitation

            CSVfile.close() # we close the CSV file
            # Redirection to next step
            return HttpResponseRedirect('informations/')
    # if a GET (or any other method) we'll create a blank form
    else:
        form = DocumentForm
    return render(request, 'document.html', {'form': form})


def informations(request):
    if request.method == 'POST':
        form = InformationForm(request.POST)
        # If the form is valid
        if form.is_valid():
            # process the data in form.cleaned_data as required
            if_title = form.clean_if_title()
            title_row = form.clean_title_row()
            start_row = form.clean_start_row()
            end_row = form.clean_end_row()
            prefix_obj = form.clean_prefix_obj()
            prefix_pred = form.clean_prefix_pred()
            file_name = form.clean_file_name()

            CSVFile = open(request.session.get('path_to_csv'), 'r', encoding='utf-8') # We re-open our CSV file using the session created in the last step
            reader = csv.reader(CSVFile, delimiter=request.session.get('delimiter')) # variable to read through the CSV file

            if os.path.exists(file_name + '.ttl'): # I there is already a TTL file named as the name passed in argument,
                os.remove(file_name + '.ttl') # we remove it and we will replace it by the new with the same name
            else:
                pass

            outfile_ttl = open(file_name + '.ttl', 'a', encoding='utf-8') # We open a new TTL file with 'a' option so that if it doesn't exist, it will create it

            outfile_ttl.write("@prefix " + prefix_obj + ": <http://ex.org/data/> .\n")  # write object prefix
            outfile_ttl.write("@prefix " + prefix_pred + ": <http://ex.org/pred#> .\n\n")  # write predicate prefix

            rownum = 0 # We define rownum = 0, because we are at the beginning of our CSV file
            c = [] # We create a c array in which we will put the variables of the title line
            for row in reader: # We go through the row of the CSV file
                if rownum < start_row: # If the row readed is before the start row specified
                    if if_title: # If there is a title in the CSV file
                        if rownum == title_row: # We search the title row
                            c = row
                            for i in range(len(c)): # We affect all title row variables to our c array
                                c[i] = ''.join(filter(str.isalnum, c[i]))
                        else:
                            pass
                    else:
                        pass
                elif start_row <= rownum < end_row: # If we read row from start to end row
                    size = len(row) # We define the size which is the number of elements in the row
                    l = [prefix_obj + ":L" + str(
                        rownum - start_row)]  # l is an array that we will use to produce our final string of
                    # characters of TTL code
                    for i in range(size): # For each element of our row
                        # If the element has only letters numbers and _, then we can put it in our TTL file without "
                        if re.match("^[a-zA-Z0-9_]*$", row[i]):
                            if if_title: # If there is a title row,
                                l.append(" " + prefix_pred + ":P" + c[i] + " " + prefix_obj + ":" + row[i]) # we define predicate by using elements of the title row
                            else: # Else
                                l.append(" " + prefix_pred + ":P" + str(i) + " " + prefix_obj + ":" + row[i]) # we define predicate by using the index in our row
                        # Else, we have to put " around to produce correct TTL file
                        else:
                            if if_title: # If there is a title row,
                                l.append(" " + prefix_pred + ":P" + c[i] + " \"" + row[i] + "\"") # we define predicate by using elements of the title row
                            else: # Else
                                l.append(" " + prefix_pred + ":P" + str(i) + " \"" + row[i] + "\"") # we define predicate by using the index in our row
                        if i == (size - 1): # If it is the end of the row
                            l.append(".\n") # it is the end of the TTL sentence, so we pass to the newt line after a point
                        else: # Else
                            l.append(";\n\t") # We pass to an other predicate in the same sentence, so we add a ;
                    d = ''.join(l) # At the end of the row, we join all the l values in d variable
                    outfile_ttl.write(d) # We write this d str in our TTL file
                rownum += 1 # At the end of each row, we add 1 to our rownum to pass to next row

            request.session['ttl_file_name'] = file_name # We put in session the name of the TTL file
            outfile_ttl.close() # We close the TTL file produced
            CSVFile.seek(0) # We go to the beginning of the CSV file to re-read it in the future
            CSVFile.close() # We close our CSV file
            form.save() # We save objects provided by the form

            # We go to the result path
            return HttpResponseRedirect('result/')

    else:
        delim = request.session.get('delimiter') # We get the delimiter provided using session
        csvFile = request.session.get('csv_name') # We get the name of the CSV file using session
        path = settings.MEDIA_ROOT + '/CSVfiles/' + csvFile + '.csv' # path is the name of the path in which the loaded csv file is located
        file = open(path, 'r', encoding='utf8') # We re-open this file
        reader = csv.reader(file, delimiter=delim) # We use a csv.reader variable to read through the CSV file

        # We will define the indices of title row, start row, etc ...
        title_row = 0
        start_row = 1
        rownum = 0 # rownum variable represents the indice of the row readed
        for row in reader: # We iterate over the lines of the CSV file
            if len(row) != 0: # If the line has a length of 0
                title_row = rownum # So it is the first not empty line in the CSV file, so by default it is the title row
                start_row = rownum + 1 # And the next row is, by default, the start row
                continue # If we have found a title and a start row, we pass to another thing
            rownum += 1 # After each iteration, we add 1 to rownum
        file.seek(0) # We put the cursor at the beginning of the CSV file, so we can read it again
        rownum = 0# We re-put 0 to rownum because we are at the beginning pof the file
        for row in reader:
            rownum += 1
        end_row = rownum # After reading all the lines, we arrive at end row

        file.seek(0) # We put the cursor at the beginning of the CSV file to re-read it in the future
        file.close() # we close the file

        request.session['path_to_csv'] = path # We put in session the entire path to CSV file loaded



        # We define by default some values in the InformationForm
        form = InformationForm(
            initial={'title_row': title_row, 'start_row': start_row, 'end_row': end_row,
                                         'file_name': csvFile, 'path_to_csv': path, 'delimiter': delim})

    return render(request, 'informations.html', {'form': form})


def result(request):
    # We return the result.html file
    return render(request, 'result.html')


def download_TTL(request):
    filename = str(request.session.get('ttl_file_name')) + '.ttl' # filename is the name of the TTL file with .ttl extension
    fl_path = settings.BASE_DIR / filename # fl_path is the path of he TTL file in our project

    fl = open(fl_path, 'r', encoding="utf8") # We open the TTL file and put it in fl variable
    response = HttpResponse(fl, content_type='application/x-turtle') # We put in response the TTL file with x-turtle type
    response['Content-Disposition'] = "attachment; filename=%s" % filename # We put the same name as in our project to the response TTL file
    fl.close() # We close the TTL file
    # And then, we return the TTL file to the user
    return response


def download_CSV(request):
    filename = request.session.get('csv_name') + '.csv' # filename is the name of our CSV file with .csv extension
    path = request.session.get('path_to_csv') # path is the path of the CSV file in our project

    file = open(path, 'r', encoding='utf8')# We open the CSV file and put it in file variable
    response = HttpResponse(file, content_type='application/csv')# We put in response the CSV file
    response['Content-Disposition'] = "attachment; filename=%s" % filename# We put the same name as in our project to the response CSV file
    file.close()# Close the CSV file
    # Return CSV file to the user
    return response
