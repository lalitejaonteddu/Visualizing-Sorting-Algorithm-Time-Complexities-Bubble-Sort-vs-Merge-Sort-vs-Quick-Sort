"""Instrumented sorting algorithms for empirical complexity analysis."""

from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter
from typing import Generator


@dataclass(frozen=True)
class SortResult:
    name: str
    sorted_values: list[int]
    comparisons: int
    swaps: int
    elapsed_ms: float


def bubble_sort(values: list[int]) -> SortResult:
    arr = values.copy()
    n = len(arr)
    comparisons = 0
    swaps = 0
    start = perf_counter()

    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            comparisons += 1
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swaps += 1
                swapped = True
        if not swapped:
            break

    elapsed_ms = (perf_counter() - start) * 1000
    return SortResult("Bubble Sort", arr, comparisons, swaps, elapsed_ms)


def merge_sort(values: list[int]) -> SortResult:
    arr = values.copy()
    comparisons = 0
    swaps = 0
    start = perf_counter()

    def merge(left: list[int], right: list[int]) -> list[int]:
        nonlocal comparisons, swaps
        merged: list[int] = []
        i = j = 0
        while i < len(left) and j < len(right):
            comparisons += 1
            if left[i] <= right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1
        merged.extend(left[i:])
        merged.extend(right[j:])
        swaps += len(left) + len(right)
        return merged

    def sort(chunk: list[int]) -> list[int]:
        if len(chunk) <= 1:
            return chunk
        mid = len(chunk) // 2
        left = sort(chunk[:mid])
        right = sort(chunk[mid:])
        return merge(left, right)

    sorted_arr = sort(arr)
    elapsed_ms = (perf_counter() - start) * 1000
    return SortResult("Merge Sort", sorted_arr, comparisons, swaps, elapsed_ms)


def insertion_sort(values: list[int]) -> SortResult:
    arr = values.copy()
    n = len(arr)
    comparisons = 0
    swaps = 0
    start = perf_counter()

    for i in range(1, n):
        key = arr[i]
        j = i - 1
        while j >= 0:
            comparisons += 1
            if arr[j] > key:
                arr[j + 1] = arr[j]
                swaps += 1
                j -= 1
            else:
                break
        arr[j + 1] = key

    elapsed_ms = (perf_counter() - start) * 1000
    return SortResult("Insertion Sort", arr, comparisons, swaps, elapsed_ms)


def selection_sort(values: list[int]) -> SortResult:
    arr = values.copy()
    n = len(arr)
    comparisons = 0
    swaps = 0
    start = perf_counter()

    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            comparisons += 1
            if arr[j] < arr[min_idx]:
                min_idx = j
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            swaps += 1

    elapsed_ms = (perf_counter() - start) * 1000
    return SortResult("Selection Sort", arr, comparisons, swaps, elapsed_ms)


def quick_sort(values: list[int]) -> SortResult:
    arr = values.copy()
    comparisons = 0
    swaps = 0
    start = perf_counter()

    def partition(a: list[int], low: int, high: int) -> int:
        nonlocal comparisons, swaps
        pivot = a[high]
        i = low - 1
        for j in range(low, high):
            comparisons += 1
            if a[j] <= pivot:
                i += 1
                a[i], a[j] = a[j], a[i]
                swaps += 1
        a[i + 1], a[high] = a[high], a[i + 1]
        swaps += 1
        return i + 1

    def sort(a: list[int], low: int, high: int) -> None:
        if low < high:
            pi = partition(a, low, high)
            sort(a, low, pi - 1)
            sort(a, pi + 1, high)

    sort(arr, 0, len(arr) - 1)
    elapsed_ms = (perf_counter() - start) * 1000
    return SortResult("Quick Sort", arr, comparisons, swaps, elapsed_ms)


