# Excel Grouper with Merging Options

This is a Streamlit web app for grouping Excel data by selected columns and merging values with custom delimiters.

## Features

- Upload an Excel `.xlsx` file (must have a single sheet named `Sheet1`)
- Delete unwanted columns before processing
- Group by any combination of columns
- Merge unique values of selected columns using a chosen delimiter
- Download the processed, grouped data as a new Excel file

## Requirements

- Python **3.8** or higher
- [`streamlit`](https://streamlit.io/)
- [`pandas`](https://pandas.pydata.org/)
- [`openpyxl`](https://openpyxl.readthedocs.io/)

Install dependencies with:

```bash
pip install streamlit pandas openpyxl
```

## Usage

Run the app with:

```bash
streamlit run streamlit_excel_grouper.py
```

Then open the link provided in your browser.

## Notes

- Uploaded Excel files **must** have a sheet named `Sheet1`
- The app allows you to select which columns to delete, group by, and merge
- The merged columns will contain unique values joined by your chosen delimiter

---
