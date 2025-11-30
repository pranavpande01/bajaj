# Medical Bill Extraction API

A FastAPI-based service that extracts structured line-item data from medical bill/invoice PDF documents using Google's Gemini AI models.

## Overview

This API accepts a PDF document URL, downloads it, splits it page-by-page, and uses Gemini AI to extract structured billing information including item names, rates, quantities, and amounts.

## Endpoints

Base URL: `http://107.23.191.29`

### POST `/process`
Standard extraction using **Gemini 2.5 Flash**.

### POST `/process2`
Two-pass extraction: initial extraction with Gemini 2.5 Flash followed by validation with **Gemini 2.5 Pro**.

### POST `/process3`
Lightweight extraction using **Gemini 2.5 Flash Lite**.

## Request Format

All endpoints accept the same request body:

```json
{
    "document": "https://teal-databases.s3.us-east-1.amazonaws.com/TRAINING_SAMPLES/train_sample_10.pdf"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `document` | string | URL to the PDF document to process |

## Response Format

```json
{
  "is_success": true,
  "data": {
    "pagewise_line_items": [
      {
        "page_no": "1",
        "page_type": "Bill Detail | Final Bill | Pharmacy",
        "bill_items": [
          {
            "item_name": "string",
            "item_amount": 100.00,
            "item_rate": 50.00,
            "item_quantity": 2.0
          }
        ]
      }
    ],
    "total_item_count": 10,
    "reconciled_amount": 1500.50
  }
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `is_success` | boolean | Whether extraction succeeded |
| `pagewise_line_items` | array | Extracted data organized by page |
| `page_no` | string | Page number in the document |
| `page_type` | string | Classification: "Bill Detail", "Final Bill", or "Pharmacy" |
| `bill_items` | array | Line items extracted from the page |
| `item_name` | string | Name of the medical item/service/drug |
| `item_amount` | float | Net amount for the item |
| `item_rate` | float/null | Unit rate (if available) |
| `item_quantity` | float/null | Quantity (if available) |
| `total_item_count` | integer | Total number of line items across all pages |
| `reconciled_amount` | float | Sum of all item amounts |

## Page Type Classification

- **Bill Detail**: Itemized list with rates and quantities
- **Final Bill**: Summary page with sub-totals and final total
- **Pharmacy**: Medicine-related bills with drug names, quantities, and rates

## Example Usage

```bash
curl -X POST http://107.23.191.29/process \
  -H "Content-Type: application/json" \
  -d '{
    "document": "https://teal-databases.s3.us-east-1.amazonaws.com/TRAINING_SAMPLES/train_sample_10.pdf"
  }'
```

## Requirements

- Python 3.8+
- Google Gemini API key (set as `GOOGLE-API-KEY` environment variable)

### Dependencies

```
google-genai>=1.50.0
pydantic>=2.0.0
pypdf>=6.0.0
python-dotenv>=1.0.0
fastapi
requests
uvicorn
```

## Installation

```bash
pip install -r requirements.txt
```

## Running the Server

```bash
uvicorn main:app --host 0.0.0.0 --port 80
```

## Architecture

1. **main.py**: FastAPI application with three endpoints
2. **downloader.py**: Downloads PDF from provided URL
3. **utils.py**: PDF splitting utilities and Pydantic models for structured output
4. **doit.py**: Core Gemini API integration for extraction
5. **orchestrator.py**: Coordinates page-by-page processing and aggregates results
6. **tester.py**: Validation module using Gemini 2.5 Pro for quality assurance
7. **assets.py**: Prompt templates for extraction tasks

## Processing Pipeline

```
URL → Download PDF → Split into pages → Extract per page (Gemini) → Aggregate results → JSON response
```