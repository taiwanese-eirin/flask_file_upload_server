# Flask File Upload Server
Work with ChatGPT to build an improved Python 3 uploadserver
This README is originally wrote by ChatGPT with some modifications 

This application is a Flask file upload server which allows users to upload files and download them at a later time. The uploaded files are stored on the server and can be accessed or deleted by the user.

## Getting started:

To get started with the application, you need to have Python 3 and Flask installed. You can use pip3 to install Flask: `pip3 install Flask`.

You can start the application by running the app.py file. This can be done using the command: `python3 app.py`.

Once the application is running, you can access it in your browser at http://localhost:5000/ or http://127.0.0.1:5000/.

## Uploading files:

To upload files, you need to navigate to the home page of the application in your browser. You will see a file upload form where you can select one or more files to upload. After selecting the file(s), click the "Upload" button to upload the file(s). The uploaded files will be saved to the UPLOAD_FOLDER location as specified in the app.py file.

## Downloading files:

To download a file, you can navigate to the home page of the application and click on the file you want to download. This will download the file to your computer.

## Deleting files:

To delete a file, you can navigate to the home page of the application and click on the "Delete" button next to the file you want to delete. You will be prompted to confirm the deletion. Click "Delete" to confirm the deletion, or "Cancel" to cancel the deletion.

## File types:

The application supports the following file types for upload and download: jpg, jpeg, png, gif. Other file types can be added by modifying the get_file_list function in the app.py file.

## Limitations:

The application has the following limitations:

- It does not currently support user authentication, so anyone who can access the application can upload, download, and delete files.
- It does not currently support the ability to rename files.
- It does not currently support the ability to search for files.

## Improvements:

Some improvements that can be made to the application include:

- Adding user authentication to prevent unauthorized access.
- Adding the ability to rename files.
- Adding the ability to search for files.
- Moving the location of the uploads folder and changing the default port. 

### Changing the default port:

The default port for the application is 5000. To change this, modify the following line in app.py:

`app.run(debug=True, port=XXXX)`

where `XXXX` is the desired port number.

### Changing the default uploads path:

To change the default uploads path, modify the following line in app.py:

`UPLOAD_FOLDER = 'path/to/new/uploads/folder'`


where `path/to/new/uploads/folder` is the desired path to the new uploads folder.

## Previewing files:

The application currently supports previewing images and videos.




