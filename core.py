import csv
import os
from PyPDF2 import PdfReader, PdfWriter
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
import reportlab.pdfbase.ttfonts



class WatermarkCore():
    txt_path = "name.txt"  
    pdf_path = "input.pdf" 
    # 指定外部字體檔案的路徑
    font_path = '../../STHeiti.ttc'
    pdf_name_pre = ""
    water_x = 5
    water_y = 5
    water_r = 30
    water_font_size = 150
    water_trans = 0.5


    def __init__(self,**thePath):	
        # txt_file
        if os.path.isfile(thePath['txt_path']):						
            if thePath['txt_path'].find('.') >= 0:				
                tmp = thePath['txt_path'].split('.')
                if tmp[1] != 'txt':
                    print('No Valid TXT File')		
                    return			
        else:
            print("Please Choose TXT")
            return        

        # pdf_file 
        if os.path.isfile(thePath['pdf_path']):						
            if thePath['pdf_path'].find('.') >= 0:				
                tmp = thePath['pdf_path'].split('.')
                if tmp[1] != 'pdf':
                    print('No Valid PDF File')		
                    return			
                else:
                    self.pdf_name_pre = tmp[0]

        
        else:
            print("Please Choose PDF")
            return        
        
        # param
        self.txt_path = thePath['txt_path']
        self.pdf_path = thePath['pdf_path']    
        self.font_path = thePath['font_path']
        # print("--------------------------------")
        # print(type(thePath['water_x']))
        self.water_x = int(thePath['water_x'])
        self.water_y = int(thePath['water_y'])
        self.water_r = int(thePath['water_r'])
        self.water_font_size = int(thePath['water_font_size'])
        self.water_trans = int(thePath['water_trans']) / 100
            
        return

    # 创建水印信息
    def create_watermark(self,content):
        """水印信息"""
        # 默认大小为21cm*29.7cm
        file_name = "mark.pdf"
        # 水印PDF页面大小
        c = canvas.Canvas(file_name, pagesize=(30 * cm, 30 * cm))
        # 移动坐标原点(坐标系左下为(0,0))
        # c.translate(4 * cm, 0 * cm)
        c.translate( self.water_x * cm, self.water_y * cm)
        # 设置字体格式与大小,中文需要加载能够显示中文的字体，否则就会乱码，注意字体路径
        try:
            reportlab.pdfbase.pdfmetrics.registerFont(
                reportlab.pdfbase.ttfonts.TTFont('STHeiti', self.font_path))
            c.setFont('STHeiti', self.water_font_size)
        except:
            # 默认字体，只能够显示英文
            print("沒有找到中文字體:STHeiti")
            c.setFont("Helvetica", self.water_font_size)
            # content = "watermark"
    
        # 旋转角度度,坐标系被旋转
        c.rotate(self.water_r)

        # 指定填充颜色
        c.setFillColorRGB(0, 0, 0)

        # 设置透明度,1为不透明
        c.setFillAlpha(self.water_trans)

        # 画几个文本,注意坐标系旋转的影响
        c.drawString(0 * cm, 3 * cm, content)

        # 关闭并保存pdf文件
        c.save()
        return file_name

    # 插入水印
    def add_watermark(self,pdf_file_in, pdf_file_mark, pdf_file_out):
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

        return True

  