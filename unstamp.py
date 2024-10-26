#!/usr/bin/env python3  
# -*- coding: utf-8 -*-  
"""  
pdf 文件去水印并裁切指定比例后重新合成pdf
"""

from itertools import product
import fitz
import os
from PIL import Image

pic_dir = "image/"
cut_ratios = {
    'top': 0.075,  # 上边裁切7.5%
    'bottom': 0.05,  # 下边裁切5%
    'left': 0,  # 左边裁切10%
    'right': 0  # 右边裁切10%
}


class pdf():

    # pdf 每一页转图片后去水印并裁切
    def test_remove_pdf(self):
        page_num = 0
        pdf_path = "pdf/潘.pdf"
        pdf = fitz.open(pdf_path)
        for page in pdf:
            rotate = int(0)
            zoom_x, zoom_y = 2,2
            trans = fitz.Matrix(zoom_x, zoom_y).prerotate(rotate)
            pixmap = page.get_pixmap(matrix=trans, alpha=False)

            # 去除水印（简单地将亮色像素设置为白色）
            for pos in product(range(pixmap.width), range(pixmap.height)):
                rgb = pixmap.pixel(pos[0], pos[1])
                if sum(rgb) >= 500:
                    pixmap.set_pixel(pos[0], pos[1], (255, 255, 255))

                    # 保存去除水印后的图片
            temp_img_path = f"{pic_dir}pdf_split_{page_num + 1}_temp.png"
            pixmap.pil_save(temp_img_path)

            # 加载图片以便裁切
            img = Image.open(temp_img_path)
            img_width, img_height = img.size

            # 计算裁切区域
            left = int(img_width * cut_ratios['left'])
            right = int(img_width * (1 - cut_ratios['right']))
            top = int(img_height * cut_ratios['top'])
            bottom = int(img_height * (1 - cut_ratios['bottom']))

            # 裁切图片
            cut_img = img.crop((left, top, right, bottom))

            # 保存裁切后的图片
            cut_img_path = f"{pic_dir}pdf_split_{page_num + 1}.png"
            cut_img.save(cut_img_path)

            # 删除临时图片
            os.remove(temp_img_path)

            print(f"第{page_num + 1}页水印去除并裁切完成")
            page_num += 1

            # 去水印并裁切的图片，重新合并成 pdf

    @staticmethod
    def test_natural_sort_key(s):
        import re
        return [int(text) if text.isdigit() else text.lower() for text in re.split('(\d+)', s)]

    def test_pic2pdf(self):
        pdf = fitz.open()
        img_files = sorted(os.listdir(pic_dir), key=self.test_natural_sort_key)

        for img in img_files:
            if not img.startswith("pdf_split_"):
                continue

            print("合并图片 " + img)
            img_path = os.path.join(pic_dir, img)
            imgdoc = fitz.open(img_path)
            pdfbytes = imgdoc.convert_to_pdf()
            imgpdf = fitz.open("pdf", pdfbytes)
            pdf.insert_pdf(imgpdf)

            # 在合并后删除原始图片文件（可选，确保合并成功后再删除）
            # 注意：这里可以选择在确认PDF合并无误后再手动或脚本方式删除图片
            # os.remove(img_path)  # 注释掉这一行，或者确保在PDF合并无误后再取消注释

        output_pdf_path = "pdf/unstamp_cut.pdf"
        pdf.save(output_pdf_path)
        pdf.close()

        # 在此处可以选择删除所有已合并的图片文件（确认PDF无误后）
        # for img in img_files:
        #     if img.startswith("pdf_split_"):
        #         os.remove(os.path.join(pic_dir, img))


if __name__ == "__main__":
    obj = pdf()
    obj.test_remove_pdf()
    obj.test_pic2pdf()

    # 清理图片文件（确认PDF无误后执行）
    # 注意：为了避免数据丢失，通常建议手动检查PDF后再删除图片
    for img in os.listdir(pic_dir):
        if img.startswith("pdf_split_"):
            os.remove(os.path.join(pic_dir, img))
