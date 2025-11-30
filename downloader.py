import json
import urllib.request
import uuid

def download_pdf(url, output_path=f"/home/ubuntu/pranav/temp_outputs/recieved/recieved.pdf"):
    #if output_path is None:
    #    output_path = f"/tmp/{uuid.uuid4()}.pdf"

    urllib.request.urlretrieve(url, output_path)
    return output_path

