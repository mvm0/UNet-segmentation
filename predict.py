import PIL
import cv2
import numpy as np
import model as m


# Предсказание нейронной сети
def predictMask(pilImage=None):
    if pilImage != None:
        model = m.vgg16_encoder_unet(input_shape=(512, 512, 3))
        # unet256 - обучение на картинках 256x256 (~50 эпох)
        # unet512 - обучение на картинках 512x512 (65 эпох)
        model.load_weights('unet512.h5')

        openCVImage = np.array(pilImage)
        h, w, _ = openCVImage.shape
        openCVImage = cv2.resize(openCVImage, (512, 512), interpolation=cv2.INTER_AREA)
        openCVImage = cv2.cvtColor(openCVImage, cv2.COLOR_RGB2BGR)
        openCVImage = openCVImage / 255.0
        openCVImage = np.array([openCVImage])

        mask = model.predict(openCVImage, batch_size=None, verbose=0, steps=None)
        mask = mask[0]
        mask = (mask > 0.5) * 255
        mask = mask.astype(np.uint8)
        mask = cv2.resize(mask, (w, h))
        return PIL.Image.fromarray(mask)