
import json
def generate_prompt():
  user_prompt="""
  You are given a multi-page medical bill/invoice document. Extract structured data from it.

  ### TASK
  From the document, extract:
  - Every line item from every page  
  - item_name (exact text)
  - item_rate
  - item_quantity
  - item_amount (net amount mentioned in bill)

  Also determine:
  - page_type for each page
  - total_item_count across all pages

  ### PAGE TYPE RULES
  - "Bill Detail" → itemized list, rates, quantities
  - "Final Bill" → has summary, sub-total, final total
  - "Pharmacy" → medicine-related bills with drug names, quantities, rates

  ### OUTPUT JSON SCHEMA
  Return JSON in this EXACT structure:

  {
    "pagewise_line_items": [
      {
        "page_no": "string",
        "page_type": "Bill Detail | Final Bill | Pharmacy",
        "bill_items": [
          {
            "item_name": "string",
            "item_amount": float,
            "item_rate": float,
            "item_quantity": float
          }
        ]
      }
    ],
    "total_item_count": integer
  }

  ### INSTRUCTIONS
  - Return only line items visible in the document.
  - Do NOT compute any totals.
  - Do NOT infer item names.
  - Do NOT duplicate items.
  - If a page has zero items, return an empty array for bill_items.
  - Maintain the order of pages in the document.
  - Input document is a medical invoice.
  - Donot confuse entities or fields like Service Amount, Total Discount, Service Amount After Discount (Bill of Supply), etc, you get the point, as these are not standard drugs, or medical procedures or medical expenditures


  Now produce the JSON output.
  """
  return user_prompt

def generate_tester_prompt():
  with open('/home/ubuntu/pranav/temp_outputs/response.json', 'r') as f:
      data = json.load(f)
    user_prompt=f"""
  Gemini 2.5-flash was asked to generate given a multi-page medical bill/invoice document to extract structured data from it.
  ### TASK
  From the document, extract:
  - Every line item from every page  
  - item_name (exact text)
  - item_rate
  - item_quantity
  - item_amount (net amount mentioned in bill)

  Also determine:
  - page_type for each page
  - total_item_count across all pages

  ### PAGE TYPE RULES
  - "Bill Detail" → itemized list, rates, quantities
  - "Final Bill" → has summary, sub-total, final total
  - "Pharmacy" → medicine-related bills with drug names, quantities, rates

  ### OUTPUT JSON SCHEMA
  Return JSON in this EXACT structure:

  {
    "pagewise_line_items": [
      {
        "page_no": "string",
        "page_type": "Bill Detail | Final Bill | Pharmacy",
        "bill_items": [
          {
            "item_name": "string",
            "item_amount": float,
            "item_rate": float,
            "item_quantity": float
          }
        ]
      }
    ],
    "total_item_count": integer
  }

  ### INSTRUCTIONS
  - Return only line items visible in the document.
  - Do NOT compute any totals.
  - Do NOT infer item names.
  - Do NOT duplicate items.
  - If a page has zero items, return an empty array for bill_items.
  - Maintain the order of pages in the document.
  - Input document is a medical invoice.
  - Donot confuse entities or fields like Service Amount, Total Discount, Service Amount After Discount (Bill of Supply), etc, you get the point, as these are not standard drugs, or medical procedures or medical expenditures


  The following output was produced:
  {d}
  """
  return user_prompt

