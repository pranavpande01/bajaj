import json
from utils import *
from doit import *
import time
from tester import *
def orchestrate(path,mode,mode2=0):
    try:
        dur=time.time()
        split_pdf_simple(path)
        pdfs=print_file_paths_pathlib("/home/ubuntu/pranav/temp_outputs/splits")
        pagewise_line_items=[]
        total_item_count=0
        reconciled_ammount=0

        for j,pdf in enumerate(pdfs):
            if mode==0:
                b,a=doit(f"{pdf}",f"train_sample_{j}",0)
            if mode==1:
                b,a=doit(f"{pdf}",f"train_sample_{j}",1)
            else:
                with open('/home/ubuntu/pranav/temp_outputs/response.json', 'r') as f:
                    data = json.load(f)
                b,a=validate("/home/ubuntu/pranav/temp_outputs/recieved/recieved.json","/home/ubuntu/pranav/temp_outputs/response.json")

                #b,a=validate(f"{pdf}",f"train_sample_{j}")

                #/home/ubuntu/pranav/temp_outputs/recieved

            bill_items=[]

            for k in PageExtraction.model_validate_json(a.text).bill_items:
                        bill_items.append({
                                 "item_name": k.item_name,
                                 "item_amount": k.item_amount    ,
                                 "item_rate": k.item_rate,
                                 "item_quantity": k.item_quantity
                        })
                        reconciled_ammount+=k.item_amount
            #print(len(bill_items))
            total_item_count+=len(bill_items)
            pagewise_line_items.append({"page_no":str(j+1),"page_type":PageExtraction.model_validate_json(a.text).page_type,"bill_items":bill_items})
        response={
                  "is_success": True,
                  "data":{"pagewise_line_items":pagewise_line_items,
                          "total_item_count":total_item_count,
                          "reconciled_amount":round(reconciled_ammount,2)
                         }

            }

        with open(f"/home/ubuntu/pranav/temp_outputs/response.json", "w") as f:
            json.dump(response, f, indent=2)

    

        print(response)
    except Exception as e:
        print(e)
        #print(pdfs)
        #remove("/home/ubuntu/pranav/zone3/temp_outputs")
