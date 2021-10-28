# Authors: Aurélien NICOLLE - Ilan SOUSSAN - Antoine DARRAS - Gabriel ENRIQUEZ
# Date: 28/10/2021
import csv
import os
import re

from django import forms
from django.core.exceptions import ValidationError

from .models import Document, Information


# First form, submission of the CSV file
class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['CSVfile', 'delimitation']

    def clean_CSVfile(self):
        data = self.cleaned_data['CSVfile']
        return data

    def clean_delimitation(self):
        data = self.cleaned_data['delimitation']
        return data

    def clean(self):
        cleaned_data = super().clean()
        CSVfile = cleaned_data.get("CSVfile")
        delimitation = cleaned_data.get("delimitation")
        filename = str(os.path.basename(CSVfile.name)).replace('.csv',
                                                               '')  # filename is the name of the CSV file without .csv extension

        # If the name of the CSV file contains other elements than letters numbers and _,
        # the file will be downloaded in our project under another name and we will no longer be able to find it
        if not re.match("^[a-zA-Z0-9_]*$", filename):
            raise ValidationError("Oops!!! The name of your file is invalid, please choose "
                                  "a file which contains only letters, numbers and _")


# Second form, submission of the informations
class InformationForm(forms.ModelForm):
    class Meta:
        model = Information
        # We put path_to_csv and delimiter inputs hidden because we will just use these variables for our validation without changing these
        widgets = {'path_to_csv': forms.HiddenInput(), 'delimiter': forms.HiddenInput()}
        fields = ['if_title', 'title_row', 'start_row', 'end_row', 'prefix_obj', 'prefix_pred', 'file_name',
                  'path_to_csv', 'delimiter']

    def clean_if_title(self):
        data = self.cleaned_data['if_title']
        return data

    def clean_title_row(self):
        data = self.cleaned_data['title_row']
        return data

    def clean_start_row(self):
        data = self.cleaned_data['start_row']
        return data

    def clean_end_row(self):
        data = self.cleaned_data['end_row']
        return data

    def clean_prefix_obj(self):
        data = self.cleaned_data['prefix_obj']
        return data

    def clean_prefix_pred(self):
        data = self.cleaned_data['prefix_pred']
        return data

    def clean_file_name(self):
        data = self.cleaned_data['file_name']
        return data

    def clean_path_to_csv(self):
        data = self.cleaned_data['path_to_csv']
        return data

    def clean_delimiter(self):
        data = self.cleaned_data['delimiter']
        return data

    def clean(self):
        cleaned_data = super().clean()
        if_title = cleaned_data.get("if_title")
        title_row = cleaned_data.get("title_row")
        start_row = cleaned_data.get("start_row")
        end_row = cleaned_data.get("end_row")
        path_to_csv = cleaned_data.get("path_to_csv")
        delimiter = cleaned_data.get("delimiter")

        if if_title:  # If there is a title in our CSV file (if_title field checked)
            if title_row is None:  # If title_row input is not filled, we raise a ValidationError
                raise ValidationError("Oops!!! the field title row is empty, and there is a title in your "
                                      "CSV file.")
            else:
                if title_row < 0:  # The row of title must be positive, otherwise we raise a ValidationError
                    raise ValidationError("Oops!!! the value of the index of title row is negative, "
                                          "that is impossible, indices start at 0.")
                if start_row <= title_row:  # The start row mst be after title row, otherwise we raise a ValidationError
                    raise ValidationError("Oops!!! your start row must be after your title row.")
        else:  # Else, if there is no title in our CSV file
            if start_row < 0:  # The start row must be positive, otherwise, we raise a ValidationError
                raise ValidationError("Oops!!! the value of the index of your start row is negative, "
                                      "that is impossible.")
        if start_row >= end_row:  # The end row must be after the start row
            raise ValidationError("Oops!!! your end row must be after your start row")

        CSVFile = open(path_to_csv, 'r', encoding='utf-8')  # CSVFile is the CSV file loaded in our project
        reader = csv.reader(CSVFile, delimiter=delimiter)  # We define a reader to read all lines of this file

        rownum = 0  # rownum is 0 at the beginning, it represents the index of the row readed
        size = 0  # size will be the size of the rows
        for row in reader:  # We go through each line
            if if_title:  # If there is a title in our CSV file
                if rownum == title_row:  # If we are reading the title row
                    if len(row) == 0:  # If this row is empty, we raise a ValidationError
                        raise ValidationError("Oops!!! your title row is empty, please choose one other")
                    else:  # Else, we define size variable by the length of this row
                        size = len(row)
            else:  # If there is no title in our CSV file
                if rownum == start_row:  # If we are reading the start_row
                    if len(row) == 0:  # If this row is empty, we raise a ValidationError
                        raise ValidationError("Oops!!! Your start row is empty.")
                    else:  # Else, we define size variable by the length of this row
                        size = len(row)
            if start_row <= rownum < end_row:  # If we are reading a line of data in our CSV file
                if len(row) != size:  # If the length of the row is different of the size defined, there is an error
                    # because all rows must have the same number of elements
                    raise ValidationError("Oops!!! The row " + rownum + " has a wrong number of elements.")

            rownum += 1  # We add 1 to rownum at each row readed

        CSVFile.seek(0)  # We put the cursor at the beginning of the CSV file to re-read through it in the future
        CSVFile.close()  # We close the CSV file
