import numpy as np
from PIL import Image
import math


def resize_image(resize_img, img_x, img_y, cols=1, rows=1):
    # 横向扩展图片到cols列
    img_multi_cols = resize_img
    for i in range(1, cols):
        img_multi_cols = np.concatenate((img_multi_cols, resize_img), axis=1)

    # 纵向扩展 横向扩展之后的图片到rows
    img_multi_rows = img_multi_cols
    for i in range(1, rows):
        img_multi_rows = np.concatenate((img_multi_rows, img_multi_cols))

    # 放缩到最大，与原图像贴合
    resize_img_x = img_multi_rows.shape[0]
    resize_img_y = img_multi_rows.shape[1]
    ret_img_x = img_x
    ret_img_y = img_y
    print("resize size from x=", resize_img_x, " y=", resize_img_y)
    print("resize size to x=", img_x, " y=", img_y)
    # print("transfer x = ", resize_img_x / img_x, " y = ", resize_img_y / img_y)
    if resize_img_x / img_x > resize_img_y / img_y:
        ret_img_x = img_x
        ret_img_y = math.floor(img_x * resize_img_y / resize_img_x)
    else:
        ret_img_x = math.floor(img_y * resize_img_x / resize_img_y)
        ret_img_y = img_y

    ret_img = Image.fromarray(img_multi_rows)
    resized_img = ret_img.resize((ret_img_y, ret_img_x), Image.ANTIALIAS)
    # print("resize size x=", ret_img_x, " y=", ret_img_y)
    ret_img_arr = np.array(resized_img, dtype=np.uint8)
    # 调整水印图片与输入的大小一致
    ret_img_arr = np.pad(ret_img_arr, ((0, img_x-ret_img_x), (0, img_y-ret_img_y)), mode='constant', constant_values=1)
    # print("resize arr size x=", ret_img_arr.shape[0], " y=", ret_img_arr.shape[1])
    return ret_img_arr
