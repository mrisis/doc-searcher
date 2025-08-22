import os
import PyPDF2
import re
import subprocess
import tempfile


def convert_docx_to_pdf(docx_path):
    output_dir = tempfile.mkdtemp()
    try:
        subprocess.run([
            "libreoffice", "--headless", "--convert-to", "pdf",
            "--outdir", output_dir, docx_path
        ], check=True)
        pdf_path = os.path.join(
            output_dir,
            os.path.splitext(os.path.basename(docx_path))[0] + ".pdf"
        )
        if os.path.exists(pdf_path):
            return pdf_path
        return None
    except Exception as e:
        print(f"خطا در تبدیل docx به pdf: {e}")
        return None


def search_in_pdf(file_path, search_term):
    results = []
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)

            for page_num, page in enumerate(pdf_reader.pages, 1):
                try:
                    text = page.extract_text()
                    if text and search_term.lower() in text.lower():
                        # پیدا کردن تعداد تکرار در صفحه
                        count = len(re.findall(re.escape(search_term.lower()), text.lower()))
                        results.append({
                            'page': page_num,
                            'count': count,
                            'preview': get_text_preview(text, search_term)
                        })
                except Exception as e:
                    print(f"خطا در خواندن صفحه {page_num}: {e}")
                    continue

    except Exception as e:
        print(f"خطا در خواندن PDF: {e}")
        return []

    return results


def search_in_docx(file_path, search_term):
    pdf_path = convert_docx_to_pdf(file_path)
    if not pdf_path:
        return []

    results = search_in_pdf(pdf_path, search_term)

    try:
        os.remove(pdf_path)
    except:
        pass

    return results


def get_text_preview(text, search_term, context_length=100):
    if not text:
        return ""

    lower_text = text.lower()
    lower_term = search_term.lower()

    index = lower_text.find(lower_term)
    if index == -1:
        return text[:context_length] + "..." if len(text) > context_length else text

    start = max(0, index - context_length // 2)
    end = min(len(text), index + len(search_term) + context_length // 2)

    preview = text[start:end]

    if start > 0:
        preview = "..." + preview
    if end < len(text):
        preview = preview + "..."

    return preview


def search_in_document(file_path, search_term):
    if not os.path.exists(file_path):
        return []

    file_extension = os.path.splitext(file_path)[1].lower()

    if file_extension == '.pdf':
        return search_in_pdf(file_path, search_term)
    elif file_extension in ['.docx', '.doc']:
        return search_in_docx(file_path, search_term)
    else:
        return []
