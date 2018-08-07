from django import forms

class UploadFileForm(forms.Form):
	upload_file=forms.FileField(
			widget=forms.ClearableFileInput(attrs={'multiple': True})
			,
			label='Select File',
			help_text = 'max. 10 megabytes')