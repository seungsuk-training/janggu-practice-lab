#!/usr/bin/env python3
"""Detect likely janggu strike onsets and visualize them over the waveform."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

import librosa
import matplotlib.pyplot as plt
import numpy as np


def positive_int(value: str) -> int:
    parsed = int(value)
    if parsed <= 0:
        raise argparse.ArgumentTypeError("0보다 큰 정수여야 합니다.")
    return parsed


def nonnegative_float(value: str) -> float:
    parsed = float(value)
    if parsed < 0:
        raise argparse.ArgumentTypeError("0 이상의 수여야 합니다.")
    return parsed


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="장구 Audio의 타격 시점(Onset)을 검출하고 파형 그림을 저장합니다."
    )
    parser.add_argument("audio", type=Path, help="분석할 Audio 파일 (WAV 권장)")
    parser.add_argument(
        "-o", "--output", type=Path,
        help="결과 PNG 경로 (기본값: 입력 파일 옆의 <이름>-onsets.png)",
    )
    parser.add_argument(
        "--delta", type=nonnegative_float, default=0.07,
        help="peak 민감도 문턱; 낮을수록 많이 검출 (기본값: 0.07)",
    )
    parser.add_argument(
        "--wait-ms", type=nonnegative_float, default=60.0,
        help="검출 사이 최소 간격, millisecond (기본값: 60)",
    )
    parser.add_argument(
        "--hop-length", type=positive_int, default=512,
        help="분석 frame 간 sample 수 (기본값: 512)",
    )
    parser.add_argument("--show", action="store_true", help="저장 후 plot 창도 표시")
    return parser


def detect_onsets(
    samples: np.ndarray,
    sample_rate: int,
    *,
    hop_length: int,
    delta: float,
    wait_ms: float,
) -> tuple[np.ndarray, np.ndarray]:
    """Return onset times and the normalized onset-strength envelope."""
    envelope = librosa.onset.onset_strength(
        y=samples, sr=sample_rate, hop_length=hop_length
    )
    wait_frames = max(
        1,
        int(round((wait_ms / 1000.0) * sample_rate / hop_length)),
    )
    frames = librosa.onset.onset_detect(
        onset_envelope=envelope,
        sr=sample_rate,
        hop_length=hop_length,
        units="frames",
        normalize=True,
        pre_max=1,
        post_max=1,
        pre_avg=3,
        post_avg=3,
        delta=delta,
        wait=wait_frames,
        backtrack=False,
    )
    times = librosa.frames_to_time(frames, sr=sample_rate, hop_length=hop_length)
    return times, envelope


def save_plot(
    samples: np.ndarray,
    sample_rate: int,
    onset_times: np.ndarray,
    output: Path,
    *,
    show: bool,
) -> None:
    duration = len(samples) / sample_rate
    time_axis = np.linspace(0.0, duration, num=len(samples), endpoint=False)

    figure, axis = plt.subplots(figsize=(14, 5))
    axis.plot(time_axis, samples, color="#284b63", linewidth=0.65, label="Waveform")
    for index, onset_time in enumerate(onset_times):
        axis.axvline(
            onset_time,
            color="#d1495b",
            linewidth=1.0,
            alpha=0.85,
            label="Detected onset" if index == 0 else None,
        )
    axis.set(title="Janggu onset detection", xlabel="Time (seconds)", ylabel="Amplitude")
    axis.set_xlim(0, duration)
    axis.grid(alpha=0.2)
    if len(onset_times):
        axis.legend(loc="upper right")
    figure.tight_layout()

    output.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output, dpi=160)
    if show:
        plt.show()
    plt.close(figure)


def main() -> int:
    args = build_parser().parse_args()
    if not args.audio.is_file():
        print(f"오류: Audio 파일을 찾을 수 없습니다: {args.audio}", file=sys.stderr)
        return 2

    output = args.output or args.audio.with_name(f"{args.audio.stem}-onsets.png")
    try:
        samples, sample_rate = librosa.load(args.audio, sr=None, mono=True)
    except Exception as error:
        print(f"오류: Audio 파일을 읽지 못했습니다: {error}", file=sys.stderr)
        return 2
    if samples.size == 0:
        print("오류: Audio 파일에 sample이 없습니다.", file=sys.stderr)
        return 2

    onset_times, _ = detect_onsets(
        samples,
        sample_rate,
        hop_length=args.hop_length,
        delta=args.delta,
        wait_ms=args.wait_ms,
    )

    print(f"파일: {args.audio}")
    print(f"길이: {len(samples) / sample_rate:.3f}초 / Sample rate: {sample_rate} Hz")
    print(
        f"설정: delta={args.delta:g}, wait={args.wait_ms:g} ms, "
        f"hop_length={args.hop_length}"
    )
    print(f"검출된 타격: {len(onset_times)}개")
    for index, onset_time in enumerate(onset_times, start=1):
        print(f"  {index:>3}: {onset_time:.3f}초")

    try:
        save_plot(samples, sample_rate, onset_times, output, show=args.show)
    except Exception as error:
        print(f"오류: 결과 그림을 저장하지 못했습니다: {error}", file=sys.stderr)
        return 2
    print(f"파형 결과: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
