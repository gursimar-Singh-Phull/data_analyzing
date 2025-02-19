import pandas as pd
import os
import matplotlib.pyplot as plt

# Initialize empty lists for file paths and DataFrames
file_paths = []
dataframes = []

# Loop to get file paths
while True:
    try:
        # Take input for file path
        file = input("Enter the path of the file (use CNTRL+SHIFT+C to copy path): ").strip()
        file = file.strip('"').strip("'")  # Remove surrounding quotes
        file = os.path.abspath(file)  # Normalize path
        print(f"Debug: Processed file path - {file}")
        
        # Check if the file exists
        if os.path.exists(file):
            file_paths.append(file)
            print(f"File '{file}' added successfully.")
        else:
            print(f"Error: The file '{file}' does not exist. Please check the path.")
        
        # Ask if the user wants to continue
        cont = input("Press 'y' to add another file or any other key to stop: ").lower()
        if cont != 'y':
            break
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        break

# Read files into DataFrames
for file in file_paths:
    try:
        if file.endswith('.csv'):
            temp_df = pd.read_csv(file)
        elif file.endswith('.xlsx') or file.endswith('.xls'):
            temp_df = pd.read_excel(file)
        elif file.endswith('.json'):
            temp_df = pd.read_json(file)
        else:
            print(f"Unsupported file format: {file}")
            continue
        dataframes.append(temp_df)
        print(f"File '{file}' read successfully.")
    except Exception as e:
        print(f"Error reading {file}: {e}")

# Concatenate all DataFrames
if dataframes:
    concatenated_df = pd.concat(dataframes, ignore_index=True)
    print(concatenated_df)
    print(f"Columns available: {concatenated_df.columns.tolist()}")

    # Ask for grouping and numeric columns
    groupby_column = input("Enter the column name to group by (e.g., Category): ")
    numeric_columns = input("Enter the numeric column(s) to analyze (separated by comma if multiple): ").split(',')
    numeric_columns = [col.strip() for col in numeric_columns]  # Clean whitespace

    # Verify all columns exist
    if groupby_column in concatenated_df.columns and all(col in concatenated_df.columns for col in numeric_columns):
        # Create a figure with subplots for each numeric column
        n_cols = len(numeric_columns)
        fig, axes = plt.subplots(n_cols, 1, figsize=(12, 6*n_cols))
        if n_cols == 1:
            axes = [axes]  # Make axes iterable when there's only one subplot

        for i, numeric_column in enumerate(numeric_columns):
            # Group by column and aggregate the numeric column
            grouped_df = concatenated_df.groupby(groupby_column)[numeric_column].agg(['sum', 'max', 'min']).reset_index()
            print(f"\nGrouped Data for {numeric_column}:")
            print(grouped_df)
            
            # Plotting
            ax = axes[i]
            
            # Line graph for max and min
            ax.plot(grouped_df[groupby_column], grouped_df['max'], label='Max', marker='o', color='blue')
            ax.plot(grouped_df[groupby_column], grouped_df['min'], label='Min', marker='o', color='red')
            
            # Bar chart for sum
            ax.bar(grouped_df[groupby_column], grouped_df['sum'], alpha=0.5, label='Sum', color='green')
            
            ax.set_title(f"Analysis of {numeric_column} by {groupby_column}", fontsize=12)
            ax.set_xlabel(groupby_column, fontsize=10)
            ax.set_ylabel(numeric_column, fontsize=10)
            ax.legend()
            ax.grid(alpha=0.3)
            ax.tick_params(axis='x', rotation=45)

        plt.tight_layout()
        plt.show()
    else:
        print("Error: One or more specified columns not found in the DataFrame.")
else:
    print("No valid files were processed.")

