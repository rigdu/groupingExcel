import streamlit as st
import pandas as pd

# Set the app title
st.title("Excel Grouper with Merging Options")

# UI: File uploader for Excel files
uploaded_file = st.file_uploader("Upload your Excel file (.xlsx)", type=["xlsx"])

if uploaded_file:
    try:
        # Read Excel file and check for "Sheet1"
        xls = pd.ExcelFile(uploaded_file)
        if "Sheet1" not in xls.sheet_names:
            st.error("The file must have only one sheet named 'Sheet1'.")
        else:
            # Read the data from Sheet1
            df = pd.read_excel(xls, sheet_name="Sheet1")

            st.success("File successfully uploaded and read.")
            st.subheader("Column Headers Found:")
            st.write(list(df.columns))

            # Select columns to delete
            cols_to_delete = st.multiselect(
                "Select columns to DELETE", 
                options=list(df.columns)
            )

            # If the user selected columns to delete, drop them from the dataframe
            if cols_to_delete:
                df = df.drop(columns=cols_to_delete)

            # Allow user to select columns to group by
            group_by_cols = st.multiselect(
                "Select columns to GROUP BY", 
                options=list(df.columns)
            )
            # Allow user to choose delimiter for merging
            delimiter = st.selectbox(
                "Select delimiter for merging grouped values", 
                options=[", ", " | ", "; ", " / ", "||"]
            )

            # Allow user to select columns to merge, excluding those used for grouping
            merge_columns = st.multiselect(
                "Select columns to MERGE (join unique values)", 
                options=[col for col in df.columns if col not in group_by_cols]
            )

            # Button to process the grouping and merging
            if st.button("Process Grouping"):
                if not group_by_cols:
                    st.warning("Please select at least one column to group by.")
                else:
                    # Function to join unique, non-null values with the selected delimiter
                    def merge_unique(series):
                        return delimiter.join(sorted(set(map(str, series.dropna()))))

                    # Group by selected columns and merge selected columns
                    grouped_df = df.groupby(group_by_cols, dropna=False).agg({
                        col: merge_unique for col in merge_columns
                    }).reset_index()

                    # For other columns, keep the first value found for each group
                    keep_cols = [col for col in df.columns if col not in merge_columns + group_by_cols]
                    if keep_cols:
                        first_values = df.groupby(group_by_cols, dropna=False)[keep_cols].first().reset_index()
                        grouped_df = pd.merge(grouped_df, first_values, on=group_by_cols, how="left")

                    # Rearrange columns: group by columns, then merged columns, then the rest
                    final_cols = group_by_cols + merge_columns + keep_cols
                    grouped_df = grouped_df[final_cols]

                    st.success("Data grouped and merged successfully!")
                    st.dataframe(grouped_df)

                    # Download button for the processed data as Excel
                    st.download_button(
                        label="Download Grouped Data as Excel",
                        data=grouped_df.to_excel(index=False, engine="openpyxl"),
                        file_name="grouped_output.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
