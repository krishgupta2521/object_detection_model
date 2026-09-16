from pathlib import Path
import sys

import cv2
from huggingface_hub import hf_hub_download
from ultralytics import YOLO


ROOT = Path(__file__).resolve().parent
IMAGE_PATH = ROOT / "images" / "fish8.jpg"
OUTPUT_PATH = ROOT / "brackish_result.jpg"
REPORT_PATH = ROOT / "detection_report.txt"

REPO_ID = "dronefreak/brackish-yolo26s"
WEIGHTS_NAME = "best.pt"
CONFIDENCE = 0.25


def main():
    if not IMAGE_PATH.exists():
        raise FileNotFoundError(f"Input image not found: {IMAGE_PATH}")

    print("Downloading/loading Brackish YOLO26s model...")
    weights = hf_hub_download(
        repo_id=REPO_ID,
        filename=WEIGHTS_NAME,
    )
    model = YOLO(weights)

    image = cv2.imread(str(IMAGE_PATH))
    if image is None:
        raise RuntimeError(f"Could not read image: {IMAGE_PATH}")

    height, width = image.shape[:2]
    center_x = width / 2.0
    center_y = height / 2.0

    print(f"Image size: {width} x {height}")
    print(f"Image center: ({center_x:.1f}, {center_y:.1f})")
    print(f"Confidence threshold: {CONFIDENCE}")

    results = model.predict(
        source=str(IMAGE_PATH),
        conf=CONFIDENCE,
        verbose=False,
    )

    result = results[0]
    annotated = image.copy()
    detections = []

    cv2.drawMarker(
        annotated,
        (round(center_x), round(center_y)),
        (255, 0, 0),
        cv2.MARKER_CROSS,
        20,
        2,
    )

    if result.boxes is not None:
        for i, box in enumerate(result.boxes):
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().tolist()
            confidence = float(box.conf[0].cpu().item())
            class_id = int(box.cls[0].cpu().item())
            class_name = result.names[class_id]

            cx = (x1 + x2) / 2.0
            cy = (y1 + y2) / 2.0

            error_x = cx - center_x
            error_y = cy - center_y

            normalized_x = error_x / center_x
            normalized_y = error_y / center_y

            detections.append(
                {
                    "index": i + 1,
                    "class": class_name,
                    "confidence": confidence,
                    "bbox": (x1, y1, x2, y2),
                    "centroid": (cx, cy),
                    "pixel_error": (error_x, error_y),
                    "normalized_error": (normalized_x, normalized_y),
                }
            )

            # Bounding box.
            p1 = (round(x1), round(y1))
            p2 = (round(x2), round(y2))
            cv2.rectangle(annotated, p1, p2, (0, 255, 0), 2)

            # Centroid.
            cv2.circle(
                annotated,
                (round(cx), round(cy)),
                5,
                (0, 0, 255),
                -1,
            )

            label = f"{class_name} {confidence:.2f}"
            cv2.putText(
                annotated,
                label,
                (round(x1), max(20, round(y1) - 8)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (0, 255, 0),
                2,
            )

            cv2.putText(
                annotated,
                f"C{i + 1}: ({cx:.1f},{cy:.1f})",
                (round(x1), min(height - 10, round(y2) + 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 0, 255),
                2,
            )

    cv2.putText(
        annotated,
        f"Detections: {len(detections)}",
        (10, 28),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.75,
        (255, 255, 255),
        2,
    )

    if not cv2.imwrite(str(OUTPUT_PATH), annotated):
        raise RuntimeError(f"Could not save: {OUTPUT_PATH}")

    with REPORT_PATH.open("w", encoding="utf-8") as f:
        f.write("Brackish YOLO26s — Task 1 Underwater Detection Demo\n")
        f.write("=" * 58 + "\n")
        f.write(f"Input: {IMAGE_PATH.name}\n")
        f.write(f"Image size: {width} x {height}\n")
        f.write(f"Image center: ({center_x:.2f}, {center_y:.2f})\n")
        f.write(f"Confidence threshold: {CONFIDENCE}\n")
        f.write(f"Detections: {len(detections)}\n\n")

        for d in detections:
            x1, y1, x2, y2 = d["bbox"]
            cx, cy = d["centroid"]
            ex, ey = d["pixel_error"]
            nx, ny = d["normalized_error"]

            f.write(f"Detection {d['index']}\n")
            f.write(f"  class: {d['class']}\n")
            f.write(f"  confidence: {d['confidence']:.3f}\n")
            f.write(
                f"  bbox: ({x1:.1f}, {y1:.1f}, {x2:.1f}, {y2:.1f})\n"
            )
            f.write(f"  centroid: ({cx:.2f}, {cy:.2f})\n")
            f.write(f"  pixel error: ({ex:.2f}, {ey:.2f})\n")
            f.write(f"  normalized error: ({nx:.3f}, {ny:.3f})\n")
            f.write(f"  normalized x in [-1,1]: {(-1 <= nx <= 1)}\n")
            f.write(f"  normalized y in [-1,1]: {(-1 <= ny <= 1)}\n\n")

    print("\nRESULTS")
    print(f"Detections: {len(detections)}")
    for d in detections:
        print(
            f"{d['index']}. {d['class']} "
            f"conf={d['confidence']:.3f} "
            f"centroid=({d['centroid'][0]:.2f}, {d['centroid'][1]:.2f}) "
            f"normalized=({d['normalized_error'][0]:.3f}, "
            f"{d['normalized_error'][1]:.3f})"
        )

    print(f"\nAnnotated image: {OUTPUT_PATH}")
    print(f"Text report:     {REPORT_PATH}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"\nERROR: {exc}", file=sys.stderr)
        sys.exit(1)
