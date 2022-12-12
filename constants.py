WIDTH, HEIGHT = 1072, 667+83
try:
    import win32api
    FRAMERATE = win32api.EnumDisplaySettings(win32api.EnumDisplayDevices().DeviceName, -1).DisplayFrequency
except ModuleNotFoundError:
    print("win32api module not found! install it with pip install pywin32")
    FRAMERATE = 60
