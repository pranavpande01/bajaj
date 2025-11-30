from fastapi import FastAPI
from pydantic import BaseModel
import requests
from downloader import download_pdf
import json
from utils import *
from tester import *
app = FastAPI()
from orchestrator import orchestrate
class DocumentRequest(BaseModel):
    document: str  # URL

@app.post("/process")
def process_document(req: DocumentRequest):
    response = requests.get(req.document, stream=True)

    if response.status_code != 200:
        return {"error": "Failed to fetch document"}

    content = response.content

    remove("/home/ubuntu/pranav/temp_outputs/recieved")
    remove("/home/ubuntu/pranav/temp_outputs/splits")
    download_pdf(req.document)
    orchestrate("/home/ubuntu/pranav/temp_outputs/recieved/recieved.pdf",0)
    import json
    with open('/home/ubuntu/pranav/temp_outputs/response.json', 'r') as f:
        data = json.load(f)

    # Print (log) the document bytes
    print("\n--- DOCUMENT RECEIVED ---")
    print(f"URL: {req.document}")
    print(f"Bytes: {len(content)}")
    print("-------------------------\n")
    remove("/home/ubuntu/pranav/temp_outputs/recieved")
    remove("/home/ubuntu/pranav/temp_outputs/splits")

        
    with open("/home/ubuntu/pranav/temp_outputs/response.json", "r") as f:
        return json.load(f)
    remove("/home/ubuntu/pranav/temp_outputs")

    #return {"status": "received", "size_bytes": len(content)}




@app.post("/process2")
def process_document2(req: DocumentRequest):
    response = requests.get(req.document, stream=True)

    if response.status_code != 200:
        return {"error": "Failed to fetch document"}

    content = response.content

    remove("/home/ubuntu/pranav/temp_outputs/recieved")
    remove("/home/ubuntu/pranav/temp_outputs/splits")
    download_pdf(req.document)
    orchestrate("/home/ubuntu/pranav/temp_outputs/recieved/recieved.pdf",0)
    import json
    orchestrate("/home/ubuntu/pranav/temp_outputs/recieved/recieved.json",1)
    
    # Print (log) the document bytes
    print("\n--- DOCUMENT RECEIVED ---")
    print(f"URL: {req.document}")
    print(f"Bytes: {len(content)}")
    print("-------------------------\n")
    remove("/home/ubuntu/pranav/temp_outputs/recieved")
    remove("/home/ubuntu/pranav/temp_outputs/splits")

        
    with open("/home/ubuntu/pranav/temp_outputs/response.json", "r") as f:
        return json.load(f)
    remove("/home/ubuntu/pranav/temp_outputs")
    #return {"status": "received", "size_bytes": len(content)}
