import json

import cv2
import numpy as np
from numpy import fromfile

from DeskPageV2.DeskTools.WindowsSoft.findOcr import FindPicOCR
from DeskPageV2.DeskTools.WindowsSoft.get_windows import find_pic, find_area
from DeskPageV2.Utils.load_res import GetConfig


def bitwise_and(image: np.ndarray, mask_position: tuple):
    """
    给图片加个掩膜遮罩，避免干扰。保留目标区域，其他的区域都遮住
    :param image: 图片
    :param mask_position: # 指定掩膜位置（左上角坐标， 右下角坐标） mask_position = (50, 50, 200, 200)
    """
    if image is not None:
        # print(image.shape[0], image.shape[1])
        # 绘制掩膜（矩形）
        # 参数分别为：图像、矩形左上角坐标、矩形右下角坐标、颜色（BGR）、线条粗细
        # cv2.rectangle(image, mask_position[0:2], mask_position[2:4], (0, 255, 0), -1)  # 遮住目标区域
        # 遮住左侧
        image = cv2.rectangle(image, [0, 0], [mask_position[0], image.shape[1]], (0, 255, 0), -1)
        # 遮住右侧
        image = cv2.rectangle(image, [mask_position[2], 0], [image.shape[1], image.shape[0]], (0, 255, 0), -1)
        # 遮住上面
        image = cv2.rectangle(image, [0, 0], [image.shape[1], mask_position[1]], (0, 255, 0), -1)
        # 遮住下面
        image = cv2.rectangle(image, [0, mask_position[3]], [image.shape[1], image.shape[0]], (0, 255, 0), -1)
    return image


class ChengYuInput:

    def __init__(self):
        self.__f = FindPicOCR()
        __chengyu_pic = GetConfig().get_chengyu_pic()

        self.chengyu_pic_up_move = cv2.imdecode(fromfile(__chengyu_pic.up_move, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
        self.chengyu_pic_down_move = cv2.imdecode(fromfile(__chengyu_pic.down_move, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
        self.chengyu_pic_unlock = cv2.imdecode(fromfile(__chengyu_pic.unlock, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
        self.chengyu_pic_l_r_tag = cv2.imdecode(fromfile(__chengyu_pic.l_r_tag, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
        self.chengyu_pic_file_json = __chengyu_pic.idiom

        self._chengyu_json_load: list = []

    @staticmethod
    def less_str_chengyu(str_list) -> list:
        """
        由于OCR识别精度的问题，导致部分词语识别失败，所以会产生确实。这里可以补充一下
        """
        less_chengyu: list = [
            (['纷', '至', '来'], '沓'),
            (['莫', '衷', '是'], '一'),
            (['老', '奸', '巨'], '猾'),
            (['患', '难', '与'], '共')
        ]
        for chengyu_str in less_chengyu:
            if set(list(chengyu_str[0])).issubset(str_list) is True:
                if chengyu_str[1] not in str_list:
                    str_list.append(chengyu_str[1])
        return str_list

    def __get_chengyu_string_key(self, image: np.ndarray):
        """
        识别游戏画面中出现的成语文字
        """

        res_up = find_area(self.chengyu_pic_up_move, image)
        res_down = find_area(self.chengyu_pic_down_move, image)
        res_l_r = find_pic(self.chengyu_pic_l_r_tag, image)
        res_unlock = find_area(self.chengyu_pic_unlock, image)

        res_up_x, res_up_y, res_down_x, res_down_y, res_unlock_x, res_unlock_y, res_left_x, res_right_x = 0, 0, 0, 0, 0, 0, 0, 0

        if res_up[-1] > 0:
            # 如果找到了 上 的图标
            res_up_x, res_up_y = res_up[0][0], res_up[0][1]
        if res_down[-1] > 0:
            # 找到 下 的图标
            res_down_x, res_down_y = res_down[0][0], res_down[0][1]
        if res_unlock[-1] > 0:
            # 找到尝试解锁的按钮
            res_unlock_x, res_unlock_y = res_unlock[2][0], res_unlock[2][1]
        if len(res_l_r) > 0:
            x_list: list = []
            for pos in res_l_r:
                x_list.append(pos[0])
            res_left_x = min(x_list)
            res_right_x = max(x_list)

        # 拼接一下坐标,上部分
        _chengyu_pos_up_x, _chengyu_pos_up_y = int(res_left_x), int(res_up_y)
        _chengyu_pos_down_x, _chengyu_pos_down_y = int(res_unlock_x), int(res_unlock_y)

        up_pic = bitwise_and(image, (_chengyu_pos_up_x, _chengyu_pos_up_y, _chengyu_pos_down_x, _chengyu_pos_down_y))

        # cv2.imshow("s", up_pic)
        # cv2.waitKey()

        res = FindPicOCR().find_ocr_all(up_pic)
        # print(res)
        # 过滤一下，上半部分和下半部分,区分的坐标是 down_tag的坐标

        up_str_list: list = []
        down_str_list: list = []

        for res_str in res:
            if res_str is None:
                continue
            res_ocr_text = res_str.ocr_text
            # 识别异常的文字，先慢慢累积
            if "知口" == res_ocr_text:
                res_ocr_text = '知'

            if len(res_ocr_text) > 1:
                continue

            if 'o' in res_ocr_text:
                continue

            res_y = res_str.box[0][1]
            if res_y <= res_down_y:
                up_str_list.append(res_ocr_text)
            else:
                down_str_list.append(res_ocr_text)
        print(f"上部分:{up_str_list}, \n下部分:{down_str_list}")
        return up_str_list, down_str_list

    def check_chengyu(self, image: np.ndarray) -> list:
        """
        拼接成语
        """
        if len(self._chengyu_json_load) == 0:
            with open(self.chengyu_pic_file_json, "r", encoding='UTF-8') as f:
                data = json.load(f)

                for dict_key in data:
                    self._chengyu_json_load.append(dict_key.get("word"))

        up_str, down_str = self.__get_chengyu_string_key(image)

        _key_input = up_str
        _key_wait = down_str

        new_list: list = _key_wait + _key_input

        new_list = self.less_str_chengyu(new_list)

        result_list: list = []
        for chengyu_str in self._chengyu_json_load:
            str_result_sum: int = 0
            for chengyu_len_str in chengyu_str:
                if chengyu_len_str in new_list:
                    str_result_sum += 1
            if len(chengyu_str) > 4:
                continue
            if str_result_sum == 4:
                # 4字成语
                # print(f"当前有成语 {chengyu_str} 符合条件")
                # 好了，初步过滤出来后，再精确过滤一遍
                # 每个成语中必须保持上下2个数据都有字符出现，并且每个字符只出现一次
                res_up_list = []
                res_down_list = []
                for chengyu_result_key in chengyu_str:
                    if chengyu_result_key in _key_input:
                        res_up_list.append(chengyu_result_key)
                    elif chengyu_result_key in _key_wait:
                        res_down_list.append(chengyu_result_key)
                if min(len(res_up_list), len(res_down_list)) > 0:
                    # print(f"当前有成语 {chengyu_str} 符合条件")
                    result_list.append(chengyu_str)

        return result_list


if __name__ == '__main__':
    o_pic = cv2.imread('D:\\SoftWare\\Game\\SnailGames\\JiuDancing\\JiuYinScreenPic\\20_59\\20_59_15.png')
    ChengYuInput().check_chengyu(o_pic)