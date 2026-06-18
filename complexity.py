"""Theoretical time-complexity helpers for all sorting algorithms."""

from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class ComplexityProfile:
    algorithm: str
    best: str
    average: str
    worst: str
    space: str
    stable: bool


BUBBLE_PROFILE = ComplexityProfile(
    algorithm="Bubble Sort",
    best="O(n)",
    average="O(n²)",
    worst="O(n²)",
    space="O(1)",
    stable=True,
)

MERGE_PROFILE = ComplexityProfile(
    algorithm="Merge Sort",
    best="O(n log n)",
    average="O(n log n)",
    worst="O(n log n)",
    space="O(n)",
    stable=True,
)

INSERTION_PROFILE = ComplexityProfile(
    algorithm="Insertion Sort",
    best="O(n)",
    average="O(n²)",
    worst="O(n²)",
    space="O(1)",
    stable=True,
)

SELECTION_PROFILE = ComplexityProfile(
    algorithm="Selection Sort",
    best="O(n²)",
    average="O(n²)",
    worst="O(n²)",
    space="O(1)",
    stable=False,
)

QUICK_PROFILE = ComplexityProfile(
    algorithm="Quick Sort",
    best="O(n log n)",
    average="O(n log n)",
    worst="O(n²)",
    space="O(log n)",
    stable=False,
)

HEAP_PROFILE = ComplexityProfile(
    algorithm="Heap Sort",
    best="O(n log n)",
    average="O(n log n)",
    worst="O(n log n)",
    space="O(1)",
    stable=False,
)

ALL_PROFILES = [
    BUBBLE_PROFILE,
    INSERTION_PROFILE,
    SELECTION_PROFILE,
    MERGE_PROFILE,
    QUICK_PROFILE,
    HEAP_PROFILE,
]


def parse_sequence(raw: str) -> list[int]:
    if not raw.strip():
        raise ValueError("Enter at least one number.")

    tokens = raw.replace(",", " ").split()
    numbers: list[int] = []
    for token in tokens:
        try:
            numbers.append(int(token))
        except ValueError as exc:
            raise ValueError(f"Invalid number: {token!r}") from exc

    if not numbers:
        raise ValueError("Enter at least one number.")
    return numbers


def is_sorted(values: list[int]) -> bool:
    return all(values[i] <= values[i + 1] for i in range(len(values) - 1))


def theoretical_operation_estimates(n: int, already_sorted: bool) -> dict[str, int]:
    """Rough comparison counts used to illustrate scaling (not exact constants)."""
    if n <= 1:
        return {
            "bubble_comparisons": 0,
            "merge_comparisons": 0,
            "insertion_comparisons": 0,
            "selection_comparisons": 0,
            "quick_comparisons": 0,
            "heap_comparisons": 0,
        }

    bubble = n - 1 if already_sorted else n * (n - 1) // 2
    merge = int(n * math.log2(n))
    insertion = n - 1 if already_sorted else n * (n - 1) // 2
    selection = n * (n - 1) // 2  # always O(n²)
    quick = int(n * math.log2(n)) if not already_sorted else n * (n - 1) // 2
    heap = int(n * math.log2(n))

    return {
        "bubble_comparisons": bubble,
        "merge_comparisons": merge,
        "insertion_comparisons": insertion,
        "selection_comparisons": selection,
        "quick_comparisons": quick,
        "heap_comparisons": heap,
    }
