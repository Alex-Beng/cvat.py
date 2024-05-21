import win32gui
import win32ui
import win32api
import win32con
from win32gui import FindWindow

import numpy as np
import cv2


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
    
    def _get_scale():
        hwnd = win32gui.GetDesktopWindow()
        hmonitor = win32api.MonitorFromWindow(hwnd, win32con.MONITOR_DEFAULTTONEAREST)

        miex = win32api.GetMonitorInfo(hmonitor)
        logical_cx = miex['Monitor'][2] - miex['Monitor'][0]
        logical_cy = miex['Monitor'][3] - miex['Monitor'][1]

        dm = win32api.EnumDisplaySettings(miex['Device'], win32con.ENUM_CURRENT_SETTINGS)
        physical_cx = dm.PelsWidth
        physical_cy = dm.PelsHeight

        return physical_cx / logical_cx


class BitBltCapture(Capture):
    def __init__(self) -> None:
        super().__init__()

    def capture(self):
        gi_handle = self.hwnd
        gi_rect = win32gui.GetWindowRect(gi_handle)
        gi_client_rect = win32gui.GetClientRect(gi_handle)
        # print(gi_client_rect, gi_rect)
        
        scale = Capture._get_scale()
        gi_client_width = int(scale * (gi_client_rect[2] - gi_client_rect[0]))
        gi_client_height = int(scale * (gi_client_rect[3] - gi_client_rect[1]))
        # h_width = int(scale * (gi_rect[2] - gi_rect[0]))
        # h_height = int(scale * (gi_rect[3] - gi_rect[1]))
        
        # 获取dc
        # 需要获得client的dc而不是window的dc
        # gi_win_dc = win32gui.GetWindowDC(gi_handle)
        gi_win_dc = win32gui.GetDC(gi_handle)
        gi_mfc_dc = win32ui.CreateDCFromHandle(gi_win_dc)
        bitmap_dc = gi_mfc_dc.CreateCompatibleDC()

        bitmap = win32ui.CreateBitmap()
        bitmap.CreateCompatibleBitmap(gi_mfc_dc, gi_client_width, gi_client_height)
        bitmap_dc.SelectObject(bitmap)
        bitmap_dc.BitBlt((0, 0), (gi_client_width, gi_client_height), gi_mfc_dc, (0, 0), win32con.SRCCOPY)

        bmp_str = bitmap.GetBitmapBits(True)
        im = np.frombuffer(bmp_str, dtype='uint8')
        im.shape = (gi_client_height, gi_client_width, 4)

        # print(im.shape, gi_client_rect)

        bitmap_dc.DeleteDC()
        win32gui.DeleteObject(bitmap.GetHandle())
        return im



if __name__ == "__main__":
    capture = BitBltCapture()
    imdata = capture.capture()
    import cv2
    cv2.imshow("test", imdata)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    print(imdata.shape)