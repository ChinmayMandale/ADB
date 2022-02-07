import os
from azure.storage.blob import BlobServiceClient
from flask import Flask, request, redirect

app = Flask(__name__)

connect_str = 'DefaultEndpointsProtocol=https;AccountName=chinmaystorageaccount;AccountKey=7B2eUPyikZVLzGP5EdlpaRQV4IG1dckKbG/4q3gnNFPnLs78yvLkpt77BctLUUwwwH++yIJuD/WW1lBOoqK4Dw==;EndpointSuffix=core.windows.net'
container_name = "assignment1container"

blob_service_client = BlobServiceClient.from_connection_string(connect_str)
try:
    container_client = blob_service_client.get_container_client(container_name)
    container_client.get_container_properties()
except Exception as e:
    print(e)
    print("Creating container...")
    container_client = blob_service_client.create_container(container_name)


@app.route("/")
def view_photos():
    blob_items = container_client.list_blobs()  # list all the blobs in the container

    img_html = "<div style='display: flex; justify-content: space-between; flex-wrap: wrap;'>"

    for blob in blob_items:
        blob_client = container_client.get_blob_client(blob.name)
        print(blob.name)
        img_html += "<img src='{}' width='auto' height='200' style='margin: 0.5em 0;'/>".format(
            blob_client.url)  # get the blob url and append it to the html

    img_html += "</div>"

    # return the html with the images
    return """
    <head>
    <!-- CSS only -->
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
    </head>
    <body>
        <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
            <div class="container">
                <a class="navbar-brand" href="/">Photos App</a>
            </div>
        </nav>
        <div class="container">
            <div class="card" style="margin: 1em 0; padding: 1em 0 0 0; align-items: center;">
                <h3>Upload new File</h3>
                <div class="form-group">
                    <form method="post" action="/upload-photos" 
                        enctype="multipart/form-data">
                        <div style="display: flex;">
                            <input type="file" accept=".png, .jpeg, .jpg, .gif" name="photos" multiple class="form-control" style="margin-right: 1em;">
                            <input type="submit" class="btn btn-primary">
                        </div>
                    </form>
                </div> 
            </div>

    """ + img_html + "</div></body>"


# flask endpoint to upload a photo
@app.route("/upload-photos", methods=["POST"])
def upload_photos():
    filenames = ""

    for file in request.files.getlist("photos"):
        try:
            container_client.upload_blob(file.filename,file)  # upload the file to the container using the filename as the blob name
            filenames += file.filename + "<br /> "
        except Exception as e:
            print(e)
            print("Ignoring duplicate filenames")  # ignore duplicate filenames

    return redirect('/')
