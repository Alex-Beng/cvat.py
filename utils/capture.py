# 1. video/image capture
# 2. bitblt capture
# 3. directx capture (low priority)

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


# TODO: 兼容视频和图片流
class Capture:
    def _get_hwnd(self) -> None:
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
        self._get_hwnd()

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
    import time
    from matplotlib import pyplot as plt
    time_sum = 0
    time_cnt = 0
    times = []
    while True:
        beg_t = time.time()
        imdata = capture.capture()
        end_t = time.time()
        import cv2
        cv2.imshow("test", imdata)
        k = cv2.waitKey(1)
        times.append(1/(end_t-beg_t))
        time_sum += (end_t - beg_t)
        time_cnt += 1
        print(f'\r{1/(end_t-beg_t):.2f}', end='')
        if k == ord('q'):
            break
    cv2.destroyAllWindows()
        
    print(f'\n{time_sum}')
    print(f'\n{time_cnt}')
    print(f'\n{time_cnt/time_sum:.2f}')
    plt.plot(times)
    plt.show()
    
