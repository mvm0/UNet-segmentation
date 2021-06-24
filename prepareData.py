from keras.preprocessing.image import ImageDataGenerator


# Подготовка данных для обучения (генератор)
def train_generator(batch_size=32):
    data_gen_args = dict(featurewise_center=True,
                         rotation_range=90.,
                         width_shift_range=0.1,
                         height_shift_range=0.1,
                         fill_mode="constant",
                         cval=0,
                         horizontal_flip=True,
                         vertical_flip=True,
                         zoom_range=0.2)
    image_datagen = ImageDataGenerator(**data_gen_args)
    mask_datagen = ImageDataGenerator(**data_gen_args)
    seed = 1
    image_generator = image_datagen.flow_from_directory(
        'data/train/images',
        class_mode=None,
        batch_size=batch_size,
        color_mode='rgb',
        target_size=(512, 512),
        seed=seed)

    mask_generator = mask_datagen.flow_from_directory(
        'data/train/masks',
        class_mode=None,
        color_mode='grayscale',
        target_size=(512, 512),
        batch_size=batch_size,
        seed=seed)

    train_generator = zip(image_generator, mask_generator)
    for (imgs, masks) in train_generator:
        imgs = imgs / 255.0
        masks = masks / 255.0
        yield (imgs,masks)