def heap_sort(values: list[int]) -> SortResult:
    arr = values.copy()
    n = len(arr)
    comparisons = 0
    swaps = 0
    start = perf_counter()

    def heapify(n: int, i: int) -> None:
        nonlocal comparisons, swaps
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2

        if l < n:
            comparisons += 1
            if arr[l] > arr[largest]:
                largest = l

        if r < n:
            comparisons += 1
            if arr[r] > arr[largest]:
                largest = r

        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            swaps += 1
            heapify(n, largest)

    for i in range(n // 2 - 1, -1, -1):
        heapify(n, i)

    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        swaps += 1
        heapify(i, 0)

    elapsed_ms = (perf_counter() - start) * 1000
    return SortResult("Heap Sort", arr, comparisons, swaps, elapsed_ms)


def bubble_sort_steps(values: list[int]) -> Generator[list[int], None, SortResult]:
    arr = values.copy()
    n = len(arr)
    comparisons = 0
    swaps = 0
    start = perf_counter()

    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            comparisons += 1
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swaps += 1
                swapped = True
                yield arr.copy()
        if not swapped:
            break

    elapsed_ms = (perf_counter() - start) * 1000
    return SortResult("Bubble Sort", arr, comparisons, swaps, elapsed_ms)


def insertion_sort_steps(values: list[int]) -> Generator[list[int], None, SortResult]:
    arr = values.copy()
    n = len(arr)
    comparisons = 0
    swaps = 0
    start = perf_counter()

    for i in range(1, n):
        key = arr[i]
        j = i - 1
        while j >= 0:
            comparisons += 1
            if arr[j] > key:
                arr[j + 1] = arr[j]
                swaps += 1
                j -= 1
                yield arr.copy()
            else:
                break
        arr[j + 1] = key
        yield arr.copy()

    elapsed_ms = (perf_counter() - start) * 1000
    return SortResult("Insertion Sort", arr, comparisons, swaps, elapsed_ms)


def selection_sort_steps(values: list[int]) -> Generator[list[int], None, SortResult]:
    arr = values.copy()
    n = len(arr)
    comparisons = 0
    swaps = 0
    start = perf_counter()

    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            comparisons += 1
            if arr[j] < arr[min_idx]:
                min_idx = j
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            swaps += 1
            yield arr.copy()

    elapsed_ms = (perf_counter() - start) * 1000
    return SortResult("Selection Sort", arr, comparisons, swaps, elapsed_ms)


def merge_sort_steps(values: list[int]) -> Generator[list[int], None, SortResult]:
    arr = values.copy()
    comparisons = 0
    swaps = 0
    start = perf_counter()

    def sort_and_yield(l: int, r: int) -> Generator[list[int], None, None]:
        nonlocal comparisons, swaps
        if l >= r:
            return
        m = (l + r) // 2
        yield from sort_and_yield(l, m)
        yield from sort_and_yield(m + 1, r)

        merged = []
        i = l
        j = m + 1
        while i <= m and j <= r:
            comparisons += 1
            if arr[i] <= arr[j]:
                merged.append(arr[i])
                i += 1
            else:
                merged.append(arr[j])
                j += 1
        while i <= m:
            merged.append(arr[i])
            i += 1
        while j <= r:
            merged.append(arr[j])
            j += 1

        swaps += len(merged)
        for idx, val in enumerate(merged):
            arr[l + idx] = val
            yield arr.copy()

    yield from sort_and_yield(0, len(arr) - 1)
    elapsed_ms = (perf_counter() - start) * 1000
    return SortResult("Merge Sort", arr, comparisons, swaps, elapsed_ms)


def quick_sort_steps(values: list[int]) -> Generator[list[int], None, SortResult]:
    arr = values.copy()
    comparisons = 0
    swaps = 0
    start = perf_counter()

    def sort_and_yield(low: int, high: int) -> Generator[list[int], None, None]:
        nonlocal comparisons, swaps
        if low < high:
            pivot = arr[high]
            i = low - 1
            for j in range(low, high):
                comparisons += 1
                if arr[j] <= pivot:
                    i += 1
                    arr[i], arr[j] = arr[j], arr[i]
                    swaps += 1
                    yield arr.copy()
            arr[i + 1], arr[high] = arr[high], arr[i + 1]
            swaps += 1
            yield arr.copy()
            pi = i + 1

            yield from sort_and_yield(low, pi - 1)
            yield from sort_and_yield(pi + 1, high)

    yield from sort_and_yield(0, len(arr) - 1)
    elapsed_ms = (perf_counter() - start) * 1000
    return SortResult("Quick Sort", arr, comparisons, swaps, elapsed_ms)


def heap_sort_steps(values: list[int]) -> Generator[list[int], None, SortResult]:
    arr = values.copy()
    n = len(arr)
    comparisons = 0
    swaps = 0
    start = perf_counter()

    def heapify_and_yield(n: int, i: int) -> Generator[list[int], None, None]:
        nonlocal comparisons, swaps
        largest = i
        l = 2 * i + 1
        r = 2 * i + 2

        if l < n:
            comparisons += 1
            if arr[l] > arr[largest]:
                largest = l

        if r < n:
            comparisons += 1
            if arr[r] > arr[largest]:
                largest = r

        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            swaps += 1
            yield arr.copy()
            yield from heapify_and_yield(n, largest)

    for i in range(n // 2 - 1, -1, -1):
        yield from heapify_and_yield(n, i)

    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        swaps += 1
        yield arr.copy()
        yield from heapify_and_yield(i, 0)

    elapsed_ms = (perf_counter() - start) * 1000
    return SortResult("Heap Sort", arr, comparisons, swaps, elapsed_ms)
