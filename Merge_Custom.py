from PyPDF2 import PdfMerger

def merge_pdfs(first_pdf, second_pdf, output_filename):
    merger = PdfMerger()
    merger.append(first_pdf)
    merger.append(second_pdf)
    with open(output_filename, "wb") as output_file:
        merger.write(output_file)
    merger.close()

# Usage example:
merge_pdfs("Custom_Start.pdf", "Data_Report.pdf", "Quality-Report.pdf")
