from django import forms

from .validators import validate_file_extension


class ConversionForm(forms.Form):
    class Meta:
        fields = ['CSVfile', 'if_title', 'title_row', 'start_row', 'end_row']
    CSVfile = forms.FileField(validators=[validate_file_extension], required=False)
    if_title = forms.BooleanField(label='There is a title row in your CSV')
    title_row = forms.IntegerField(label='Index of title row')
    start_row = forms.IntegerField(label='Index of start row')
    end_row = forms.IntegerField(label='Index of end row')


    def clean_CSVfile(self):
        data = self.cleaned_data['CSVfile']
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
        title_row = cleaned_data.get("title_row")
        start_row = cleaned_data.get("start_row")
        end_row = cleaned_data.get("end_row")
        # All the indexes must be positive
        if title_row < 0:
            raise ValueError("Oops!!! There is a problem, the index of your title row must be greater or equal to 0.")
        # If the index of start is less than the index of title, error
        if title_row >= start_row:
            raise ValueError("Oops!!! There is a problem, the index of your start row must be greater than the index"
                             "of your title row.")
        # If the index of end is less than the index of start, error
        if start_row >= end_row:
            raise ValueError("Oops!!! There is a problem, the index of your end row must be greater than the index"
                             "of your start row.")



