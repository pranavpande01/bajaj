from pathlib import Path
from pypdf import PdfReader, PdfWriter
import os

def split_pdf_simple(input_pdf_path, output_folder="/home/ubuntu/pranav/temp_outputs/splits"):

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    reader = PdfReader(input_pdf_path)
    
    for i, page in enumerate(reader.pages):
        writer = PdfWriter()
        writer.add_page(page)

        output_filename = os.path.join(output_folder, f"page_{i + 1}.pdf")
        
        with open(output_filename, "wb") as output_stream:
            writer.write(output_stream)
        

def print_file_paths_pathlib(directory_path_str):
    p = Path(directory_path_str)
    return [str(item.resolve()) for item in sorted(p.iterdir()) if item.is_file()]


def remove(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)

        if os.path.isfile(file_path):
            os.remove(file_path)


from google import genai
from pydantic import BaseModel, Field
from typing import List, Optional

# Single line item
class BillItem(BaseModel):
    item_name: str = Field(description="Name of the item or medical procedure or drug or particulars or service name as mentioned in the bill")
    item_amount: float = Field(description="Net Amount of the corresponding item post discounts as mentioned in the bill, or as rupees, in many cases, might appear in the last column, try to reason if unsure of the same")
    item_rate: Optional[float] = Field(default=None, description="Rate of the corresponding item as mentioned in the bill, might appear separately or clubbed with quantity as rate x quantity or quantity x rate, for example 10x2, try to infer from other fields if not mentioned explicitly, output null if not mentioned")
    item_quantity: Optional[float] = Field(default=None, description="Quantity of the corresponding item as mentioned in the bill, might appear separately or clubbed with rate as rate x quantity or quantity x rate, for example 10x2, try to infer from other fields if not mentioned explicitly, output null if not mentioned")

# Wrapper to hold MULTIPLE items - THIS IS THE KEY FIX!
class PageExtraction(BaseModel):
    page_type: str = Field(description="Type of the page - can be one of the following: Bill Detail, Final Bill, Pharmacy'")
    bill_items: List[BillItem] = Field(description="List of ALL line items extracted from this page of the bill")
