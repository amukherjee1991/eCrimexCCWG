import pandas as pd
import sys
import os

# Check if the correct number of arguments are provided
if len(sys.argv) < 3:
    print("Usage: python script.py <path_to_csv> <output_directory>")
    sys.exit(1)

# File path and output directory from command-line arguments
file_path = sys.argv[1]
output_directory = sys.argv[2]

# Ensure the output directory exists
output_directory = os.path.join(output_directory, 'files_by_source')
os.makedirs(output_directory, exist_ok=True)

# Load the dataset
df = pd.read_csv(file_path)

# Summarize the data
summary = df.describe(include='all')

# Print summary of the data
print("Data Summary:")
print(summary)

# Get the last row for each source
last_rows = df.groupby('source').tail(1)

# Print the last rows for each source
print("\nLast Rows for Each Source:")
print(last_rows)

# Split the dataset by source and save them as CSV
unique_sources = df['source'].unique()
for source in unique_sources:
    # Filter the dataframe by source
    filtered_df = df[df['source'] == source]
    # Define the file name, ensuring valid filename
    file_name = f'{source}.csv'.replace(" ", "_").replace("/", "_")
    full_path = os.path.join(output_directory, file_name)
    # Save the filtered dataframe to CSV
    filtered_df.to_csv(full_path, index=False)
    print(f"Saved {full_path}")
