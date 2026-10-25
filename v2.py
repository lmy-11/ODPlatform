from od_platform.inference.overlay import FPSCounter, Metrics
fps = FPSCounter(window_size=5)
for ms in [10, 12, 11, 9, 10]: fps.update(ms)
assert abs(fps.fps - 95.2) < 1.0
print(f"? FPSCounter: fps={fps.fps:.1f}, inst={fps.inst:.1f}")
m = Metrics()
m.capture.update(33.3)
m.add_speed({"preprocess": 1.5, "inference": 8.0, "postprocess": 2.0})
print(f"? Metrics snapshot: {m.snapshot()}")
