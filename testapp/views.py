from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import HttpResponseNotFound
from django.http import HttpResponseServerError
from django.http import HttpResponsePermanentRedirect

# You would have to do this in your application
from file_repository.models import Inode
from file_repository.forms import DirectoryForm, FileForm, DeleteInode
from file_repository.commands import get_inode

import magic

def index(request):
    context = {}
    return render(request, 'testapp/index.html', context)

def repository(request, filedir):
    directoryform = DirectoryForm
    fileform = FileForm

    try:
        i = get_inode(filedir, 'testapp')
    except Inode.Error404:
        return HttpResponseNotFound('<h1>File or directory not found</h1>')
    except Inode.Error500:
        return HttpResponseServerError('<h1>Internal server error</h1>')
    except Inode.Redirect302 as e:
        return HttpResponsePermanentRedirect('/repository/' + e.newpath)

    if request.method == 'POST':
        deleteinode = DeleteInode(request.POST)

        if deleteinode.is_valid():
            print("This is valid")
            print(deleteinode.cleaned_data['inodeid'])
            deletenode = Inode.objects.get(id=deleteinode.cleaned_data['inodeid'])
            deletenode.deletenode()
        else:
            directoryform = DirectoryForm(request.POST)
            fileform = FileForm(request.POST, request.FILES)
            if directoryform.is_valid():
                i.create_directory(directoryform.cleaned_data['name'])
            elif fileform.is_valid():
                i.create_file(fileform.cleaned_data['content'].name,
                              fileform.cleaned_data['content'])

    if i.is_directory==False:
        file_content = i.content.read()
        content_type = magic.from_buffer(file_content, mime=True).decode()
        response = HttpResponse(content_type=content_type)
        response.write(file_content)
        return response
    elif i.is_directory==True:
        context = {'directorynode':     i,
                   'directoryform':     directoryform,
                   'fileform':          fileform,    
                   'filedir':           filedir,
                  }

        return render(request, 'testapp/repository.html', context)
