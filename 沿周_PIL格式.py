import cv2
import numpy as np
from PIL import ImageFont, ImageDraw, Image
import math
import MouseMinWidth

# mx = 0
# my = 0
# radius0 = 81
# radius1 = 102
# lcx = 124
# lcy = 198
# lcenter = (lcx, lcy)  # 左圆心
# rcx = 1142
# rcy = 198
# rcenter = (rcx, rcy)  # 右圆心
# piancha=0
# #读取图片文件
# img = cv2.imread("mskover.png")
# xiaoup = cv2.imread("maskup.png")
# xiaoleft = cv2.imread("maskleft.png")
#
# xiaodown = cv2.imread("maskdown.png")
# xiaoright = cv2.imread("maskright.png")
# maskleft = cv2.imread("mmaskleft.png")
# maskright = cv2.imread("mmaskright.png")
########################################################
# radius0 = 82
# radius1 = 102
# lcx = 103
# lcy = 150
# lcenter = (lcx, lcy)  # 左圆心
# rcx = 1022
# rcy = 150
radius0 = 86
radius1 = 104
lcx = 106
lcy = 150
lcenter = (lcx, lcy)  # 左圆心
rcx = 1017
rcy = 150
rcenter = (rcx, rcy)  # 右圆心
piancha = 0
# 微调高度，注意y轴正方向
trim_up = -5
trim_upup = -10
weitiaoleft=-8
img = cv2.imread("result_gray.png")
xiaoup = cv2.imread("cut2.png")
xiaoleft = cv2.imread("cut1.png")
xiaodown = cv2.imread("cut4.png")
xiaoright = cv2.imread("cut3.png")
maskleft = cv2.imread("cad_cut_1.png")
maskright = cv2.imread("cad_cut_3.png")
print(xiaoleft.shape)

# 获取图像尺寸
# height, width, channels = img.shape
img_copy = img.copy()  # 保存原始图片的副本


# print(img.shape)


def get_cercle(cx, cy):
    angle_rad = math.atan2(cy - my, mx - cx)
    if angle_rad >= 0:
        angle_rad1 = angle_rad
    else:
        angle_rad1 = angle_rad + 2 * 3.1415926
    # 就用弧度算，不需要转角度
    y2 = int(cy - (radius1 * math.sin(angle_rad1)))
    x2 = int(cx + (radius1 * math.cos(angle_rad1)))
    y1 = int(cy - (radius0 * math.sin(angle_rad1)))
    x1 = int(cx + (radius0 * math.cos(angle_rad1)))
    return x1, y1, x2, y2


