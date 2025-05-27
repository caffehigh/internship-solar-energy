"""
OCR processing for electricity bills
"""
import re
import io
import streamlit as st

# Optional imports for OCR functionality
try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

try:
    import PyPDF2
    PYPDF2_AVAILABLE = True
except ImportError:
    PYPDF2_AVAILABLE = False

class BillOCRProcessor:
    def __init__(self):
        self.amount_patterns = [
            r'total[:\s]*₹?\s*(\d+(?:,\d+)*(?:\.\d{2})?)',
            r'amount[:\s]*₹?\s*(\d+(?:,\d+)*(?:\.\d{2})?)',
            r'bill[:\s]*₹?\s*(\d+(?:,\d+)*(?:\.\d{2})?)',
            r'₹\s*(\d+(?:,\d+)*(?:\.\d{2})?)',
            r'rs\.?\s*(\d+(?:,\d+)*(?:\.\d{2})?)',
            r'current[:\s]*₹?\s*(\d+(?:,\d+)*(?:\.\d{2})?)',
            r'payable[:\s]*₹?\s*(\d+(?:,\d+)*(?:\.\d{2})?)'
        ]

        self.units_patterns = [
            r'units[:\s]*(\d+(?:,\d+)*(?:\.\d{2})?)',
            r'kwh[:\s]*(\d+(?:,\d+)*(?:\.\d{2})?)',
            r'consumption[:\s]*(\d+(?:,\d+)*(?:\.\d{2})?)',
            r'energy[:\s]*(\d+(?:,\d+)*(?:\.\d{2})?)',
            r'present[:\s]*reading[:\s]*(\d+(?:,\d+)*(?:\.\d{2})?)',
            r'current[:\s]*reading[:\s]*(\d+(?:,\d+)*(?:\.\d{2})?)'
        ]

    def process_uploaded_file(self, uploaded_file):
        """
        Process uploaded file (PDF or image) and extract bill information

        Args:
            uploaded_file: Streamlit uploaded file object

        Returns:
            Dictionary with extracted information
        """
        try:
            file_type = uploaded_file.type

            if file_type == "application/pdf":
                return self._process_pdf(uploaded_file)
            elif file_type.startswith("image/"):
                return self._process_image(uploaded_file)
            else:
                return {"error": "Unsupported file type. Please upload PDF or image files."}

        except Exception as e:
            return {"error": f"Error processing file: {str(e)}"}

    def _process_pdf(self, uploaded_file):
        """Extract text from PDF file"""
        if not PYPDF2_AVAILABLE:
            return {"error": "PyPDF2 not installed. Please install it to process PDF files."}

        try:
            # Read PDF content
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
            text = ""

            # Extract text from all pages
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"

            return self._extract_bill_info(text)

        except Exception as e:
            return {"error": f"Error reading PDF: {str(e)}"}

    def _process_image(self, uploaded_file):
        """Extract text from image file using OCR"""
        try:
            # For demo purposes, we'll simulate OCR without actually using pytesseract
            # In a real implementation, you would use:
            # import pytesseract
            # image = Image.open(uploaded_file)
            # text = pytesseract.image_to_string(image)

            # Simulated OCR result for demo
            return {
                "success": True,
                "message": "OCR functionality is simulated for demo. In production, this would use pytesseract to extract text from images.",
                "extracted_amount": None,
                "extracted_units": None,
                "raw_text": "Simulated OCR text extraction"
            }

        except Exception as e:
            return {"error": f"Error processing image: {str(e)}"}

    def _extract_bill_info(self, text):
        """
        Extract bill amount and units from text

        Args:
            text: Extracted text from bill

        Returns:
            Dictionary with extracted information
        """
        text_lower = text.lower()

        # Extract amount
        extracted_amount = None
        for pattern in self.amount_patterns:
            matches = re.findall(pattern, text_lower, re.IGNORECASE)
            if matches:
                # Get the largest amount found (likely the total)
                amounts = [self._parse_number(match) for match in matches]
                extracted_amount = max(amounts) if amounts else None
                break

        # Extract units
        extracted_units = None
        for pattern in self.units_patterns:
            matches = re.findall(pattern, text_lower, re.IGNORECASE)
            if matches:
                # Get the first valid units found
                units = [self._parse_number(match) for match in matches]
                extracted_units = units[0] if units else None
                break

        return {
            "success": True,
            "extracted_amount": extracted_amount,
            "extracted_units": extracted_units,
            "raw_text": text[:500] + "..." if len(text) > 500 else text,
            "message": "Text extracted successfully from PDF"
        }

    def _parse_number(self, number_str):
        """Parse number string and convert to float"""
        try:
            # Remove commas and convert to float
            cleaned = re.sub(r'[,\s]', '', str(number_str))
            return float(cleaned)
        except (ValueError, TypeError):
            return None

    def validate_extracted_data(self, extracted_amount, extracted_units):
        """
        Validate extracted data and provide suggestions

        Args:
            extracted_amount: Extracted bill amount
            extracted_units: Extracted units consumed

        Returns:
            Dictionary with validation results
        """
        validation_results = {
            "amount_valid": False,
            "units_valid": False,
            "suggestions": []
        }

        # Validate amount
        if extracted_amount and 100 <= extracted_amount <= 50000:
            validation_results["amount_valid"] = True
        else:
            validation_results["suggestions"].append(
                "Please verify the bill amount. Typical range: ₹100 - ₹50,000"
            )

        # Validate units
        if extracted_units and 50 <= extracted_units <= 5000:
            validation_results["units_valid"] = True
        else:
            validation_results["suggestions"].append(
                "Please verify the units consumed. Typical range: 50 - 5000 units"
            )

        # Calculate tariff if both are valid
        if validation_results["amount_valid"] and validation_results["units_valid"]:
            calculated_tariff = extracted_amount / extracted_units
            validation_results["calculated_tariff"] = round(calculated_tariff, 2)

            if 3 <= calculated_tariff <= 15:
                validation_results["tariff_reasonable"] = True
            else:
                validation_results["tariff_reasonable"] = False
                validation_results["suggestions"].append(
                    f"Calculated tariff (₹{calculated_tariff:.2f}/unit) seems unusual. Please verify."
                )

        return validation_results
