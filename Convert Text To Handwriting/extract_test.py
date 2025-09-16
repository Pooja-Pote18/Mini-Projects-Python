from tkinter import Tk
from tkinter.filedialog import askopenfilename
import PyPDF2
from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import os
import sys

#  Determine Script Folder 
script_folder = os.path.dirname(os.path.abspath(__file__))

#  Step 1: Select PDF 
Tk().withdraw()  
pdf_file = askopenfilename(title="Select a PDF file", filetypes=[("PDF files", "*.pdf")])
if not pdf_file:
    print("❌ No PDF selected. Exiting.")
    sys.exit()
print("Selected PDF:", pdf_file)

#  Step 2: Check Font 
default_font = os.path.join(script_folder, "DancingScript-Regular.ttf")  # default font in script folder

if os.path.exists(default_font):
    font_path = default_font
    print(f"✅ Found font: {font_path}")
else:
    print(f"⚠️ Font 'DancingScript-Regular.ttf' not found in script folder.")
    print("Please select a handwriting TTF font file manually.")
    Tk().withdraw()
    font_path = askopenfilename(title="Select a TTF font file", filetypes=[("TTF fonts", "*.ttf")])
    if not font_path:
        print("❌ No font selected. Exiting.")
        sys.exit()
    print(f"✅ Selected font: {font_path}")

#  Step 3: Extract Text from PDF 
def extract_text_from_pdf(pdf_file):
    text = ""
    with open(pdf_file, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

extracted_text = extract_text_from_pdf(pdf_file)
print(f"✅ Extracted {len(extracted_text)} characters from PDF.")

#  Step 4: Convert to Handwriting Image 
def text_to_handwriting_image(text, output_file, font_path):
    try:
        img = Image.new("RGB", (1200, 1600), color="white")
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(font_path, 28)
        y_text = 50
        for line in text.split("\n"):
            draw.text((50, y_text), line, font=font, fill=(0, 0, 0))
            y_text += 40  # line spacing
        img.save(output_file)
        print(f"✅ Saved handwriting image as {output_file}")
    except Exception as e:
        print(f"❌ Error creating handwriting image: {e}")

# Full paths for outputs
png_file = os.path.join(script_folder, "handwriting.png")
pdf_file_output = os.path.join(script_folder, "handwriting_output.pdf")

# Save first 1000 characters as image
text_to_handwriting_image(extracted_text[:1000], png_file, font_path)

#  Step 5: Convert to Handwriting PDF 
def text_to_handwriting_pdf(text, output_pdf, font_path):
    try:
        c = canvas.Canvas(output_pdf, pagesize=A4)
        pdfmetrics.registerFont(TTFont("Handwriting", font_path))
        c.setFont("Handwriting", 14)
        width, height = A4
        y = height - 50
        for line in text.split("\n"):
            if y < 50:  # new page
                c.showPage()
                c.setFont("Handwriting", 14)
                y = height - 50
            c.drawString(50, y, line)
            y -= 20
        c.save()
        print(f"✅ Saved handwriting PDF as {output_pdf}")
    except Exception as e:
        print(f"❌ Error creating handwriting PDF: {e}")

# Convert full text to PDF
text_to_handwriting_pdf(extracted_text, pdf_file_output, font_path)
