# Function to correct if there is duplicated column names (which case the change to a json will fail at the end of calculations)
def rename_duplicate_columns(df):

    new_columns = []
    column_count = {}

    for col in df.columns:
        if col in column_count:
            column_count[col] += 1
            new_columns.append(f"{col}_{column_count[col]}")
        else:
            column_count[col] = 0
            new_columns.append(col)

    df.columns = new_columns
    return df