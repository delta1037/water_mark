from PIL import Image
import numpy as np
from resize_image import resize_image

threshold = 200


def show_one_zero_map(one_zero_arr, out_put_name):
    one_zero_arr[one_zero_arr == 1] = 255
    t_output_img = Image.fromarray(one_zero_arr)
    t_output_img.save(out_put_name, "PNG")


# 合并并输出图像
def encode(src_img_path, water_mark_path, encode_cols=1, encode_rows=1, one_zero=1):
    water_mark_img = np.array((0, 0), dtype=np.uint8)
    src_img = np.array(Image.open(src_img_path), dtype=np.uint8)
    print("src_img_shape : ", src_img.shape)
    if one_zero == 1:
        water_mark_img = np.array(Image.open(water_mark_path).convert('1'), dtype=np.uint8)
    else:
        water_mark_img = np.array(Image.open(water_mark_path).convert('L'), dtype=np.uint8)
    print("water_mark_img shape : ", water_mark_img.shape)
    # print(water_mark_img)
    # show_one_zero_map(water_mark_img, 'water_one_zero.png')
    src_img_x = src_img.shape[0]
    src_img_y = src_img.shape[1]

    merge_img_src = resize_image(water_mark_img, src_img_x, src_img_y, encode_cols, encode_rows)
    print("resized img shape:", merge_img_src.shape)
    if merge_img_src.shape[0] > src_img_x or merge_img_src.shape[1] > src_img_y:
        # 重新定义后的水印图片应该小于目的图片的大小
        print("resize water mark error!!")
        exit(-1)

    # 清空原图像最后一位的信息，插入水印的值
    if one_zero == 1:
        src_img[:, :, 1] = (src_img[:, :, 1] & 0xfe) | (merge_img_src[:, :] & 0x1)
    else:
        src_img[:, :, 1] = (src_img[:, :, 1] & 0xfe) | ((merge_img_src[:, :] & 0x80) >> 7)
        src_img[:, :, 2] = (src_img[:, :, 2] & 0xfe) | ((merge_img_src[:, :] & 0x40) >> 6)
        src_img[:, :, 3] = (src_img[:, :, 3] & 0xfe) | ((merge_img_src[:, :] & 0x20) >> 5)
    output_img = Image.fromarray(src_img)
    return output_img


def decode(src_img_path, one_zero=1):
    src_img = np.array(Image.open(src_img_path), dtype=np.uint8)
    # 遍历src_img，取出最后一位
    gray_img = np.zeros((src_img.shape[0], src_img.shape[1]), dtype=np.uint8)
    if one_zero == 1:
        gray_img[:, :] = (src_img[:, :, 1] & 0x1)
        gray_img[gray_img == 1] = 255
        gray_img[gray_img == 0] = 0
    else:
        gray_img[:, :] = ((src_img[:, :, 1] & 0x1) << 7) + ((src_img[:, :, 2] & 0x1) << 6) \
                         + ((src_img[:, :, 3] & 0x1) << 5)

    output_img = Image.fromarray(gray_img)
    return output_img
