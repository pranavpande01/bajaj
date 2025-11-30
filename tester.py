import json
from utils import *
import time

from google import genai
from google.genai import types
import pathlib
import os
from pydantic import BaseModel, Field
from typing import List, Optional

from dotenv import load_dotenv
load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE-API-KEY"))

REFERENCE_PDF_PATH = "/home/ubuntu/pranav/reference/sample_composite.pdf"


class ValidatedBillItem(BaseModel):
    item_name: str = Field(description="Name of the item")
    item_amount: float = Field(description="Net amount")
    item_rate: Optional[float] = Field(default=None, description="Rate per unit")
    item_quantity: Optional[float] = Field(default=None, description="Quantity")


class ValidatedPageExtraction(BaseModel):
    page_no: str = Field(description="Page number")
    page_type: str = Field(description="Type: Bill Detail, Final Bill, or Pharmacy")
    bill_items: List[ValidatedBillItem] = Field(description="List of line items")


class ValidationResponse(BaseModel):
    was_corrected: bool = Field(description="True if any corrections were made to the original extraction")
    correction_notes: Optional[str] = Field(default=None, description="Brief explanation of what was corrected, if anything")
    pagewise_line_items: List[ValidatedPageExtraction] = Field(description="The validated/corrected extraction")
    total_item_count: int = Field(description="Total count of all line items")
    reconciled_amount: float = Field(description="Sum of all item amounts")


def generate_validator_prompt(extraction_json: dict) -> str:
    return f"""
You are a VALIDATOR for medical bill extraction. Your job is to verify and correct extractions if needed.

### CONTEXT
1. You are given:
   - The ORIGINAL PDF (medical bill/invoice)
   - A REFERENCE PDF showing a sample input and its correct JSON output (use this to understand the expected format and quality)
   - The EXTRACTION produced by another model (shown below)

2. Your task:
   - Compare the extraction against the original PDF
   - Check for: missing items, incorrect amounts, wrong item names, duplicates, misclassified page types
   - Return the CORRECTED extraction (or the original if it's already correct)

### EXTRACTION TO VALIDATE
{json.dumps(extraction_json, indent=2)}

### VALIDATION RULES
- Every line item in the PDF must appear in the extraction
- item_name must match the PDF exactly (no paraphrasing)
- item_amount must be the net amount shown in the bill
- item_rate and item_quantity should be extracted if visible, null otherwise
- page_type must be: "Bill Detail", "Final Bill", or "Pharmacy"
- Do NOT add items that don't exist in the PDF
- Do NOT remove items that do exist in the PDF
- Recalculate total_item_count and reconciled_amount based on validated items

### OUTPUT
Return the validated extraction. Set was_corrected=true if you made ANY changes, false if the original was correct.
If corrected, briefly explain what was wrong in correction_notes.
"""


def validate(original_pdf_path: str, extraction_json: dict) -> tuple:
    """
    Validate and potentially correct an extraction using Gemini 2.5 Pro.

    Args:
        original_pdf_path: Path to the original PDF that was extracted
        extraction_json: The extraction output from the Flash model

    Returns:
        tuple: (usage_metadata, validated_response)
    """
    original_pdf = pathlib.Path(original_pdf_path)
    reference_pdf = pathlib.Path(REFERENCE_PDF_PATH)

    prompt = generate_validator_prompt(extraction_json)

    contents = [
        types.Part.from_bytes(
            data=original_pdf.read_bytes(),
            mime_type='application/pdf',
        ),
    ]

    if reference_pdf.exists():
        contents.append(
            types.Part.from_bytes(
                data=reference_pdf.read_bytes(),
                mime_type='application/pdf',
            )
        )

    contents.append(prompt)

    response = client.models.generate_content(
        model="gemini-2.5-pro",
        contents=contents,
        config={
            "response_mime_type": "application/json",
            "response_json_schema": ValidationResponse.model_json_schema(),
        },
    )

    return response.usage_metadata, response
  