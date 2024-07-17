#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pdf 文件去水印
"""

from itertools import product
import fitz
import os


pic_dir = "image/"

class pdf():

    # pdf 每一页转图片后去水印
    def test_remove_pdf(self):
        page_num = 0
        pdf = fitz.open("pdf/mobile.pdf")
        for page in pdf:
            rotate = int(0)
            # 每个尺寸的缩放系数为2，这将为我们生成分辨率提高4倍的图像
            zoom_x, zoom_y = 2, 2
            trans = fitz.Matrix(zoom_x, zoom_y).prerotate(rotate)
            pixmap = page.get_pixmap(matrix=trans, alpha=False)
            for pos in product(range(pixmap.width), range(pixmap.height)):
                rgb = pixmap.pixel(pos[0], pos[1])
                if (sum(rgb) >= 570):
                    pixmap.set_pixel(pos[0], pos[1], (255, 255, 255))
            pixmap.pil_save(f"{pic_dir}pdf_split_{page_num+1}.png")
            print(f"第{page_num+1}页水印去除完成")
            page_num = page_num + 1


    # 去水印的图片，重新合并成 pdf
    @staticmethod
    def test_natural_sort_key(s):
        """自定义排序键，用于自然排序文件名中的数字"""
        import re
        return [int(text) if text.isdigit() else text.lower() for text in re.split('(\d+)', s)]

    def test_pic2pdf(self):
        pdf = fitz.open()
        img_files = sorted(os.listdir(pic_dir), key=self.test_natural_sort_key)

        for img in img_files:
            if not img.startswith("pdf_split_"):
                continue

            print("合并图片 " + img)
            imgdoc = fitz.open(pic_dir + img)
            pdfbytes = imgdoc.convert_to_pdf()
            imgpdf = fitz.open("pdf", pdfbytes)
            pdf.insert_pdf(imgpdf)
        pdf.save("pdf/unstamp.pdf")
        pdf.close()


if __name__ == "__main__":
    obj=pdf()
    obj.test_remove_pdf()
    obj.test_pic2pdf()
