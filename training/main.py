"""
This file contain the execute file with.
Only after-learning functions are contain here.
At this moment, all libraries are import here, however at the final version it will be changed.
"""
from model import ModelCreation
from generator import DataGenerator
from utils import dbg, CoolDownCallback
import argparse
from tensorflow.keras.callbacks import ModelCheckpoint

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # Hardware options
    parser.add_argument("--hardware", "-H", type=str, help="Define what hardware is used during execute the prject.", required=False)

    # General options
    parser.add_argument("--train", type=int, help="Provide number of training epochs", required=False)
    parser.add_argument("--train_image_path", type=str, help="Training images dataset path", required=True)
    parser.add_argument("--train_image_labels_path", type=str, help="Training images labels path", required=True)
    parser.add_argument("--model", type=str, help="Define type of used architecture [efficientnet = EfficientNetB2, nasnet = NASNetMobile]", required=False, default='nasnet')
    parser.add_argument("--load-weights", type=str, help="Path to saved weights", required=False)
    parser.add_argument("--load-model", type=str, help="Path to saved model", required=False)
    parser.add_argument("--generate-tfrecord", help="Generate tfrecord file", required=False, action='store_true')
    parser.add_argument("--tfrecord-path", help="Path to tfrecord file", required=False)
    parser.add_argument("--max-size", type=int, help="Max dataset size", required=False)
    parser.add_argument("--augment-data", help="Do augment data", required=False, action="store_true")
    parser.add_argument("--validation-split", type=float, help="Validation split of training data", default=0.05)
    parser.add_argument("--learning-rate", type=float, help="Learning rate", default=0.001)
    parser.add_argument("--batch-size", type=int, help="Batch size", default=32)
    parser.add_argument("--model-data-dir", type=str, help="Path to store saved models", default="./models/")
    parser.add_argument("--wandb", help="Log training progress to wandb", required=False, action='store_true')
    parser.add_argument("--checkpoint", help="Auto save model checkpoint", required=False, action='store_true')
    parser.add_argument("--cooldown", help="Cool down the GPU ", required=False, action='store_true')

    # Evaluation options
    parser.add_argument("--evaluate", type=str, help="Do evaluate model on images from given directory",
                        required=False)
    parser.add_argument("--evaluate-single", type=str, help="Do evaluate model on specific image", required=False)
    parser.add_argument("--save-activations", action="store_true",
                        help="Save image activations while evaluating instead of plotting it", required=False)
    parser.add_argument("--evaluation-results-dir", type=str, help="Path to store evaluation results",
                        default="./results/")
    parser.add_argument("--shift", help="Evaluate second time with shifted images", required=False, action='store_true')

    args = parser.parse_args()
    if args.evaluate and args.evaluate_single:
        dbg("Cannot combine evaluation on multiple images and single image", mode="crit")

    shapes = {"input": (96, 96, 3), "output": 1}
    if args.hardware=="KRIM":
        train_image_path = args.train_image_path
        train_image_labels_path = args.train_image_labels_path
    else:
        train_image_path = "./data/train/"
        train_image_labels_path = "./data/train_labels.csv"

    # Wandb
    if args.wandb:
        dbg("Using Weights and Biases")
        import wandb
        from wandb.keras import WandbCallback
        wandb.init(entity='agh-techmed', project='kaggle-cancer-detection')

    # Create the generator
    train_generator = DataGenerator(
        train_image_path,
        train_image_labels_path,
        data_shapes=shapes,
        batch_size=args.batch_size,
        is_prepared=False if args.generate_tfrecord else True,
        augment_data=args.augment_data,
        validation_split=args.validation_split,
        tf_record_file_path=args.tfrecord_path if args.tfrecord_path else "",
        max_size=args.max_size if args.max_size else ""
    )

    # Exit if no more actions are specified
    if not(args.train or args.evaluate or args.evaluate_single):
        dbg("Nothing more to do, exiting")
        exit()

    # check trailing slash
    model_dir = args.model_data_dir
    if model_dir[-1] != "/":
        model_dir += "/"

    # Build the model
    model_util = ModelCreation(
        input_shape=shapes["input"],
        output_shape=shapes["output"],
        learning_rate=args.learning_rate,
        architecture=args.model,
        model_data_dir=model_dir,
        saved_weights=args.load_weights,  # when this parameter is not provided it will be False
        saved_model=args.load_model
    )

    if args.train:
        callbacks = []
        if args.wandb:
            callbacks.append(WandbCallback())

        if args.checkpoint:
            callbacks.append(ModelCheckpoint(model_dir + '/' + args.model + '-checkpoint.hdf5', monitor='val_loss', save_best_only=True, mode='min', verbose=1))

        if args.cooldown:
            callbacks.append(CoolDownCallback())

        # Train the model
        dbg(f"training the {args.model} model")
        model_util.model.fit(
            train_generator.tfdataset_train,
            steps_per_epoch=train_generator.get_steps_per_epoch(),
            epochs=args.train,
            validation_data=train_generator.tfdataset_validation,
            validation_steps=train_generator.get_validation_steps_per_epoch(),
            callbacks=callbacks
        )
        # Save after training
        model_util.save_model()