def get_mouse_pos(event, x, y, flags, param):
    global mx, my, img, y2, x2, y1, x1, flag, width

    # 大图坐标转小图
    if event == cv2.EVENT_MOUSEMOVE:

        mx, my = x, y

        img_draw = img_copy.copy()
        print("鼠标坐标：", (x, y))
        angle_rad = 0
        # 把左右圆心标注出来
        img_draw[lcy - 1:lcy + 1, lcx - 1:lcx + 1] = [255, 255, 255]
        img_draw[rcy - 1:rcy + 1, rcx - 1:rcx + 1] = [255, 255, 255]
        # 设置需要显示的字体
        fontpath = "font/simsun.ttc"
        font1 = ImageFont.truetype(fontpath, 20)
        img_pil = Image.fromarray(img_draw)
        draw = ImageDraw.Draw(img_pil)
        # # # 绘制文字信息

        # 计算左侧半圆弧度值
        if lcx >= mx >= 0:
            x1, y1, x2, y2 = get_cercle(lcx, lcy)
            # 大图坐标转小图坐标，调用亿力的函数
            # try:
            flag, width = MouseMinWidth.MouseMinWidthInRing(x2 - (lcx - radius1), y2 - (lcy - radius1) + piancha,
                                                            x1 - (lcx - radius1), y1 - (lcy - radius1) + piancha,
                                                            xiaoleft, maskleft)
            # except Exception as result:
            #     print(result)
        # 计算中间上部条形
        if lcx < mx < rcx and 0 < my <= rcy:
            x1 = x2 = mx
            y1 = lcy - radius1
            y2 = lcy - radius0
            # 大图坐标转小图坐标，调用亿力的函数
            xx = x1 - lcx
            flag, width = MouseMinWidth.MouseMinWidthInLine(xx, xiaoup)
        # 计算中间下部条形
        if lcx < mx < rcx and my > rcy:
            x1 = x2 = mx
            y1 = lcy + radius1 + piancha
            y2 = lcy + radius0 + piancha
            # 大图坐标转小图坐标，调用亿力的函数
            xx = x1 - lcx
            flag, width = MouseMinWidth.MouseMinWidthInLine(xx, xiaodown)
        # 计算右侧半圆弧度值
        if mx >= rcx:
            x1, y1, x2, y2 = get_cercle(rcx, rcy)
            # 大图坐标转小图坐标，调用亿力的函数
            flag, width = MouseMinWidth.MouseMinWidthInRing(x2 - rcx, y2 - (lcy - radius1) + piancha, x1 - rcx,
                                                            y1 - (lcy - radius1) + piancha, xiaoright, maskright)

        # 画线
        # cv2.line(img_draw, (x1, y1), (x2, y2), (0, 255, 0), 3)
        draw.line([(x1, y1), (x2, y2)], fill=(0, 255, 0), width=3)

        # 在图片上添加文本
        font = cv2.FONT_HERSHEY_SIMPLEX  # 字体类型
        text0 = '是否合格:'  # flag

        # print(type(text0))
        # text0.encode("GBK").decode("UTF-8", errors="ignore")
        text1 = str(flag)  # flag
        text2 = str(width)  # 一条线上有几个合格
        text3 = "最小焊缝宽度:"

        color = (255, 255, 255)  # BGR 格式颜色
        if flag == False:
            color1 = (0, 0, 255)
        else:
            color1 = color
        # thickness = 1  # 粗细
        # font_scale = 0.8  # 字体大小
        # text_size0, _ = cv2.getTextSize(text0, font, font_scale, thickness)
        # text_size1, _ = cv2.getTextSize(text1, font, font_scale, thickness)
        # text_size2, _ = cv2.getTextSize(text2, font, font_scale, thickness)
        # text_size3, _ = cv2.getTextSize(text3, font, font_scale, thickness)

        # text_size[0] text长度，text_size[1] text高度
        w0, h0 = font1.getsize(text0)
        w1, h1 = font1.getsize(text1)
        w2, h2 = font1.getsize(text2)
        w3, h3 = font1.getsize(text3)
        # 写字上部
        if 0 < my <= rcy:
            # 写字，右侧半圆上部
            if mx >= rcx:
                if w2 + x2 > width - rcx:
                    # 第一个汉字语句
                    draw.text((x1 - w2 - w3+weitiaoleft, y1 + h2), text0, font=font1
                              , fill=color
                              )
                    # 数据1
                    draw.text((x1 - w2 - w1, y1 + h2), text1, font=font1, fill=color1
                              )
                    # 数据2
                    draw.text((x1 - w2+weitiaoleft, y1 + 2 * h2), text2, font=font1, fill=color
                              )
                    # 第二个汉字语句
                    draw.text((x1 - w2 - w3+weitiaoleft, y1 + 2 * h2), text3, font=font1
                              , fill=color
                              )
            # 写字，左侧半圆上部
            if mx <= lcx:
                # if w2 + w3 > x2:
                draw.text((x1, y1 + h2), text0, font=font1, fill=color
                          )
                draw.text((x1 + w0, y1 + h2), text1, font=font1, fill=color1
                          )
                draw.text((x1 + w3, y1 + 2 * h2), text2, font=font1, fill=color
                          )
                draw.text((x1, y1 + 2 * h2), text3, font=font1, fill=color
                          )
            # draw.text((x1, y1 + h2), text0, font=font1, fill=color
            #           )
            # draw.text((x1 + w0, y1 + h2), text1, font=font1, fill=color
            #           )
            # draw.text((x1 + w3, y1 + 2 * h2), text2, font=font1, fill=color
            #           )
            # draw.text((x1, y1 + 2 * h2), text3, font=font1, fill=color
            #           )

            # 写字，中间条形上部
            if lcx < mx < rcx:
                draw.text((x1 - w3, y1 - h2 - h1 + trim_upup), text0, font=font1,
                          fill=color)

                draw.text((x1 - w1, y1 - h2 - h1 + trim_upup), text1, font=font1, fill=color1)
                draw.text((x1, y1 - h2 + trim_up), text2, font=font1, fill=color)
                draw.text((x1 - w3, y1 - h2 + trim_up), text3, font=font1, fill=color)
        else:
            # 写字，右侧半圆下部
            if mx >= rcx:
                # if  w2 + x2 > width:
                draw.text((x1 - w2 - w3+weitiaoleft, y1 - h2 - h3), text0, font=font1,
                          fill=color
                          )
                draw.text((x1 - w2 - w1, y1 - h2 - h3), text1, font=font1, fill=color1
                          )
                draw.text((x1 - w2+weitiaoleft, y1 - h2), text2, font=font1, fill=color
                          )
                draw.text((x1 - w2 - w3+weitiaoleft, y1 - h2), text3, font=font1, fill=color
                          )
                # else:
                #  draw.text(img_draw, text1, (x1 -  w2, y1 - h2), font,    ,fill=color,
                #               )
                #  draw.text(img_draw, text2, (x1 -  w2, y1), font,    ,fill=color,
                #               )
            # 写字，左侧半圆下部
            if mx <= lcx:
                if w2 + w3 > x2:
                    draw.text((x1, y1 - h3 - h2), text0, font=font1, fill=color
                              )
                    draw.text((x1 + w0, y1 - h3 - h2), text1, font=font1, fill=color1
                              )
                    draw.text((x1 + w3, y1 - h3), text2, font=font1, fill=color
                              )
                    draw.text((x1, y1 - h3), text3, font=font1, fill=color
                              )

            # 写字，中间条形下部,分成三部分
            # 左
            if lcx + w3 > mx > lcx:
                draw.text((x1, y2 - h2 - h1 + trim_upup), text0, font=font1, fill=color
                          )
                draw.text((x1 + w0, y2 - h2 - h1 + trim_upup), text1, font=font1,
                          fill=color1,
                          )
                draw.text((x1 + w3, y2 - h2 + trim_up), text2, font=font1, fill=color)
                draw.text((x1, y2 - h2 + trim_up), text3, font=font1, fill=color)
            # 中间
            if lcx + w3 <= mx <= rcx - w2:
                draw.text((x1 - w3, y2 - h2 - h1 + trim_upup), text0, font=font1,
                          fill=color
                          )
                draw.text((x1 - w1, y2 - h2 - h1 + trim_upup), text1, font=font1, fill=color1)
                draw.text((x1, y2 - h2 + trim_up), text2, font=font1, fill=color)
                draw.text((x1 - w3, y2 - h2 + trim_up), text3, font=font1, fill=color)
            # 右侧
            if rcx - w2 < mx < rcx:
                draw.text((x1 - w2 - w3, y2 - h2 - h1 + trim_upup), text0, font=font1
                          ,
                          fill=color
                          )
                draw.text((x1 - w2 - w1, y2 - h2 - h1 + trim_upup), text1, font=font1,
                          fill=color1
                          )
                draw.text((x1 - w2, y2 - h2 + trim_up), text2, font=font1, fill=color
                          )
                draw.text((x1 - w2 - w3, y2 - h2 + trim_up), text3, font=font1,
                          fill=color
                          )

        # 显示更新后的图像
        # cv2.imshow("image", img_draw)
        img1 = np.array(img_pil)

        # 在窗口中展示图片
        cv2.imshow('image', img1)
        # cv2.imshow("image", img1)


