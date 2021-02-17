import os
from tensorflow.keras.callbacks import Callback
import time

def dbg(msg, mode="debug"):
    colors = {
        "debug": "\033[92m[*]\t",
        "warning": "\033[93m[!]\t",
        "error": "\033[91m[!]\t",
        "clear": "\033[0m",
    }
    if mode == "crit":
        raise Exception(colors["error"] + str(msg) + colors["clear"])
    print(colors[mode] + str(msg) + colors["clear"])


def get_image_id_from_path(path):
    return os.path.basename(path).replace(".tif", "")


class CoolDownCallback(Callback):
    start_time = False
    cooldown_time = 60
    training_time = 3*60

    def on_train_batch_begin(self, batch, logs=None):
        if self.start_time:
            if time.time() - self.start_time >= self.training_time:
                print(f'Sleeping for {self.cooldown_time} seconds')
                time.sleep(self.cooldown_time)
                self.start_time = time.time()
        else:
            self.start_time = time.time()
