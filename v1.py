from od_platform.inference.pipeline_config import load_pipeline_config

pc = load_pipeline_config("apps/platform/configs/runtime/infer_pipeline.yaml")
print("viz_enabled:", pc.viz_enabled, "| label_mapping:", len(pc.label_mapping))
print("camera_raw:", pc.camera_raw)
pc2 = load_pipeline_config("nonexist.yaml")
print("缺失文件兜底:", pc2.viz_enabled, pc2.camera_raw)
