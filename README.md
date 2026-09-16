# Brackish YOLO26s — Underwater Detection Demo

This is a **single-folder runnable demo** for the Task 1 underwater-vision evidence.

It uses the **Brackish YOLO26s** model to detect marine animals in `fish8.jpg`, then calculates:

- bounding box
- object centroid (bounding-box center)
- image center
- pixel error
- normalized horizontal error
- normalized vertical error

## Files

```text
Brackish_Fish8_Demo/
├── fish8.jpg
├── detect.py
├── requirements.txt
├── run.sh
└── README.md
```

The first run downloads `best.pt` automatically from the official Hugging Face model repository, so the 20.4 MB model checkpoint does not need to be committed into Git.

## 1. Use your existing Python environment

If you already have the project virtual environment from Task 1:

```bash
source ~/Documents/Development/kyushu_project/beg_task/.venv/bin/activate
```

Then:

```bash
cd /path/to/Brackish_Fish8_Demo
pip install -r requirements.txt
./run.sh
```

## 2. Or install into a fresh environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
./run.sh
```

## Output

The program creates:

```text
brackish_result.jpg
detection_report.txt
```

The annotated image shows:

- green bounding boxes
- red centroid dots
- blue image-center marker
- detected class/confidence

The text report contains the exact numerical values for each detection.

## Normalized error

For image width `W` and height `H`:

```text
image_center_x = W / 2
image_center_y = H / 2

error_x = cx - image_center_x
error_y = cy - image_center_y

normalized_x = error_x / image_center_x
normalized_y = error_y / image_center_y
```

For a centroid inside the image, both normalized errors lie in `[-1, 1]`.

## Model

The model is:

`dronefreak/brackish-yolo26s`

It is fine-tuned on the Brackish Underwater benchmark and contains these classes:

- crab
- fish
- jellyfish
- shrimp
- small_fish
- starfish

Model source:

https://huggingface.co/dronefreak/brackish-yolo26s

The model card reports test-split metrics of mAP@50 99.1 and mAP@50-95 85.77 for the Brackish benchmark. These are benchmark results and should not be interpreted as guaranteed performance on arbitrary underwater images.

## Important limitation

This demo is for Task 1 / perception experimentation. The Brackish model was trained on a specific underwater dataset and its model card notes that all footage came from one fixed camera/location in Denmark; generalization to other cameras, locations and water types is untested.

Therefore, a successful result on `fish8.jpg` is evidence of a working pipeline, not proof of general underwater detection performance.

## Task 1 pipeline

```text
Underwater image
      ↓
Brackish YOLO26s
      ↓
Bounding box
      ↓
Centroid
      ↓
Image center
      ↓
Normalized image error
```
