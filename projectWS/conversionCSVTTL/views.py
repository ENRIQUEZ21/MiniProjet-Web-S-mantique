import csv
import re

# Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import ConversionForm



def index(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ConversionForm(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # CSVfile = Document(docfile=request.FILES['CSVfile'])
            CSVfile = form.clean_CSVfile()
            delimitation = form.clean_delimitation()
            if_title = form.clean_if_title()
            title_row = form.clean_title_row()
            start_row = form.clean_start_row()
            end_row = form.clean_end_row()

            decoded_file = CSVfile.read().decode('utf-8').splitlines()
            reader = csv.reader(decoded_file, delimiter=delimitation)


            outfile_ttl = open('exitTTLFile.ttl', 'a', encoding="utf8")

            outfile_ttl.write("@prefix d: <http://ex.org/data/> .\n")
            outfile_ttl.write("@prefix p: <http://ex.org/pred#> .\n\n")


            rownum = 0
            c = []  # c will be used to represent the row of title if it exists
            for row in reader:
                if rownum < start_row:
                    if if_title:
                        if rownum == title_row:
                            c = row
                            # We delete all undedirable elements in title row from our CSV file
                            for i in range(len(c)):
                                c[i] = ''.join(filter(str.isalnum, c[i]))
                        else:
                            pass
                    else:
                        pass
                elif start_row <= rownum <= end_row:
                    size = len(row)
                    l = []  # l is an array that we will use to produce our final string of characters of TTL code
                    l.append("d:L" + str(rownum - start_row))
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
            # CSVfile.close()


            form.save()
            # request.session['outfile_ttl'] = outfile_ttl
            return HttpResponseRedirect('result/')
        # if a GET (or any other method) we'll create a blank form
    else:
        form = ConversionForm
    return render(request, 'index.html', {'form': form})


def result(request):
    # outfile_ttl = request.session.get('outfile_ttl')
    return render(request, 'result.html')
