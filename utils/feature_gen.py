# 大概算重新造轮子吧，，
# 生成特征及序列化/反序列化
# 只关心提瓦特大陆的定位，其他先不管
# 直接使用 pickle 序列化，不关心体积，只要内存里一样就行

import re
import os
from typing import List

import cv2
import numpy as np

class ImagePyramid:
    def __init__(self, img):
        _width, _height = img.shape[:2]
        assert _width == _height
        
        self.ori_scale = _width
        # 主要看够不够大，不够大说明是未开放/海域
        self.interesting = _width > 256
        self.img = img
        self.pyramid = self._generate_pyramid()
    def _generate_pyramid(self):
        # 生成金字塔
        _py = {}
        _py[self.ori_scale] = self.img
        _width = self.ori_scale
        # 分别往上和往下
        # 全员nn
        while _width > 1:
            _width //= 2
            _py[_width * 2]
            _py[_width] = cv2.resize(_py[_width * 2], (_width, _width), interpolation=cv2.INTER_NEAREST)
        _width = self.ori_scale
        while _width < 2048:
            _width *= 2
            _py[_width] = cv2.resize(_py[_width // 2], (_width, _width), interpolation=cv2.INTER_NEAREST)
        return _py

def get_map_names(root_path: str):
    # 使用正则去匹配 UI_MapBack_{int}_{int}.png

    # patten = re.compile(r"UI_MapBack_(\d+)_(\d+).png")
    # int 可以为负数
    patten = re.compile(r"UI_MapBack_(-?\d+)_(-?\d+).png")
    map_names = []
    for file in os.listdir(root_path):
        if patten.match(file):
            # get the x, y
            x, y = patten.match(file).groups()
            map_names.append((file, int(x), int(y)))
        # else:
        #     print(f"Warning: {file} not match")
    return map_names

def get_maps_feat(map_pys: dict[tuple[int, int], ImagePyramid]):
    # 1. 直接最逆天的方法，获得8邻域，拼成 2048*3 x 2048*3
    # 2. 同时维护一个 2048*3 x 2048*3 的mask当lut，用于最后的特征过滤
    # 3. 特征提取
    # 4. 对pt进行过滤、坐标变换

    # get the x y range first
    xs = [x for x, y in map_pys.keys()]
    ys = [y for x, y in map_pys.keys()]
    x_min, x_max, y_min, y_max = xy_range(xs, ys)

    for x in range(x_min, x_max+1):
        for y in range(y_min, y_max+1):
            if (x, y) not in map_pys:
                continue

def comp_one_map_feat(map_pys: dict[tuple[int, int], ImagePyramid], x: int, y: int):
    dircs = [
        (1, 1), (1, 0), (1, -1),
        (0, 1), (0, 0), (0, -1),
        (-1, 1), (-1, 0), (-1, -1)
    ]

    big_neibor = np.zeros((2048*3, 2048*3, 3), dtype=np.uint8)
    big_mask = np.zeros((2048*3, 2048*3), dtype=np.uint8)
    for dirc in dircs:
        dx, dy = dirc
        nx, ny = x+dx, y+dy
        if (nx, ny) in map_pys:
            _img = map_pys[(nx, ny)].pyramid[2048]
            # 2048*2048
            _x = 2048 + x * 2048
            _y = 2048 + y * 2048
            big_neibor[_x:_x+2048, _y:_y+2048] = _img
            big_mask[_x:_x+2048, _y:_y+2048] = 1
    surf = cv2.xfeatures2d.SURF.create()
    surf_keypoints = surf.detect(big_neibor, big_mask)
    print(len(surf_keypoints))

    pass

def xy_range(xs, ys)-> List[int, int, int, int]:
    x_min = min(xs)
    x_max = max(xs)
    y_min = min(ys)
    y_max = max(ys)
    return x_min, x_max, y_min, y_max

def main():
    root_path = "./maps"
    # 用勾八金字塔，直接全员2048
    map_names = get_map_names(root_path)
    # read map images and inin the pyramid
    map_pyramids = {}
    for name, x, y in map_names:
        _path = os.path.join(root_path, name)
        _img = cv2.imread(_path)
        _img_py = ImagePyramid(_img)
        map_pyramids[(x, y)] = _img_py
    get_maps_feat(map_pyramids)


def old_main():
    root_path = "./maps"
    map_names = get_map_names(root_path)
    x_min = min(map_names, key=lambda x: x[1])[1]
    x_max = max(map_names, key=lambda x: x[1])[1]
    y_min = min(map_names, key=lambda x: x[2])[2]
    y_max = max(map_names, key=lambda x: x[2])[2]
    print(x_min, x_max, y_min, y_max)
    exit()
    for name, x, y in map_names:
        # read the image and print the size
        _path = os.path.join(root_path, name)
        img = cv2.imread(_path)
        # 只有 2048/1024 or 128及更小的尺寸
        if img.shape[0] > 256:
            print(_path, x, y, img.shape)
            cv2.imshow("test", img)
            cv2.waitKey(1)
            continue
        method = cv2.INTER_LINEAR
        if x == 0 and y == 1:
            # print(_path, x, y, img.shape)
            # resize to 2028 and save it
            img_res = cv2.resize(img, (2048, 2048), interpolation=method)
            cv2.imwrite("test01l.png", img_res)
        if x == 0 and y == 2:
            print(_path, x, y, img.shape)
            img_res = cv2.resize(img, (2048, 2048), interpolation=method)
            cv2.imwrite("test02l.png", img_res)
            

        # if img.shape[0] == 2048:
        #     method = [
        #         cv2.INTER_NEAREST,
        #         cv2.INTER_LINEAR,
        #         cv2.INTER_CUBIC,
        #         cv2.INTER_AREA,
        #         cv2.INTER_LANCZOS4,
        #         cv2.INTER_LINEAR_EXACT            
        #     ]
        #     for i,m in enumerate(method):
        #         print(f"Method {i}: {m}")
        #         img_res = cv2.resize(img, (256, 256), interpolation=m)
        #         cv2.imwrite(f"test_{i}.png", img_res)
        #     cv2.imwrite("test.png", img)
        #     exit()
    print(len(map_names))

if __name__ == "__main__":
    # main()
    # exit()
    old_main()