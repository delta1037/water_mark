from gray_water_mark import encode, decode

# 前期考虑黑白图像的数字水印
# 后期考虑彩色图像的数字水印
output_img = encode('./src_img.png', './water_mark.png', 1, 1, 0)
output_img.save('output.png', "PNG")

decode_img = decode('output.png', 0)
decode_img.save('decode_result.png', "PNG")
