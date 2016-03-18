from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import HttpResponseNotFound
from django.http import HttpResponseServerError

# You would have to do this in your application
from file_repository.models import Inode
from file_repository.forms import DirectoryForm, FileForm
from file_repository.views import get_inode
from file_repository.commands import del_inode, create_root, create_file, create_directory

import magic

def index(request):
   context = {}
   return render(request, 'testapp/index.html', context)

def repository(request, filedir):
   directoryform = DirectoryForm
   fileform = FileForm

   print(dir(request))

   retcode, current_directory, current_file, redirect_path = get_inode(filedir, 'testapp')
   if retcode == 200:
      print("Response 200")
      pass # Nothing to do here, the rest of the page will handle this
   elif retcode == 301:
      return HttpResponseRedirect('/repository/' + redirect_path)
   elif retcode == 404:
      return HttpResponseNotFound('<h1>Error 404: File or Directory Not Found</h1>')
   else:
      print("An error occured")
      return HttpResponseServerError('<h1>Error 500: Some kind of weirdo internal error</h1>')

   print("Return code: %d" % retcode)

   if request.method == 'POST':
      directoryform = DirectoryForm(request.POST)
      fileform = FileForm(request.POST, request.FILES)
      if directoryform.is_valid():
         try:
            current_directory.inodes.get( name = directoryform.cleaned_data['name'])
         except Inode.DoesNotExist:
            create_directory(current_directory, directoryform.cleaned_data['name'])
      elif fileform.is_valid():
         try:
            current_directory.inodes.get(name=fileform.cleaned_data['content'].name )
         except Inode.DoesNotExist:
            create_file(current_directory, fileform.cleaned_data['content'].name, fileform.cleaned_data['content'])
      else: #Invalid both, just continue
         pass
   else:
      if current_file: # Check if the file is being sent over
         file_content = current_file.content.read()
         content_type = magic.from_buffer(file_content, mime=True).decode()
         response = HttpResponse(content_type=content_type)
         response.write(file_content)
         return response

   # Reset the form
   directoryform = DirectoryForm()
   fileform = FileForm()

   context = {    'directoryform':       directoryform,
                  'fileform':            fileform,   
                  'current_directory':   current_directory,
            }

   return render(request, 'testapp/repository.html', context)
