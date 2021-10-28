# Authors: Aurélien NICOLLE - Ilan SOUSSAN - Antoine DARRAS - Gabriel ENRIQUEZ
# Date: 26/10/2021
import csv
import os
import re

# Create your views here.

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
            CSVfile = form.clean_CSVfile()
            delimitation = form.clean_delimitation()

            pathToCSV = settings.MEDIA_ROOT + '/CSVfiles/' + str(CSVfile)
            if os.path.exists(pathToCSV):
                os.remove(pathToCSV)
            else:
                pass

            form.save()

            csvName = str(CSVfile).replace('.csv', '')

            request.session['csv_name'] = csvName

            request.session['delimiter'] = delimitation

            CSVfile.close()
            return HttpResponseRedirect('informations/')
        # if a GET (or any other method) we'll create a blank form
    else:
        form = DocumentForm
    return render(request, 'document.html', {'form': form})


def informations(request):
    if request.method == 'POST':
        form = InformationForm(request.POST)
        if form.is_valid():
            if_title = form.clean_if_title()
            title_row = form.clean_title_row()
            start_row = form.clean_start_row()
            end_row = form.clean_end_row()
            prefix_obj = form.clean_prefix_obj()
            prefix_pred = form.clean_prefix_pred()
            file_name = form.clean_file_name()

            CSVFile = open(request.session.get('path_to_csv'), 'r', encoding='utf-8')
            reader = csv.reader(CSVFile, delimiter=request.session.get('delimiter'))

            if os.path.exists(file_name + '.ttl'):
                os.remove(file_name + '.ttl')
            else:
                pass

            outfile_ttl = open(file_name + '.ttl', 'a', encoding='utf-8')

            outfile_ttl.write("@prefix " + prefix_obj + ": <http://ex.org/data/> .\n")  # write object prefix
            outfile_ttl.write("@prefix " + prefix_pred + ": <http://ex.org/pred#> .\n\n")  # write predicate prefix

            rownum = 0
            c = []
            for row in reader:
                if rownum < start_row:
                    if if_title:
                        if rownum == title_row:
                            c = row
                            for i in range(len(c)):
                                c[i] = ''.join(filter(str.isalnum, c[i]))
                        else:
                            pass
                    else:
                        pass
                elif start_row <= rownum < end_row:
                    size = len(row)
                    l = [prefix_obj + ":L" + str(
                        rownum - start_row)]  # l is an array that we will use to produce our final string of
                    # characters of TTL code
                    for i in range(size):
                        if re.match("^[a-zA-Z0-9_]*$", row[i]):
                            if if_title:
                                l.append(" " + prefix_pred + ":P" + c[i] + " " + prefix_obj + ":" + row[i])
                            else:
                                l.append(" " + prefix_pred + ":P" + str(i) + " " + prefix_obj + ":" + row[i])
                        else:
                            if if_title:
                                l.append(" " + prefix_pred + ":P" + c[i] + " \"" + row[i] + "\"")
                            else:
                                l.append(" " + prefix_pred + ":P" + str(i) + " \"" + row[i] + "\"")
                        if i == (size - 1):
                            l.append(".\n")
                        else:
                            l.append(";\n\t")
                    d = ''.join(l)
                    outfile_ttl.write(d)
                rownum += 1

            request.session['ttl_file_name'] = file_name
            outfile_ttl.close()
            CSVFile.seek(0)
            CSVFile.close()
            form.save()

            return HttpResponseRedirect('result/')

    else:
        delim = request.session.get('delimiter')
        csvFile = request.session.get('csv_name')
        path = settings.MEDIA_ROOT + '/CSVfiles/' + csvFile + '.csv'
        file = open(path, 'r', encoding='utf8')
        reader = csv.reader(file, delimiter=delim)

        # We will define the indices of title row, start row, etc ...
        title_row = 0
        start_row = 1
        end_row = 10
        rownum = 0
        for row in reader:
            if len(row) != 0:
                title_row = rownum
                start_row = rownum + 1
                continue
            rownum += 1
        file.seek(0)
        rownum = 0
        for row in reader:
            rownum += 1
        end_row = rownum

        file.seek(0)
        file.close()

        request.session['path_to_csv'] = path
        request.session['delimiter'] = delim



        form = InformationForm(
            initial={'title_row': title_row, 'start_row': start_row, 'end_row': end_row,
                                         'file_name': csvFile, 'path_to_csv': path, 'delimiter': delim})

    return render(request, 'informations.html', {'form': form})


def result(request):
    return render(request, 'result.html')


def download_TTL(request):
    filename = str(request.session.get('ttl_file_name')) + '.ttl'
    fl_path = settings.BASE_DIR / filename

    fl = open(fl_path, 'r', encoding="utf8")
    response = HttpResponse(fl, content_type='application/x-turtle')
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    fl.close()
    return response


def download_CSV(request):
    path = request.session.get('path_to_csv')
    filename = request.session.get('csv_name') + '.csv'

    file = open(path, 'r', encoding='utf8')
    response = HttpResponse(file, content_type='application/csv')
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    file.close()
    return response
