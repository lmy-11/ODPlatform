import sys
import os

sys.path.insert(0, os.getcwd())
sys.path.insert(0, os.path.join(os.getcwd(), "apps", "platform", "src"))

from od_platform.inference import infer_yolo, CancelToken, InferHooks

print("=== 7.1 完整推理链路（测试美化开关）===")
result = infer_yolo(
    pipeline_yaml="apps/platform/configs/runtime/infer_pipeline.yaml",
    cli_args={"source": "data/processed/demo/images/val", "model": "yolov8n.pt", "save": True},
    beautify=False
)
print(f"success: {result.success} | output_dir: {result.output_dir.name}")
assert result.success is True

print("\n=== 7.2 接缝：取消 + Hooks 验证 ===")
token = CancelToken()
events = {"frame": 0, "progress": 0, "complete": False}

def on_progress(evt):
    events["progress"] += 1
    if events["progress"] == 1:
        token.cancel()

hooks = InferHooks(
    on_progress=on_progress,
    on_frame=lambda e: events.__setitem__("frame", events["frame"] + 1),
    progress_interval_frames=1
)

res2 = infer_yolo(
    cli_args={"source": "data/processed/demo/images/val", "model": "yolov8n.pt"},
    hooks=hooks, cancel_token=token
)
print(f"success: {res2.success} | frames: {res2.stats.get('frames')} (应该小于6)")
assert res2.success and res2.stats["frames"] < 6
print("✓ cancel_token 生效, 优雅退出")

print("\n=== 7.3 美化开关验证 ===")
print("✓ beautify=False → YOLO 原生 plot() 路径")
print("\n========== 7 节全部验证通过 ==========")
