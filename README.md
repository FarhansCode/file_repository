# File Repository Application

## Brief Description

This is my attempt at writing a file system repository system. It allows you to
view system files in a hierarchical manner, rather than all in a single
directory or folder.

## Why this code?

Models.FileField() only stores files in a single directory. You can specify a 
'upload_to' directory, but that still only creates a single repository directory
where all files are stored. This code adds an abstraction layer to help organize
files in a hierarchical manner.

## Initialization

I have not yet figured out how to add an initializer in a migration, so you will
have to create an initial root Inode.

```python
Inode(rootname='testapp', name='').save()
```

## How to use

1. Download and save the code into your project directory.
2. Insert the application in your INSTALLED_APPS list. [Example](https://github.com/FarhansCode/file_repository/blob/master/testapp/settings.py#L40)
3. Create the database migrations and perform the migration.
4. Create the initial root Inode element.
```python
Inode(rootname='testapp', name='').save()
```
There can be multiple roots, each whose name is set to ''.
5. Add in the necessary line in your urls.py file. Example is listed [here](https://github.com/FarhansCode/file_repository/blob/master/testapp/urls.py#L7).

## Help

This is my first public submission to the Internets. Please review my code and
provide suggestions. In particular, I think the get_path() in 
file_repository/commands.py method is ugly and does too much.

Second, I use regular expressions twice in this project. Please review them.
They are located in the testapp/urls.py and in get_path().

Last, I am not yet versed in writing Django unittests. Some sample unittests
would be nice!
