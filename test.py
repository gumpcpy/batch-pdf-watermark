import csv
from PyPDF2 import PdfReader, PdfWriter
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
import reportlab.pdfbase.ttfonts

input_pdf = "input.pdf"  # Replace with your input PDF file path
name_txt = "name.txt" 

# 创建水印信息
def create_watermark(content):
    """水印信息"""
    # 默认大小为21cm*29.7cm
    file_name = "mark.pdf"
    # 水印PDF页面大小
    c = canvas.Canvas(file_name, pagesize=(30 * cm, 30 * cm))
    # 移动坐标原点(坐标系左下为(0,0))
    # c.translate(4 * cm, 0 * cm)
    c.translate(15* cm, 15 * cm)
    # 设置字体格式与大小,中文需要加载能够显示中文的字体，否则就会乱码，注意字体路径
    try:
        reportlab.pdfbase.pdfmetrics.registerFont(
            reportlab.pdfbase.ttfonts.TTFont('STHeiti', 'STHeiti.ttc'))
        c.setFont('STHeiti', 150)
    except:
        # 默认字体，只能够显示英文
        c.setFont("Helvetica", 30)
        content = "watermark"
 
    # 旋转角度度,坐标系被旋转
    c.rotate(30)
    # 指定填充颜色
    c.setFillColorRGB(0, 0, 0)
    # 设置透明度,1为不透明
    c.setFillAlpha(0.05)
    # 画几个文本,注意坐标系旋转的影响
    c.drawString(0 * cm, 3 * cm, content)
    # 关闭并保存pdf文件
    c.save()
    return file_name

# 插入水印
def add_watermark(pdf_file_in, pdf_file_mark, pdf_file_out):
    pdf_output = PdfWriter()
    input_stream = open(pdf_file_in, 'rb')
    pdf_input = PdfReader(input_stream, strict=False)
 
    # 获取PDF文件的页数
    # pageNum = pdf_input.getNumPages()
    pageNum = len(pdf_input.pages)
 
    # 读入水印pdf文件
    pdf_watermark = PdfReader(open(pdf_file_mark, 'rb'), strict=False)
    # 给每一页打水印
    for i in range(pageNum):
        page = pdf_input.pages[i]

        page.merge_page(pdf_watermark.pages[0])
        page.compress_content_streams()  # 压缩内容
        pdf_output.add_page(page)
    pdf_output.write(open(pdf_file_out, 'wb'))


# Read the CSV file
with open(name_txt, 'r') as file:
    for name in file:
        print(name.strip())
        name = name.strip()
        pdf_file_out = f"Output_{name}.pdf"
        add_watermark(input_pdf, create_watermark(name), pdf_file_out)


# Open the input PDF file
# with open(input_pdf, 'rb') as file:
#     pdf_reader = PdfReader(file)

#     # Iterate through each name and generate PDFs with watermarks
#     for i, name in enumerate(names, 1):
#         output_pdf = f"input_name{i}.pdf"  # Output PDF file name

#         # Create a PDF writer object
#         pdf_writer = PdfWriter()

#         # Add watermark to each page of the input PDF
#         for page_num in range(len(pdf_reader.pages)):
#             page = pdf_reader.pages[page_num]

#             # Create a watermark object
#             watermark = page

#             # Add the watermark content from the CSV to each page
#             watermark_content = name[0]  # Assuming the CSV has one column
#             watermark.add_watermark(watermark_content, fontsize=50, alpha=0.5, inplace=True)

#             # Add the watermarked page to the PDF writer
#             pdf_writer.add_page(watermark)

#         # Write the watermarked PDF to the output file
#         with open(output_pdf, 'wb') as output_file:
#             pdf_writer.write(output_file)

#         print(f"Watermarked PDF generated: {output_pdf}")
