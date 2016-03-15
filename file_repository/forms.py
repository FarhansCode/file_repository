from django import forms

from file_repository.models import Inode

class DirectoryForm(forms.ModelForm):
	class Meta:
		model = Inode 
		fields = ['name']

class FileForm(forms.ModelForm):
	class Meta:
		model = Inode 
		fields = ['content']
