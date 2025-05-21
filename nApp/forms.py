from django import forms

class CSVImportForm(forms.Form):
    csv_file = forms.FileField(
        label="Select CSV file",
        help_text="Headers must match your Application fields.  "
                  "For multi-value columns (e.g. tags), separate values with ',' inside a quoted cell."
    )