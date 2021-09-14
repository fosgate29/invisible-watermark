import cv2
from imwatermark import WatermarkEncoder
from imwatermark import WatermarkDecoder


bgr = cv2.imread('original.jpg')
wm = 'test'

encoder = WatermarkEncoder()
encoder.set_watermark('bytes', wm.encode('utf-8'))
bgr_encoded = encoder.encode(bgr, 'dwtDct')

cv2.imwrite('test_wm.png', bgr_encoded)

bgr = cv2.imread('test_wm.png')

length = encoder.get_length()
decoder = WatermarkDecoder('bytes', length)

watermark = decoder.decode(bgr, 'dwtDct')
print(watermark.decode('utf-8'))
