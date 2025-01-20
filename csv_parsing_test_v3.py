import csv

FIRST_COLUMN_HEADER = 'Patient Name' # First column header that appears in the file
INVALID_RECORD = [None, FIRST_COLUMN_HEADER, ''] # Rows that start with these values are not a complete patient record

def process_csv(file_path):
    '''
    Processes the given CSV file, skipping metadata and printing the column headers and rows.
    
    Args:
        file_path (str): The path to the CSV file to be processed.
    '''
    try:
        with open(file_path, mode='r', newline='') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            column_headers_obtained = False # flag to track if the column headers have been read
            record_count = 0
            patient_records = {}
            
            for row in csv_reader:
                # Skip metadata lines until column headers are reached in file
                if row[0] != FIRST_COLUMN_HEADER and not column_headers_obtained:
                    continue

                # Parse column headers
                if row[0] == FIRST_COLUMN_HEADER and not column_headers_obtained:
                    print(list(filter(None, row)))
                    column_headers_obtained = True
                
                # Parse records 
                if row[0] not in INVALID_RECORD and column_headers_obtained:
                    patient_records[record_count] = list(filter(None, row))
                    record_count += 1

                # Get city and state address in multi-line data and add to address in row(s) above
                if row[0] == '' and column_headers_obtained:
                    if any(row) and patient_records:
                        address_list = list(filter(None, row))
                        for item in address_list:
                            patient_records[record_count-1][9] += ' ' + item

            # Output patient records
            for value in patient_records.values():
                print(value)

            # Print the total number of processed records
            print(f'\nProcessed {record_count} records')

    except FileNotFoundError:
        print(f'Error: The file "{file_path}" was not found.')
    
    except csv.Error as e:
        print(f'Error: There was an issue with CSV parsing: {e}')
    
    except Exception as e:
        print(f'An unexpected error occurred: {e}')

# Example usage
process_csv('training_csv_file.csv')
