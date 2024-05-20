import win32gui
import win32ui
import win32con
from win32gui import FindWindow

import numpy as np


def _find_window_local():
    class_name = "UnityWndClass"
    window_name = "原神"
    hwnd = FindWindow(class_name, window_name)
    return hwnd


# 基类，负责Hwnd的获取
class Capture:
    def __init__(self) -> None:
        self.hwnd = _find_window_local()
        if self.hwnd == 0:
            raise ValueError("未找到窗口")
        

class BitBltCapture(Capture):
    def __init__(self) -> None:
        super().__init__()

    def capture(self):
        hwnd = self.hwnd

        # 获取窗口的设备上下文
        hwndDC = win32gui.GetWindowDC(hwnd)
        mfcDC = win32ui.CreateDCFromHandle(hwndDC)
        saveDC = mfcDC.CreateCompatibleDC()

        # 获取窗口的大小
        left, top, right, bot = win32gui.GetClientRect(hwnd)
        width = right - left
        height = bot - top

        # 创建一个位图来存储捕获内容
        saveBitMap = win32ui.CreateBitmap()
        saveBitMap.CreateCompatibleBitmap(mfcDC, width, height)
        saveDC.SelectObject(saveBitMap)

        # 使用BitBlt捕获窗口图像
        result = saveDC.BitBlt((0, 0), (width, height), mfcDC, (0, 0), win32con.SRCCOPY)

        # 将捕获的图像转换为numpy数组
        bmpinfo = saveBitMap.GetInfo()
        bmpstr = saveBitMap.GetBitmapBits(True)
        imdata = np.frombuffer(bmpstr, dtype='uint8')
        imdata.shape = (height, width, 4)

        # 清理资源
        win32gui.DeleteObject(saveBitMap.GetHandle())
        saveDC.DeleteDC()
        mfcDC.DeleteDC()
        win32gui.ReleaseDC(hwnd, hwndDC)

        # 返回numpy数组
        return imdata

if __name__ == "__main__":
    capture = BitBltCapture()
    imdata = capture.capture()
    import cv2
    cv2.imshow("test", imdata)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    print(imdata.shape)