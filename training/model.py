"""
model python file contain three classes at this moment.
ModelPreparation():
    - contain methods necessary to preapere data and model to learning process

ModelCreation():
    - contain methods necessary to create model. In particular create_model() function.
CyclicR(Callback):
"""
import numpy as np
from tensorflow.keras.layers import GlobalAveragePooling2D
from tensorflow.keras.layers import Concatenate, GlobalMaxPooling2D
from tensorflow.keras.layers import Dense, Dropout, Flatten, Input
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.callbacks import Callback
from tensorflow.keras.applications.nasnet import NASNetMobile, preprocess_input
from tensorflow.keras.losses import binary_crossentropy
from tensorflow.keras.optimizers import Adam
import cv2
import os
from utils import dbg
from glob import glob


class ModelPreparation:
    def __init__(self, path, batch_size, generator_data, labeled_data):
        self.path = path
        self.batch = batch_size
        self.generator_data = generator_data
        self.labeled_data = labeled_data

    def get_id_from_path(self):
        return os.path.basename(self.path).replace(".tif", "")

    def get_path_from_id(self, data_path, image_id):
        return data_path + image_id + ".tif"

    def get_image_label(self, image_id):
        return self.labeled_data[image_id]


class ModelCreation:
    def __init__(
        self, input_shape, output_shape, learning_rate, architecture, model_data_dir="./models/", saved_weights=False, saved_model=False
    ):
        """
        :param model_data_dir: Path where to store saved models etc
        """

        self.input_shape = input_shape
        self.output_shape = output_shape
        # self.input_iterator, self.output_iterator = iterators
        self.architecture = architecture
        self.learning_rate = learning_rate
        self.model_data_dir = model_data_dir
        self.model = None

        if self.architecture == 'efficientnet':
            dbg(f"Creating {self.architecture} model")
            self.model = self.create_model_efficientnet()

        if self.architecture == 'nasnet':
            dbg(f"Creating {self.architecture} model")
            self.model = self.create_model_nasnet()

        if saved_model:
            dbg(f"Loading saved model: {saved_model}")
            self.model = load_model(saved_model)

        if not self.model:
            dbg(f"Model {self.architecture} not found", mode="crit")
        self.model.summary()

        if saved_weights:
            dbg(f"Loading saved weights: {saved_weights}")
            self.model.load_weights(saved_weights)

    def create_model_efficientnet(self):
        # Import Efficientnet
        import efficientnet.tfkeras as efn

        input_tensor = Input(shape=self.input_shape)
        base_model = efn.EfficientNetB2(include_top=False, input_tensor=input_tensor)
        x = base_model(input_tensor)
        x = Flatten()(x)
        x = Dense(1024, activation="relu")(x)
        x = Dropout(0.5)(x)
        out = Dense(self.output_shape, activation="sigmoid")(x)
        model = Model(input_tensor, out)
        model.compile(optimizer=Adam(self.learning_rate), loss=binary_crossentropy, metrics=['acc'])
        return model

    def create_model_nasnet(self):
        input_tensor = Input(shape=self.input_shape)
        base_model = NASNetMobile(include_top=False, input_tensor=input_tensor)
        x = base_model(input_tensor)
        out_1 = GlobalMaxPooling2D()(x)
        out_2 = GlobalAveragePooling2D()(x)
        out_3 = Flatten()(x)
        out = Concatenate(axis=-1)([out_1, out_2, out_3])
        out = Dropout(0.5)(out)
        out = Dense(self.output_shape, activation="sigmoid")(out)
        model = Model(input_tensor, out)
        model.compile(optimizer=Adam(self.learning_rate), loss=binary_crossentropy, metrics=['acc'])
        return model

    def save_model(self, filename=""):
        model_file_path = self.model_data_dir + filename + self.architecture
        i = 1
        while os.path.isfile(model_file_path):
            model_file_path = self.model_data_dir + filename + self.architecture + '-' + str(i)
            i += 1
        weights_path = model_file_path + "-weights"
        model_file_path = model_file_path + '-model'
        self.model.save(model_file_path)
        self.model.save_weights(weights_path, save_format='tf')
        dbg(f"model saved: {model_file_path}\tweights saved: {weights_path}")

    def evaluate(self, folder_path):
        images = glob(folder_path + "/*.tif")
        print(images)
        dbg("Evaluating the model on {} entries".format(len(images)))

        results = {}
        i=0
        for img in images:
            image = preprocess_input(cv2.imread(img))
            results[img] = self.model.predict(np.expand_dims(image, axis=0))
            # image = cv2.imread(img)
            # image = cv2.resize(image, (96, 96, 3))
            # image = preprocess_input(cv2.imread(img))
            # results[img] = self.model.predict(image)
            i+=1
            if i >100:
                break
        return results

    def single_evaluate(self, img_path):
        input_data = preprocess_input(cv2.imread(img_path))
        return {img_path: self.model.predict(np.expand_dims(input_data, axis=0))}


class CyclicLR(Callback):
    def __init__(self, base_lr, max_lr, step_size, base_m, max_m, cyclical_momentum):
        self.base_lr = base_lr
        self.max_lr = max_lr
        self.base_m = base_m
        self.max_m = max_m
        self.cyclical_momentum = cyclical_momentum
        self.step_size = step_size

        self.clr_iterations = 0.0
        self.cm_iterations = 0.0
        self.trn_iterations = 0.0
        self.history = {}

    def clr(self):
        cycle = np.floor(1 + self.clr_iterations / (2 * self.step_size))
        if cycle == 2:
            x = np.abs(self.clr_iterations / self.step_size - 2 * cycle + 1)
            return self.base_lr - (self.base_lr - self.base_lr / 100) * np.maximum(
                0, (1 - x)
            )
        else:
            x = np.abs(self.clr_iterations / self.step_size - 2 * cycle + 1)
            return self.base_lr + (self.max_lr - self.base_lr) * np.maximum(0, (1 - x))

    def cm(self):
        cycle = np.floor(1 + self.clr_iterations / (2 * self.step_size))
        if cycle == 2:

            x = np.abs(self.clr_iterations / self.step_size - 2 * cycle + 1)
            return self.max_m
        else:
            x = np.abs(self.clr_iterations / self.step_size - 2 * cycle + 1)
            return self.max_m - (self.max_m - self.base_m) * np.maximum(0, (1 - x))

    def on_train_begin(self, logs={}):
        logs = logs or {}
        if self.clr_iterations == 0:
            K.set_value(self.model.optimizer.lr, self.base_lr)
        else:
            K.set_value(self.model.optimizer.lr, self.clr())

        if self.cyclical_momentum == True:
            if self.clr_iterations == 0:
                K.set_value(self.model.optimizer.momentum, self.cm())
            else:
                K.set_value(self.model.optimizer.momentum, self.cm())

    def on_batch_begin(self, batch, logs=None):
        logs = logs or {}
        self.trn_iterations += 1
        self.clr_iterations += 1

        self.history.setdefault("lr", []).append(K.get_value(self.model.optimizer.lr))
        self.history.setdefault("iterations", []).append(self.trn_iterations)

        if self.cyclical_momentum == True:
            self.history.setdefault("momentum", []).append(
                K.get_value(self.model.optimizer.momentum)
            )

        for k, v in logs.items():
            self.history.setdefault(k, []).append(v)

        K.set_value(self.model.optimizer.lr, self.clr())

        if self.cyclical_momentum == True:
            K.set_value(self.model.optimizer.momentum, self.cm())
