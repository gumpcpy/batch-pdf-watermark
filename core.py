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
        self.output_dir = thePath['output_dir']
            
        return

    # 创建水印信息
    def create_watermark(self, content):
        """根據水印內容產生水印PDF，並存到 output_dir，回傳完整路徑"""
        # 取得原始PDF檔名（不含副檔名）
        pdf_base = os.path.splitext(os.path.basename(self.pdf_path))[0]
        # 新檔名：原檔名_水印內容.pdf
        mark_pdf_name = f"{pdf_base}_{content}.pdf"
        # 組合完整路徑
        mark_pdf_path = os.path.join(self.output_dir, mark_pdf_name)

        # 確保 output_dir 存在
        os.makedirs(self.output_dir, exist_ok=True)

        # 頁面大小
        from reportlab.pdfgen import canvas
        from reportlab.lib.units import cm
        c = canvas.Canvas(mark_pdf_path, pagesize=(30 * cm, 30 * cm))
        c.translate(self.water_x * cm, self.water_y * cm)
        try:
            import reportlab.pdfbase.pdfmetrics
            import reportlab.pdfbase.ttfonts
            reportlab.pdfbase.pdfmetrics.registerFont(
                reportlab.pdfbase.ttfonts.TTFont('STHeiti', self.font_path))
            c.setFont('STHeiti', self.water_font_size)
        except:
            print("沒有找到中文字體:STHeiti")
            c.setFont("Helvetica", self.water_font_size)
        c.rotate(self.water_r)
        c.setFillColorRGB(0, 0, 0)
        c.setFillAlpha(self.water_trans)
        c.drawString(0 * cm, 3 * cm, content)
        c.save()
        return mark_pdf_path

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

  
if __name__ == "__main__":
    # 預設參數
    params = {
        'txt_path': 'TEST/name.txt',           # 預設的名字檔案
        'pdf_path': 'TEST/sample.pdf',          # 預設的 PDF 檔案
        'font_path': 'STHeiti.ttc', # 預設字體路徑
        'water_x': 5,                     # 水印 X 座標
        'water_y': 5,                     # 水印 Y 座標
        'water_r': 30,                    # 水印旋轉角度
        'water_font_size': 100,           # 水印字體大小
        'water_trans': 50,                 # 水印透明度 (百分比)
        'output_dir': 'TEST/output',  # 新增：目的地資料夾
    }

    # 建立 WatermarkCore 實例
    wm = WatermarkCore(**params)

    # 讀取名字檔案
    with open(params['txt_path'], 'r', encoding='utf-8') as f:
        names = [line.strip() for line in f if line.strip()]

    # 對每個名字產生水印並加到 PDF
    for name in names:
        mark_pdf = wm.create_watermark(name)
        # out_pdf 路徑同理組合
        pdf_base = os.path.splitext(os.path.basename(params['pdf_path']))[0]
        output_pdf_name = f"{pdf_base}_{name}.pdf"
        output_pdf_path = os.path.join(params['output_dir'], output_pdf_name)
        wm.add_watermark(params['pdf_path'], mark_pdf, output_pdf_path)
        print(f"已產生: {output_pdf_path}")