import easyocr
import json
import os
import re
from datetime import datetime
from PIL import Image
import ollama

_MODEL = os.environ.get("OLLAMA_MODEL", "llama3.2")

_SYSTEM_PROMPT = (
    "You are a receipt and invoice data extractor. "
    "Given raw OCR text from a receipt or invoice, extract the following fields and return ONLY a JSON object "
    "with no markdown, no explanation:\n"
    "- vendor: the merchant or business name (not a payment processor like Visa, Mastercard, "
    "Global Payments, SumUp, iZettle, Square, etc.)\n"
    "- amount: the final total as a number (e.g. 16.00). Use the 'Total', 'Grand Total', or 'Amount Due' "
    "line — never a serial number, S/N, or card number.\n"
    "- currency: the 3-letter ISO currency code (e.g. GBP, EUR, USD, NOK)\n"
    "- date: the transaction date in YYYY-MM-DD format\n\n"
    "If a field cannot be determined, use null. Return only the JSON object."
)


class ReceiptProcessor:
    def __init__(self):
        self.reader = easyocr.Reader(['en'], gpu=False)

    def extract_text(self, image_path: str) -> str:
        result = self.reader.readtext(image_path)
        return "\n".join([line[1] for line in result])

    def _parse_with_ollama(self, raw_text: str) -> dict:
        response = ollama.chat(
            model=_MODEL,
            messages=[
                {"role": "system", "content": _SYSTEM_PROMPT},
                {"role": "user", "content": f"Extract data from this receipt text:\n\n{raw_text}"},
            ],
            options={"temperature": 0},
        )
        content = response["message"]["content"].strip()
        clean = re.sub(r"^```(?:json)?\s*|\s*```$", "", content, flags=re.DOTALL).strip()
        return json.loads(clean)

    def process_receipt(self, image_path: str) -> dict:
        try:
            raw_text = self.extract_text(image_path)
            data = self._parse_with_ollama(raw_text)

            return {
                "success": True,
                "vendor": data.get("vendor") or "Unknown Vendor",
                "amount": float(data["amount"]) if data.get("amount") is not None else None,
                "currency": data.get("currency"),
                "date": data.get("date") or datetime.now().strftime("%Y-%m-%d"),
                "raw_text": raw_text,
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def validate_image(self, file_path: str) -> bool:
        try:
            img = Image.open(file_path)
            img.verify()
            return True
        except Exception:
            return False
