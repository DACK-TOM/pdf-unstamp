RGB测试

1. 图片转为无压缩bmp格式
python3 -m unittest rgb.TestRGB.test_pic2bmp 

2. 图片RGB通道分离
python3 -m unittest rgb.TestRGB.test_split_rgb

3. 获取图片RGB值
python3 -m unittest rgb.TestRGB.test_get_rgb

—-----------------------------------------------------------

PDF去水印

1. PDF每一页转图片后去水印
python3 -m unittest unstamp.TestUnstamp.test_remove_pdf

2. 去水印后图片重新合成PDF
python3 -m unittest unstamp.TestUnstamp.test_pic2pdf


修改bug
合并pdf时，按照1，10，11，12，，，，2,20,21,22,23,24，，，错误顺序
改变函数调用方式，更符合个人习惯（主观）
