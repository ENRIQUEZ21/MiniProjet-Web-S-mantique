# Authors: Aurélien NICOLLE - Ilan SOUSSAN - Antoine DARRAS - Gabriel ENRIQUEZ
# Date: 26/10/2021
import csv

from django import forms
from django.core.exceptions import ValidationError

from .models import Document


class ConversionForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['CSVfile', 'delimitation', 'if_title', 'title_row', 'start_row', 'end_row']

    def clean_CSVfile(self):
        data = self.cleaned_data['CSVfile']
        return data

    def clean_delimitation(self):
        data = self.cleaned_data['delimitation']
        return data

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

    def clean(self):
        cleaned_data = super().clean()
        CSVfile = cleaned_data.get("CSVfile")
        delimitation = cleaned_data.get("delimitation")
        if_title = cleaned_data.get("if_title")
        title_row = cleaned_data.get("title_row")
        start_row = cleaned_data.get("start_row")
        end_row = cleaned_data.get("end_row")
        # If there is a title in our CSV file
        if if_title:
            # If the the index of the row of title is specified
            if title_row is not None:
                # If the index of the title is negative, error
                if title_row < 0:
                    raise ValidationError("Oops!!! There is a problem, the index of your title row must be greater or "
                                          "equal to 0.")
                    # If the index of start is less than the index of title, error
                if title_row >= start_row:
                    raise ValidationError("Oops!!! There is a problem, the index of your start row must be greater "
                                          "than the index "
                                          "of your title row.")
            # Else, if it is not specified
            else:
                # If the index of start is negative or equal to 0, error, no 0 because there is a title
                if start_row <= 0:
                    raise ValidationError("Oops!!! There is a problem, the index of the start row must be "
                                          "greater than 0 ")
        # Else, if there is no title in the CSV file
        else:
            if start_row < 0:
                raise ValidationError(
                    "Oops!!! There is a problem, the index of the first row analyzed must be greater or equal to 0.")
        # If the index of end is less than the index of start, error
        if start_row >= end_row:
            raise ValidationError(
                "Oops!!! There is a problem, the index of your end row must be greater than the index "
                "of your start row.")

        num = 0
        if delimitation is None:
            delimitation = ','
        file = CSVfile.read().decode('utf-8').splitlines()
        read = csv.reader(file, delimiter=delimitation)
        size = 0
        for row in read:
            if if_title:
                if title_row is None:
                    if num == 0:
                        if len(row) == 0:
                            raise ValidationError("Oops!!! the title row index 0 (by default) is empty, please "
                                                  "choose one valid")
                        else:
                            size = len(row)
                else:
                    if num == title_row:
                        if len(row) == 0:
                            raise ValidationError("Oops!!! your title row is empty, please choose one other")
                        else:
                            size = len(row)
            else:
                if num == start_row:
                    size = len(row)
            if start_row <= num <= end_row:
                if len(row) == 0:
                    raise ValidationError("Oops!!! the row number "+ str(num)+" is an invalid empty row")
                if len(row) != size:
                    raise ValidationError("Oops!!! the row number "+str(num)+" is an invalid row which doesn't contain "
                                                                             "the good number of elements")
            num += 1



