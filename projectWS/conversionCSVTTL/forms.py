# Authors: Aurélien NICOLLE - Ilan SOUSSAN - Antoine DARRAS - Gabriel ENRIQUEZ
# Date: 26/10/2021
import csv
import os
import re

from django import forms
from django.core.exceptions import ValidationError

from .models import Document, Information


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
        filename = str(os.path.basename(CSVfile.name)).replace('.csv', '')

        if not re.match("^[a-zA-Z0-9_]*$", filename):
            raise ValidationError("Oops!!! The name of your file is invalid, please choose "
                                  "a file which contains only letters, numbers and _")


class InformationForm(forms.ModelForm):
    class Meta:
        model = Information
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

        if if_title:
            if title_row is None:
                raise ValidationError("Oops!!! the field title row is empty, and there is a title in your "
                                      "CSV file.")
            else:
                if title_row < 0:
                    raise ValidationError("Oops!!! the value of the index of title row is negative, "
                                          "that is impossible, indices start at 0.")
                if start_row <= title_row:
                    raise ValidationError("Oops!!! your start row must be after your title row.")
        else:
            if start_row < 0:
                raise ValidationError("Oops!!! the value of the index of your start row is negative, "
                                      "that is impossible.")
        if start_row >= end_row:
            raise ValidationError("Oops!!! your end row must be after your start row")

        print(path_to_csv)
        CSVFile = open(path_to_csv, 'r', encoding='utf-8')
        reader = csv.reader(CSVFile, delimiter=delimiter)

        rownum = 0
        size = 0
        for row in reader:
            if if_title:
                if rownum == title_row:
                    if len(row) == 0:
                        raise ValidationError("Oops!!! your title row is empty, please choose one other")
                    else:
                        size = len(row)
            else:
                if rownum == start_row:
                    if len(row) == 0:
                        raise ValidationError("Oops!!! Your start row is empty.")
                    else:
                        size = len(row)
            if start_row <= rownum < end_row:
                if len(row) != size:
                    raise ValidationError("Oops!!! The row "+rownum+" has a wrong number of elements.")

            rownum+=1

        CSVFile.seek(0)
        CSVFile.close()