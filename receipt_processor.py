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
    "Given raw OCR text from a receipt or invoice, return ONLY a JSON object with no markdown, no explanation.\n\n"
    "Rules:\n"
    "- vendor: the actual shop, restaurant, or business name. "
    "NEVER use payment terminal or card network names such as: "
    "Global Payments, Worldpay, SumUp, iZettle, Square, Stripe, Visa, Mastercard, Amex. "
    "These appear at the top of the receipt as the terminal brand — skip them and look for the real merchant name below.\n"
    "- amount: the final total as a plain number (e.g. 16.00). "
    "Use the line labelled Total, Grand Total, or Amount Due. "
    "Never use a serial number, S/N, MID, TID, AID, or card number.\n"
    "- currency: 3-letter ISO code (GBP, EUR, USD, NOK, etc.)\n"
    "- date: transaction date as YYYY-MM-DD\n\n"
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
