import cv2
import numpy as np
from typing import List, Any

class DrawStyle:
    def __init__(self, box_thickness=2, text_scale=0.5, text_color=(255,255,255), text_bg_alpha=0.6):
        self.box_thickness = box_thickness
        self.text_scale = text_scale
        self.text_color = text_color
        self.text_bg_alpha = text_bg_alpha
    @classmethod
    def from_image_size(cls, h, w, **kwargs):
        return cls(**kwargs)

class BeautifyVisualizer:
    def __init__(self, labels: List[str], label_mapping: dict=None, color_mapping: dict=None, default_color=(0,255,0), font_path=None):
        self.labels = labels
        self.label_mapping = label_mapping or {}
        self.color_mapping = color_mapping or {}
        self.default_color = default_color
    
    @classmethod
    def from_yolo_results(cls, boxes, confidences, labels):
        return {"boxes": boxes, "confs": confidences, "labels": labels}

    def draw(self, image: np.ndarray, dets: dict, style: DrawStyle, use_label_mapping: bool) -> np.ndarray:
        out = image.copy()
        boxes = dets.get("boxes", [])
        confs = dets.get("confs", [])
        labels = dets.get("labels", [])
        for box, conf, label in zip(boxes, confs, labels):
            x1, y1, x2, y2 = map(int, box)
            color = self.color_mapping.get(label, self.default_color)
            cv2.rectangle(out, (x1, y1), (x2, y2), color, style.box_thickness)
            disp_label = self.label_mapping.get(label, label) if use_label_mapping else label
            text = f"{disp_label} {conf:.2f}"
            cv2.putText(out, text, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, style.text_scale, color, 1)
        return out