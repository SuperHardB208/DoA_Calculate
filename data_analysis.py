import os
import pandas as pd
import numpy as np

# Set the path of the folder containing txt files and the output Excel filename
txt_folder = ''
output_excel = ''

# Initialize an empty dictionary to store all data
data_dict = {}

# Iterate through all txt files in the folder
for filename in os.listdir(txt_folder):
    if filename.endswith('.txt'):
        file_path = os.path.join(txt_folder, filename)
        
        # Use the first word of the filename as the y-column name
        y_column_name = filename.split()[0]
        
        # Open and read the file
        with open(file_path, 'r') as f:
            for line in f:
                try:
                    # Split by comma and extract x and y
                    x_value, y_value = line.strip().split(',', 1)
                    x_value = float(x_value)  # Assume x is numeric
                    y_value = float(y_value)  # Assume y is numeric
                    
                    # Adjust x value to circular angles
                    if x_value < 0:
                        x_value += 180  # Convert negative angles to positive
                    elif x_value <= 2.5:
                        x_value = 177.5  # Convert angles from 0 to 2.5 to 177.5
                
                    # If x value not in dictionary, initialize it
                    if x_value not in data_dict:
                        data_dict[x_value] = {}
                    
                    # Store the y value under the column named after the file
                    data_dict[x_value][y_column_name] = y_value
                
                except ValueError:
                    # Skip the line if x or y cannot be parsed as a number
                    print(f"Skipping unparseable line: {line.strip()}")
                    continue

# Convert the dictionary into a DataFrame
df_final = pd.DataFrame.from_dict(data_dict, orient='index').reset_index().rename(columns={'index': 'x'})

# Replace NaN with 0 (no corresponding y value)
df_final.fillna(0, inplace=True)

# Normalize each column: divide all values in each column by the column sum
for column in df_final.columns[1:]:  # Skip the first column 'x'
    column_sum = df_final[column].sum()
    if column_sum != 0:  # Avoid division by zero
        df_final[column] = df_final[column] / column_sum

# Define circular 5-degree bins from -2.5 to 180
bins = np.arange(-2.5, 182.5, 5)  # From -2.5 to 180.5, step = 5
labels = np.arange(0, 180, 5)     # Labels from 0, stepping by 5, total 36 labels

# Use pd.cut to create bins based on the defined intervals
df_final['bin'] = pd.cut(df_final['x'], bins=bins, labels=labels, include_lowest=True)

# Create a DataFrame to store the summed results for each bin
df_binned = pd.DataFrame({'bin': labels})  # Preserve the number of labels

# Sum y-values within each bin for every column
for column in df_final.columns[1:-1]:  # Skip 'x' and 'bin'
    binned_sums = df_final.groupby('bin')[column].sum().reindex(df_binned['bin']).reset_index(drop=True)
    
    # Store results in the new DataFrame
    df_binned[column] = binned_sums

# Save results to Excel
df_binned.to_excel(output_excel, index=False)

print(f"Data has been successfully saved to {output_excel}")
