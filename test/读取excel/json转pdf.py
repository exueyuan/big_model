from fpdf import FPDF


class PDF(FPDF):
    def __init__(self):
        super().__init__()
        self.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf')
        ttc_file = './SourceHanSerif-VF.ttf.ttc'
        self.add_font('SourceHanSerif-VF.ttf', '', ttc_file, uni=True, index=0)
        self.set_font('SourceHanSerif-VF.ttf', '', 14)


def txt_to_pdf(txt_filename, pdf_filename):
    # 创建PDF对象
    pdf = PDF()
    pdf.add_page()

    # 打开并读取TXT文件内容
    with open(txt_filename, 'r', encoding='utf-8') as file:
        for line in file:
            pdf.cell(0, 10, txt=line, ln=True)

    # 保存PDF文件
    pdf.output(pdf_filename)


# 使用示例
txt_filename = 'data.json'  # 替换为你的TXT文件名
pdf_filename = 'output.pdf'  # 输出PDF文件名
txt_to_pdf(txt_filename, pdf_filename)

print(f'"{txt_filename}" has been successfully converted to "{pdf_filename}"')
