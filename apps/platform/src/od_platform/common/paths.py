#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  : paths.py
# @Author    : ODPlatform Team
# @Project   : ODPlatform
# @Function  : 集中定义项目路径常量
#              - 使用 marker file 模式定位 ROOT_DIR(workspace 根)
#              - 引入 APP_DIR 概念,把【共享资产】和【端私有资产】分开

from __future__ import annotations

from pathlib import Path
from typing import List, Tuple

# ============================================================
# Workspace 根目录定位 (marker file 模式)
# ============================================================
WORKSPACE_MARKER: str = ".odp-workspace"


def _find_workspace_root(
    start: Path,
    markers: Tuple[str, ...] = (WORKSPACE_MARKER,),
) -> Path:
    """
    从 start 开始沿父目录向上查找,返回包含任一 marker 文件的目录。

    Args:
        start: 起始路径(通常是 Path(__file__))
        markers: 一组 marker 文件名,任一存在即视为找到

    Returns:
        Path: workspace 根目录

    Raises:
        FileNotFoundError: 一直爬到文件系统根仍没找到
    """
    current = start.resolve()
    if current.is_file():
        current = current.parent

    for parent in [current, *current.parents]:
        for marker in markers:
            if (parent / marker).exists():
                return parent

    raise FileNotFoundError(
        f"找不到 workspace marker 文件 ({markers})。"
        f"请确认仓库根存在 {WORKSPACE_MARKER} 文件。"
    )


# 计算 ROOT_DIR(模块加载时执行一次)
ROOT_DIR: Path = _find_workspace_root(Path(__file__))


# ============================================================
# 端根目录 APP_DIR (platform 这一个端的根)
# ============================================================
APP_DIR: Path = ROOT_DIR / "apps" / "platform"


# ============================================================
# 【共享资产】(在 ROOT_DIR 下,所有端可访问)
# ============================================================
DATA_DIR: Path = ROOT_DIR / "data"
MODELS_DIR: Path = ROOT_DIR / "models"
RUNS_DIR: Path = ROOT_DIR / "runs"

# 模型子目录
PRETRAINED_MODELS_DIR: Path = MODELS_DIR / "pretrained"  # 下载的预训练权重(输入)
TRAINED_MODELS_DIR: Path = MODELS_DIR / "trained" 
CHECKPOINTS_DIR: Path = MODELS_DIR / "checkpoints"   # 加上这一行       # 训练产出、长期保留的权重(产物)

# 数据集子目录
RAW_DATA_DIR: Path = DATA_DIR / "raw"              # 原始数据:只读,绝不就地改
PROCESSED_DATA_DIR: Path = DATA_DIR / "processed"  # 派生数据集:含冻结后的 train/val/test


# ============================================================
# 【端私有资产】(在 APP_DIR 下,只属于 platform 这个端)
# ============================================================
CONFIGS_DIR: Path = APP_DIR / "configs"
LOGGING_DIR: Path = APP_DIR / "logging"
UNIT_TEST_DIR: Path = APP_DIR / "tests"


# ============================================================
# 【顶层文档目录】(共享给所有人)
# ============================================================
DOCS_DIR: Path = ROOT_DIR / "docs"


# ============================================================
# 【工程基础设施目录】(共享)
# ============================================================
SCRIPTS_DIR: Path = ROOT_DIR / "scripts"


# ============================================================
# 【工具元数据目录】(D2 新增)
# ============================================================
META_DIR: Path = ROOT_DIR / ".odp-meta"
META_LOGGING_DIR: Path = META_DIR / "logs"


# ============================================================
# 对外暴露的"要初始化的目录列表"
# ============================================================
def get_dirs_to_initialize() -> List[Path]:
    """
    返回项目启动时需要确保存在的所有目录列表。
    """
    return [
        # 共享资产
        DATA_DIR,
        RUNS_DIR,
        MODELS_DIR,
        PRETRAINED_MODELS_DIR,
        TRAINED_MODELS_DIR,
        RAW_DATA_DIR,
        PROCESSED_DATA_DIR,
        # 端私有资产
        CONFIGS_DIR,
        LOGGING_DIR,
        UNIT_TEST_DIR,
        # 工程基础设施
        SCRIPTS_DIR,
        DOCS_DIR,
        # 工具元数据 (D2 新增)
        META_LOGGING_DIR,
        RUNTIME_CONFIGS_DIR,    # ★ D5 新增
    ]


# ============================================================
# 对外暴露的"要重置的目录列表" (D2 新增)
# ============================================================
def get_dirs_to_reset() -> List[Path]:
    """
    返回 reset_project 可以安全清理的目录列表。
    """
    return [
        # 划分后的派生数据集
        PROCESSED_DATA_DIR,
        # 训练运行产物
        RUNS_DIR,
        # 训练产出的权重
        TRAINED_MODELS_DIR,
        # 端私有运行时日志
        LOGGING_DIR,
        DATASET_CONFIGS_DIR,
    ]

