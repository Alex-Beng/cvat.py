# test surf and draw

import cv2
import numpy as np

img = cv2.imread("maps/UI_MapBack_-1_-1.png")
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
surf = cv2.xfeatures2d.SURF.create()
surf_keypoints, surf_des = surf.detectAndCompute(img_gray, None)
print(len(surf_keypoints))
img_keypoints = cv2.drawKeypoints(img, surf_keypoints, None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
img_onlykp = cv2.drawKeypoints(img, surf_keypoints, None, flags=cv2.DRAW_MATCHES_FLAGS_NOT_DRAW_SINGLE_POINTS)
cv2.imshow("surf", img_keypoints)
cv2.imshow("surf_onlykp", img_onlykp)


# 变为使用分块双阈值的方式
# 128x128 -> 取 384x384 领域

dircs = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1), (0, 0), (0, 1),
    (1, -1), (1, 0), (1, 1)
]
L = 128

row, col = img_gray.shape
print(row, col)

for rb in range(0, row, L):
    for cb in range(0, col, L):
        img_block = img_gray[rb:rb+L, cb:cb+L]
        surf_keypoints, surf_des = surf.detectAndCompute(img_block, None)
        for kp in surf_keypoints:
            kp.pt = (kp.pt[0] + cb, kp.pt[1] + rb)
        img_block_keypoints = cv2.drawKeypoints(img, surf_keypoints, None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        img_block_onlykp = cv2.drawKeypoints(img, surf_keypoints, None, flags=cv2.DRAW_MATCHES_FLAGS_NOT_DRAW_SINGLE_POINTS)
        cv2.imshow("block", img_block_keypoints)
        cv2.imshow("block_onlykp", img_block_onlykp)
        cv2.waitKey(0)


cv2.waitKey(0)

