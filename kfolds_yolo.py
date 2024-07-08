from pathlib import Path
import yaml
import pandas as pd
from collections import Counter
from sklearn.model_selection import KFold
import shutil
from ultralytics import YOLO
import os
from statistics import mean 

def get_all_subdirectories(directory):
    subdirectories = [x[0] for x in os.walk(directory)]
    return subdirectories

def perform_kfolds(dataset_path, ksplit):
    dataset_path = Path(dataset_path)  # replace with 'path/to/dataset' for your custom data
    subdirs = ["train", "test", "val"]

    labels = []

    # Get all label files
    for subdir in subdirs:
        labels.extend((dataset_path / subdir).rglob("*labels/*.txt"))  # all data in 'labels'

    # Load class names from the YAML file
    yaml_file = dataset_path / "data.yaml"  # your data YAML with data directories and names dictionary
    with open(yaml_file, "r", encoding="utf8") as y:
        classes = yaml.safe_load(y)["names"]

    # Create an empty dataframe with class names as columns
    indx = [l.stem for l in labels]  # uses base filename as ID (no extension)
    labels_df = pd.DataFrame(0, columns=classes, index=indx)

    # Populate the dataframe
    for label in labels:
        lbl_counter = Counter()

        with open(label, "r") as lf:
            lines = lf.readlines()

        for l in lines:
            # classes for YOLO label uses integer at first position of each line
            class_id = int(l.split(" ")[0])
            class_name = classes[class_id]
            lbl_counter[class_name] += 1

        # Update the dataframe row with the counts from lbl_counter
        for class_name, count in lbl_counter.items():
            labels_df.loc[label.stem, class_name] = count

    # Replace any `nan` values with `0.0`
    labels_df = labels_df.fillna(0.0)
    print(labels_df)

    ksplit = 5
    kf = KFold(n_splits=ksplit, shuffle=True, random_state=20)  # setting random_state for repeatable results

    kfolds = list(kf.split(labels_df))

    folds = [f"split_{n}" for n in range(1, ksplit + 1)]
    folds_df = pd.DataFrame(index=indx, columns=folds)

    for idx, (train, val) in enumerate(kfolds, start=1):
        folds_df[f"split_{idx}"].loc[labels_df.iloc[train].index] = "train"
        folds_df[f"split_{idx}"].loc[labels_df.iloc[val].index] = "val"

    print(folds_df)

    fold_lbl_distrb = pd.DataFrame(index=folds, columns=classes)

    for n, (train_indices, val_indices) in enumerate(kfolds, start=1):
        train_totals = labels_df.iloc[train_indices].sum()
        val_totals = labels_df.iloc[val_indices].sum()

        # To avoid division by zero, we add a small value (1E-7) to the denominator
        ratio = val_totals / (train_totals + 1e-7)
        fold_lbl_distrb.loc[f"split_{n}"] = ratio

    print(fold_lbl_distrb)

    supported_extensions = [".jpg", ".jpeg", ".png"]

    # Initialize an empty list to store image file paths
    images = []

    # Loop through supported extensions and gather image files
    for subdir in subdirs:
        for ext in supported_extensions:
            images.extend(sorted((dataset_path / subdir / "images").rglob(f"*{ext}")))

    print('images')
    print(images)

    # Create the necessary directories and dataset YAML files (unchanged)
    save_path = Path(dataset_path / f"{ksplit}-Fold_Cross-val")
    save_path.mkdir(parents=True, exist_ok=True)
    ds_yamls = []

    for split in folds_df.columns:
        # Create directories
        split_dir = save_path / split
        split_dir.mkdir(parents=True, exist_ok=True)
        (split_dir / "train" / "images").mkdir(parents=True, exist_ok=True)
        (split_dir / "train" / "labels").mkdir(parents=True, exist_ok=True)
        (split_dir / "val" / "images").mkdir(parents=True, exist_ok=True)
        (split_dir / "val" / "labels").mkdir(parents=True, exist_ok=True)

        # Create dataset YAML files
        dataset_yaml = split_dir / f"data.yaml"
        ds_yamls.append(Path(dataset_yaml).as_posix())
        data_yaml_path = os.path.abspath(split_dir)

        with open(dataset_yaml, "w") as ds_y:
            yaml.safe_dump(
                {
                    "path": Path(data_yaml_path).as_posix(),
                    "train": "train",
                    "val": "val",
                    "names": list(classes),
                },
                ds_y,
            )

    for image, label in zip(images, labels):
        for split, k_split in folds_df.loc[image.stem].items():
            # Destination directory
            img_to_path = save_path / split / k_split / "images"
            lbl_to_path = save_path / split / k_split / "labels"

            # Copy image and label files to new directory (SamefileError if file already exists)
            shutil.copy(image, img_to_path / image.name)
            shutil.copy(label, lbl_to_path / label.name)

    return ds_yamls #returns data yamls for each fold


# not really used in train.py i just want to test if it works
def main():
    ksplit = 5
    folds = perform_kfolds('./data/raw_dataset', ksplit)
    print(folds)
    weights_path = "./yolov8n.pt"
    model = YOLO(weights_path, task="detect")

    results = {}

    # Define your additional arguments here
    batch = -1
    project = "kfold_demo"
    epochs = 1

    for k in range(ksplit):
        dataset_yaml = folds[k]
        print(dataset_yaml)
        model.train(data=dataset_yaml, epochs=epochs, batch=batch, name=project, workers=2)  # include any train arguments
        model_results = model.val(data=dataset_yaml)
        results[k] = model_results.box.map  # save output metrics for further analysis
        print(results)

    print(mean(list(results.values())))

if __name__ == '__main__':
    main()