# Sort Complexity Lab

Python project: compare **Bubble Sort** vs **Merge Sort** time complexity.

## Folder structure

```
sort-complexity/
├── app.py              # Streamlit UI (frontend)
├── algorithms.py       # Bubble & merge sort with metrics
├── complexity.py       # Input parsing + O() theory
├── requirements.txt    # Dependencies
├── run.sh              # One-command start (Mac/Linux)
├── README.md
├── .gitignore
└── .vscode/
    ├── settings.json   # Python interpreter
    └── launch.json     # F5 to run app
```

## Open in VS Code

1. **File → Open Folder**
2. Select the `sort-complexity` folder
3. Open terminal and run:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Or on Mac/Linux:

```bash
chmod +x run.sh
./run.sh
```

4. Open **http://localhost:8501**

## Files

| File | Purpose |
|------|---------|
| `app.py` | Web UI: input numbers, show complexity results |
| `algorithms.py` | Sorting + count comparisons, swaps, time |
| `complexity.py` | Parse input, theoretical O(n), O(n²), O(n log n) |
