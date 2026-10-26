from __future__ import annotations
import logging
from PySide6.QtCore import QObject, Signal, Slot
from od_platform.inference import CancelToken, InferHooks, InferResult, ProgressEvent, infer_yolo

logger = logging.getLogger(__name__)

class InferWorker(QObject):
    progress_changed = Signal(int, int, float)
    inference_finished = Signal(object)
    inference_failed = Signal(str)

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.cancel_token = CancelToken()
        self._sink = None

    def set_sink(self, sink) -> None:
        self._sink = sink

    @Slot(str, str)
    def start_infer(self, model: str, source: str) -> None:
        self.cancel_token = CancelToken()
        hooks = InferHooks(
            on_progress=self._on_progress,
            on_complete=self._on_complete,
            on_error=self._on_error,
        )
        try:
            result = infer_yolo(
                cli_args={"source": source, "model": model, "show": False, "save": False},
                output_sink=self._sink, hooks=hooks, cancel_token=self.cancel_token,
            )
        except Exception as e:
            logger.error(f"InferWorker 异常: {e}")
            self.inference_failed.emit(str(e))

    @Slot()
    def cancel(self) -> None:
        self.cancel_token.cancel()

    def _on_progress(self, evt: ProgressEvent) -> None:
        total = evt.total_frames if evt.total_frames is not None else -1
        self.progress_changed.emit(evt.frame_idx, total, evt.fps_loop)

    def _on_complete(self, result: InferResult) -> None:
        self.inference_finished.emit(result)

    def _on_error(self, exc: Exception) -> None:
        self.inference_failed.emit(str(exc))
