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
    numeric_column = input("Enter the numeric column to analyze (e.g., Sales): ")

    if groupby_column in concatenated_df.columns and numeric_column in concatenated_df.columns:
        # Group by column and aggregate the numeric column
        grouped_df = concatenated_df.groupby(groupby_column)[numeric_column].agg(['sum', 'max', 'min']).reset_index()
        print("\nGrouped Data:")
        print(grouped_df)
        
        # Plotting the grouped data
        plt.figure(figsize=(10, 6))
        
        # Line graph for max and min
        plt.plot(grouped_df[groupby_column], grouped_df['max'], label='Max Values', marker='o', color='blue')
        plt.plot(grouped_df[groupby_column], grouped_df['min'], label='Min Values', marker='o', color='red')
        
        # Bar chart for sum
        plt.bar(grouped_df[groupby_column], grouped_df['sum'], alpha=0.5, label='Sum Values', color='green')
        
        plt.title(f"Analysis of {numeric_column} by {groupby_column}", fontsize=16)
        plt.xlabel(groupby_column, fontsize=14)
        plt.ylabel(numeric_column, fontsize=14)
        plt.legend()
        plt.grid(alpha=0.3)
        plt.xticks(rotation=45)  # Rotate x-axis labels if necessary
        plt.tight_layout()
        plt.show()
    else:
        print("Error: Specified columns not found in the DataFrame.")
else:
    print("No valid files were processed.")

