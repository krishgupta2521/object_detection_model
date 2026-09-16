# Kyushu Task 1 (Beginner Foundations)

- bounding box
- object centroid (bounding-box center)
- image center
- pixel error
- normalized horizontal error
- normalized vertical error

## 2. Install environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 detect.py
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


For ROS2 

Publisher: 
source /opt/ros/jazzy/setup.bash
source ~/ros2_ws/install/setup.bash
ros2 run ros2_image_pub_sub_demo image_subscriber

Subsriber
(Then in another terminal):
source /opt/ros/jazzy/setup.bash
source ~/ros2_ws/install/setup.bash
ros2 run ros2_image_pub_sub_demo image_subscriber