"""Streamlit frontend: compare all five sorting algorithms on time complexity."""

from __future__ import annotations

import math
import random

# pyrefly: ignore [missing-import]
import streamlit as st

import time

from algorithms import (
    bubble_sort, insertion_sort, merge_sort, quick_sort, selection_sort, heap_sort,
    bubble_sort_steps, insertion_sort_steps, merge_sort_steps, quick_sort_steps, selection_sort_steps, heap_sort_steps
)
from complexity import (
    ALL_PROFILES,
    is_sorted,
    parse_sequence,
    theoretical_operation_estimates,
)

st.set_page_config(
    page_title="Sort Complexity Lab",
    layout="wide",
)

st.title("Sort Complexity Lab")
st.caption(
    "Enter a sequence of integers. The app runs **Bubble Sort**, **Insertion Sort**, "
    "**Selection Sort**, **Merge Sort**, and **Quick Sort** — then shows theoretical "
    "and measured complexity for your input size n."
)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab_analyze, tab_benchmark, tab_animation = st.tabs(["Analyze", "Speed Benchmark", "Step-by-Step Animation"])

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 1 — Analyze
# ═══════════════════════════════════════════════════════════════════════════════
with tab_analyze:

    sample_map = {
        "Random (7 values)": "64, 34, 25, 12, 22, 11, 90",
        "Already sorted": "1, 2, 3, 4, 5, 6, 7",
        "Reverse sorted": "7, 6, 5, 4, 3, 2, 1",
        "Single element": "42",
        "Larger random (15 values)": "38, 7, 91, 45, 23, 60, 14, 77, 5, 88, 32, 50, 19, 66, 3",
    }

    if "sequence" not in st.session_state:
        st.session_state.sequence = sample_map["Random (7 values)"]

    # ── Random generator ──────────────────────────────────────────────────────
    with st.expander("Random Input Generator", expanded=True):
        gen_col1, gen_col2, gen_col3 = st.columns([2, 1, 1])
        with gen_col1:
            rand_count = st.slider(
                "How many numbers to generate?",
                min_value=5,
                max_value=200,
                value=10,
                step=5,
                key="rand_count",
            )
        with gen_col2:
            rand_min = st.number_input("Min value", value=1, step=1, key="rand_min")
        with gen_col3:
            rand_max = st.number_input("Max value", value=999, step=1, key="rand_max")

        if st.button("Generate random numbers", use_container_width=True):
            lo = int(min(rand_min, rand_max))
            hi = int(max(rand_min, rand_max))
            nums = [random.randint(lo, hi) for _ in range(rand_count)]
            st.session_state.sequence = ", ".join(str(x) for x in nums)
            st.rerun()

    # ── Manual / sample input ─────────────────────────────────────────────────
    col_run, col_sample = st.columns([1, 1])
    with col_sample:
        preset = st.selectbox("Sample inputs", list(sample_map.keys()))
        if st.button("Load sample"):
            st.session_state.sequence = sample_map[preset]
            st.rerun()

    raw_input = st.text_area(
        "Number sequence",
        height=90,
        help="Comma- or space-separated integers, e.g. 5, 1, 4, 2, 8",
        key="sequence",
    )

    run = col_run.button("Analyze complexity", type="primary", use_container_width=True)

    if run:
        try:
            sequence = parse_sequence(raw_input)
        except ValueError as err:
            st.error(str(err))
            st.stop()

        n = len(sequence)
        sorted_input = is_sorted(sequence)
        estimates = theoretical_operation_estimates(n, sorted_input)

        bubble    = bubble_sort(sequence)
        insertion = insertion_sort(sequence)
        selection = selection_sort(sequence)
        merge     = merge_sort(sequence)
        quick     = quick_sort(sequence)

        heap      = heap_sort(sequence)

        all_results = [bubble, insertion, selection, merge, quick, heap]
        est_keys = [
            "bubble_comparisons",
            "insertion_comparisons",
            "selection_comparisons",
            "merge_comparisons",
            "quick_comparisons",
            "heap_comparisons",
        ]

        st.success(f"Parsed **n = {n}** values. All algorithms produced identical sorted output.")

        st.subheader("Input")
        st.code(", ".join(str(v) for v in sequence), language="text")

        # Theoretical complexity table
        st.subheader("Theoretical Time Complexity")
        theory_data = {
            "Algorithm": [p.algorithm for p in ALL_PROFILES],
            "Best":      [p.best      for p in ALL_PROFILES],
            "Average":   [p.average   for p in ALL_PROFILES],
            "Worst":     [p.worst     for p in ALL_PROFILES],
            "Space":     [p.space     for p in ALL_PROFILES],
            "Stable":    ["Yes" if p.stable else "No" for p in ALL_PROFILES],
        }
        st.table(theory_data)

        # Measured results
        st.subheader("Measured on Your Input")
        cols = st.columns(len(all_results))
        for col, result, est_key in zip(cols, all_results, est_keys):
            with col:
                st.markdown(f"**{result.name}**")
                st.metric("Comparisons", f"{result.comparisons:,}")
                st.metric("Array writes / moves", f"{result.swaps:,}")
                st.metric("Wall-clock time", f"{result.elapsed_ms:.4f} ms")
                st.metric("Theoretical estimate", f"~{estimates[est_key]:,}")

        # Scaling info
        st.subheader(f"Scaling Comparison for n = {n}")
        if n > 1:
            log_n = math.log2(n)
            n2 = n * n
            n_log_n = int(n * log_n)
            ratio = n2 / n_log_n if n_log_n else float("inf")

            scale_cols = st.columns(3)
            scale_cols[0].metric("n", n)
            scale_cols[1].metric("n² (quadratic)", f"{n2:,}")
            scale_cols[2].metric("n log₂ n (linearithmic)", f"{n_log_n:,}")

            st.info(
                f"For n = {n}, quadratic growth (n² = {n2:,}) is about **{ratio:.1f}×** "
                f"larger than n log₂ n ({n_log_n:,}). "
                "Merge Sort and Quick Sort stay closer to linearithmic; "
                "Bubble, Insertion, and Selection Sort degrade faster as n grows."
            )

        # Growth chart
        st.subheader("Estimated Comparison Growth Near Your n")
        chart_rows = []
        for size in range(max(2, n - 4), n + 11):
            est = theoretical_operation_estimates(size, False)
            chart_rows.append(
                {
                    "n": size,
                    "Bubble / Insertion / Selection (est.)": est["bubble_comparisons"],
                    "Merge Sort (est.)":  est["merge_comparisons"],
                    "Quick Sort (est.)":  est["quick_comparisons"],
                    "Heap Sort (est.)":   est["heap_comparisons"],
                }
            )
        st.line_chart(
            chart_rows,
            x="n",
            y=[
                "Bubble / Insertion / Selection (est.)",
                "Merge Sort (est.)",
                "Quick Sort (est.)",
                "Heap Sort (est.)",
            ],
            height=320,
        )
        st.caption(
            "Chart shows estimated comparison counts for unsorted inputs near your current n. "
            "Empirical counts above reflect your exact sequence."
        )

        st.subheader("Sorted Output")
        st.write(merge.sorted_values)


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 2 — Speed Benchmark
# ═══════════════════════════════════════════════════════════════════════════════
with tab_benchmark:
    st.markdown("### Speed Benchmark Mode")
    st.markdown(
        "Runs all 5 algorithms on **randomly generated inputs** of increasing size "
        "and plots the **actual measured wall-clock time (ms)**."
    )

    b_col1, b_col2 = st.columns([2, 1])
    with b_col1:
        bench_sizes_input = st.text_input(
            "Input sizes to test (comma-separated)",
            value="10, 50, 100, 250, 500, 750, 1000",
            help="e.g. 10, 50, 100, 500, 1000",
        )
    with b_col2:
        bench_runs = st.number_input(
            "Repeats per size (averaged)",
            min_value=1, max_value=10, value=3, step=1,
        )

    skip_slow = st.checkbox(
        "Skip Bubble / Insertion / Selection for sizes > 500 (they become very slow)",
        value=True,
    )

    run_bench = st.button("Run Benchmark", type="primary", use_container_width=True)

    if run_bench:
        try:
            bench_sizes = [int(x.strip()) for x in bench_sizes_input.split(",") if x.strip()]
            if not bench_sizes:
                raise ValueError("Enter at least one size.")
        except ValueError as err:
            st.error(f"Invalid sizes: {err}")
            st.stop()

        SLOW_THRESHOLD = 500

        algo_map = {
            "Bubble Sort":    bubble_sort,
            "Insertion Sort": insertion_sort,
            "Selection Sort": selection_sort,
            "Merge Sort":     merge_sort,
            "Quick Sort":     quick_sort,
            "Heap Sort":      heap_sort,
        }

        progress = st.progress(0, text="Running benchmark…")
        total_steps = len(bench_sizes) * len(algo_map) * int(bench_runs)
        step = 0

        # results[algo_name][size] = avg_ms
        results: dict[str, dict[int, float]] = {name: {} for name in algo_map}

        for size in bench_sizes:
            for algo_name, algo_fn in algo_map.items():
                is_slow_algo = algo_name in ("Bubble Sort", "Insertion Sort", "Selection Sort")
                if skip_slow and is_slow_algo and size > SLOW_THRESHOLD:
                    step += int(bench_runs)
                    progress.progress(
                        min(step / total_steps, 1.0),
                        text=f"Skipping {algo_name} at n={size}…",
                    )
                    continue

                times = []
                for _ in range(int(bench_runs)):
                    data = random.sample(range(1, size * 10 + 1), min(size, size * 10))
                    res = algo_fn(data)
                    times.append(res.elapsed_ms)
                    step += 1
                    progress.progress(
                        min(step / total_steps, 1.0),
                        text=f"Benchmarking {algo_name} at n={size}…",
                    )

                results[algo_name][size] = sum(times) / len(times)

        progress.empty()
        st.success("Benchmark complete!")

        # Build chart rows
        chart_rows = []
        for size in bench_sizes:
            row: dict[str, float | int] = {"n": size}
            for algo_name in algo_map:
                if size in results[algo_name]:
                    row[algo_name] = round(results[algo_name][size], 4)
            chart_rows.append(row)

        st.subheader("Wall-Clock Time (ms) by Input Size")
        available_algos = [
            name for name in algo_map
            if any(name in row for row in chart_rows)
        ]
        st.line_chart(chart_rows, x="n", y=available_algos, height=380)

        # Summary table
        st.subheader("Benchmark Results Table (avg ms)")
        table_data: dict[str, list] = {"Input size (n)": bench_sizes}
        for algo_name in algo_map:
            table_data[algo_name] = [
                f"{results[algo_name][s]:.4f}" if s in results[algo_name] else "skipped"
                for s in bench_sizes
            ]
        st.table(table_data)

        # Winner per size
        st.subheader("Fastest Algorithm per Input Size")
        winner_cols = st.columns(min(len(bench_sizes), 5))
        for i, size in enumerate(bench_sizes):
            col = winner_cols[i % len(winner_cols)]
            size_results = {k: v[size] for k, v in results.items() if size in v}
            if size_results:
                winner = min(size_results, key=size_results.get)
                col.metric(f"n = {size}", winner, f"{size_results[winner]:.4f} ms")


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 3 — Step-by-Step Animation
# ═══════════════════════════════════════════════════════════════════════════════
with tab_animation:
    st.markdown("### Step-by-Step Animation")
    st.markdown("Watch the array being sorted in real-time.")

    anim_algo = st.selectbox("Algorithm", ["Bubble Sort", "Insertion Sort", "Selection Sort", "Merge Sort", "Quick Sort", "Heap Sort"], key="anim_algo")
    anim_n = st.slider("Array Size (N <= 100)", min_value=10, max_value=100, value=30, step=5, key="anim_n")
    anim_speed = st.slider("Animation Speed (ms delay)", min_value=0, max_value=200, value=30, step=10, key="anim_speed")

    if st.button("Start Animation", type="primary"):
        data = list(range(1, anim_n + 1))
        random.shuffle(data)

        algo_map_steps = {
            "Bubble Sort": bubble_sort_steps,
            "Insertion Sort": insertion_sort_steps,
            "Selection Sort": selection_sort_steps,
            "Merge Sort": merge_sort_steps,
            "Quick Sort": quick_sort_steps,
            "Heap Sort": heap_sort_steps,
        }

        chart_placeholder = st.empty()
        status_placeholder = st.empty()

        gen = algo_map_steps[anim_algo](data)
        steps_count = 0

        while True:
            try:
                state = next(gen)
                chart_placeholder.bar_chart(state)
                steps_count += 1
                status_placeholder.text(f"Steps: {steps_count}")
                time.sleep(anim_speed / 1000.0)
            except StopIteration as e:
                res = e.value
                status_placeholder.success(f"Finished in {steps_count} visual updates! Comparisons: {res.comparisons}, Swaps: {res.swaps}")
                break



