from __future__ import annotations
import logging
import numpy as np
from pathlib import Path
from PySide6.QtCore import QObject, Signal
from od_platform.frame_source import SourceType

logger = logging.getLogger(__name__)

class QtSignalSink(QObject):
    frame_ready = Signal(object)
    write_count = 0

    def __init__(self, parent: QObject | None = None) -> None:
        QObject.__init__(self, parent)

    def open(self, output_dir: Path, source_type: SourceType) -> None:
        pass

    def write(self, frame, annotated: np.ndarray) -> None:
        try:
            if not annotated.flags["C_CONTIGUOUS"]:
                annotated = np.ascontiguousarray(annotated)
            self.frame_ready.emit(annotated)
            self.write_count += 1
        except Exception as e:
            logger.warning(f"QtSignalSink.write 失败 (已吞): {e}")

    def close(self) -> None:
        pass