# ============================================================
# 绝对保护目录 (D2 新增)
# ============================================================
PROTECTED_DIRS: Tuple[Path, ...] = (
    ROOT_DIR,
    ROOT_DIR / "apps",
    ROOT_DIR / "packages",
    APP_DIR,
    APP_DIR / "src",
    SCRIPTS_DIR,
    DOCS_DIR,
    UNIT_TEST_DIR,
    CONFIGS_DIR,
    ROOT_DIR / ".git",
    ROOT_DIR / ".odp-workspace",
    META_DIR,
    META_LOGGING_DIR,
)


def is_protected(path: Path) -> bool:
    path = path.resolve(strict=False)
    for protected in PROTECTED_DIRS:
        protected_resolved = protected.resolve(strict=False)
        if path == protected_resolved:
            return True
        
        # 兼容 Python 3.8 及以下的写法
        try:
            protected_resolved.relative_to(path)
            return True
        except ValueError:
            pass
            
    return False

# ============================================================
# 自测打印 (保留 D1 原本的测试代码)
# ============================================================
if __name__ == "__main__":
    print(f"ROOT_DIR (workspace) = {ROOT_DIR}")
    print(f"APP_DIR  (platform)  = {APP_DIR}")
    print(f"\n共享资产:")
    print(f"  DATA_DIR    = {DATA_DIR.relative_to(ROOT_DIR)}")
    print(f"  MODELS_DIR  = {MODELS_DIR.relative_to(ROOT_DIR)}")
    print(f"  RUNS_DIR    = {RUNS_DIR.relative_to(ROOT_DIR)}")
    print(f"\n端私有资产:")
    print(f"  CONFIGS_DIR = {CONFIGS_DIR.relative_to(ROOT_DIR)}")
    print(f"  LOGGING_DIR = {LOGGING_DIR.relative_to(ROOT_DIR)}")
    
    print(f"\n元数据资产:")
    print(f"  META_LOGGING_DIR = {META_LOGGING_DIR.relative_to(ROOT_DIR)}")

    print(f"\n要初始化的目录共 {len(get_dirs_to_initialize())} 个:")
    for d in get_dirs_to_initialize():
        print(f"  - {d.relative_to(ROOT_DIR)}")
        
    print(f"\n要重置的目录共 {len(get_dirs_to_reset())} 个:")
    for d in get_dirs_to_reset():
        print(f"  - {d.relative_to(ROOT_DIR)}")

# apps/platform/src/od_platform/common/paths.py(增量:追加到文件尾部)

DATASET_CONFIGS_DIR: Path = CONFIGS_DIR / "datasets"   # 数据集 yaml 的家(Ultralytics 约定)

def raw_dataset_root(name: str) -> Path:
    return RAW_DATA_DIR / name

def dataset_processed_dir(name: str) -> Path:
    return PROCESSED_DATA_DIR / name

def dataset_yaml_path(name: str) -> Path:
    return DATASET_CONFIGS_DIR / f"{name}.yaml"

# 别忘了:把 DATASET_CONFIGS_DIR 加进 get_dirs_to_initialize() 的返回元组
VALIDATION_RUNS_DIR: Path = RUNS_DIR / "data_validation"   # 质检报告的家(按需创建,不进 init 清单)


def validation_run_dir(run_id: str) -> Path:
    return VALIDATION_RUNS_DIR / run_id
# ============================================================
# D5 增量: 运行配置目录 (跟 D3 立的 DATASET_CONFIGS_DIR 语义完全不同)
#   DATASET_CONFIGS_DIR: 描述【数据】的 yaml (odp-transform 产出)
#   RUNTIME_CONFIGS_DIR : 描述【跑法】的 yaml (runtime_config 子系统产出)
# 两类 yaml 物理分目录, 语义不会互相污染.
# ============================================================
RUNTIME_CONFIGS_DIR: Path = CONFIGS_DIR / "runtime"


def runtime_config_path(name: str) -> Path:
    """返回某个运行配置文件的路径: <CONFIGS_DIR>/runtime/<name>.yaml

    Args:
        name: 配置名 (如 "train" / "val" / "infer"), 不带 .yaml 后缀

    Returns:
        Path 对象 (尚未创建, 调用方自己负责 mkdir)

    用法:
        train_yaml = runtime_config_path("train")
        # → <APP_DIR>/configs/runtime/train.yaml
    """
    return RUNTIME_CONFIGS_DIR / f"{name}.yaml"