# cv2.namedWindow('image',cv2.WND_PROP_FULLSCREEN)
# cv2.setWindowProperty('image', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
# cv2.resizeWindow("image", img.shape[1], img.shape[0])  # 设置窗口大小
# cv2.moveWindow("image",200,200)

# # 初始化显示窗口
# cv2.namedWindow("image", cv2.WINDOW_NORMAL)
cv2.namedWindow("image")
# 绑定鼠标事件处理函数
cv2.setMouseCallback("image", get_mouse_pos)
"""
取消边框（上标题栏）的方法
1.cv2.namedWindow('image',cv2.WND_PROP_FULLSCREEN)  创建窗口
    
2.设置窗口参数
    将图片改为全屏
    C++版：
    CV_WINDOW_NORMAL          = 0x000000000   // 将窗口更改为正常大小或使窗口可调整大小
    CV_WINDOW_AUTOSIZE        =  0x00000001   // 通过显示的图像约束大，窗口不能调整大小
    CV_WINDOW_FULLSCREEN  =  1                     // 将窗口更改为全屏
    CV_WINDOW_FREERATIO      =  0x00000100   // 图像尽可能地扩展(没有比例约束)
    CV_WINDOW_KEEPRATIO      =  0x00000000    // 使窗口可调整大小，但保留显示图像的比例
    
    cv2.setWindowProperty()函数可以用来设置窗口属性，其中第一个参数是窗口名称，第二个参数是要设置的属性，第三个参数是属性值。
    在这个代码中，第二个参数使用了常量cv2.WND_PROP_FULLSCREEN，表示需要设置窗口的全屏属性。
    因为我们需要将窗口全屏，所以第三个参数是cv2.WINDOW_FULLSCREEN，表示将窗口设置为真正的全屏，不显示边框和标题栏等内容。
    cv2.setWindowProperty('image', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
3.# 设置窗口大小
    cv2.resizeWindow("image", img.shape[1], img.shape[0])  # 设置窗口大小
4.确定生成窗口位置
    cv2.moveWindow("image",50,500)
"""

# 在窗口中展示图片

# cv2.imshow("image", img)

cv2.waitKey(0)

# 释放窗口资源
cv2.destroyAllWindows()
