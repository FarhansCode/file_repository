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

## License

Licensed under the BSD. You don't have to return your code to me, but it would
be nice :)

## Initialization

The testapp requires the python-magic module. You can install as follows:
```
pip install python-magic
```

I have not yet figured out how to add an initializer in a migration, so you will
have to create an initial root Inode.

```python
Inode.methods.createroot(rootname='testapp')
```

If you do not do this, it will return a 500 error message.

## How to use

1. Download and save the code into your project directory.
2. Insert the application in your INSTALLED_APPS list. [Example](https://github.com/FarhansCode/file_repository/blob/master/testapp/settings.py#L40)
3. Create the database migrations and perform the migration.
4. Create the initial root Inode element.
```python
Inode.methods.createroot(rootname='testapp')
```
5. Add in the necessary line in your urls.py file. Example is listed [here](https://github.com/FarhansCode/file_repository/blob/master/testapp/urls.py#L7).

## Where do files go?
By default, files are uploaded into file_repository/_file. You can change that path [here](https://github.com/FarhansCode/file_repository/blob/master/file_repository/models.py#L14).

## Help

This is my first public submission to the Internets. Please review my code and
provide suggestions. Few things I need help on. 

First, I use regular expressions a few times in this project. I am still new to
regex and it would be nice to have it reviewed.

Second, I am not yet versed in writing Django unittests. Some unittests would
be nice!
