import pandas as pd

def format_input_dataset(file_path, file_format='csv', **kwargs):
    """
    Reads the input dataset and formats it into a standard set of tuples.

    Args:
    - file_path (str): Path to the input dataset file.
    - file_format (str): Format of the input dataset file (csv, excel, json).
    - **kwargs: Additional keyword arguments to pass to the file reader.

    Returns:
    - formatted_data (list of tuples): Standard set of tuples representing the dataset.
    """
    formatted_data = []
    
    if file_format.lower() == 'csv':
        df = pd.read_csv(file_path, **kwargs)
    elif file_format.lower() == 'excel':
        df = pd.read_excel(file_path, **kwargs)
    elif file_format.lower() == 'json':
        df = pd.read_json(file_path, **kwargs)
    else:
        raise ValueError("Unsupported file format. Please provide 'csv', 'excel', or 'json'.")
    
    # Organize the data into tuples
    for index, row in df.iterrows():
        data_tuple = tuple(row)
        formatted_data.append(data_tuple)
    
    return formatted_data

# Example usage:
file_path = 'sample.csv'  # Replace with the path to your dataset file
formatted_data = format_input_dataset(file_path, file_format='csv')
print(formatted_data[:5])  # Print the first few tuples for verification
