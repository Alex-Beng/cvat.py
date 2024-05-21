# program entrance for Filter-based Location Estimation

# 1. 截屏
# 2. 各个位置估计方法
# 3. 在这个文件中组装各个模块，异步处理

import asyncio

cap_queue = asyncio.Queue()
mini_map_queue = asyncio.Queue()

async def capture_warp():
    from utils.capture import BitBltCapture
    capture = BitBltCapture()

    while True:
        cap_queue.put_nowait(capture.capture())
        await asyncio.sleep(0.001)

async def odemeter_warp():
    pass

async def template_loc_warp():
    pass

async def feature_loc_warp():
    pass

async def main():
    # do the KF and plot in the main loop
    pass

if __name__ == "__main__":
    asyncio.run(main())
