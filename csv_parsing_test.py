import csv

with open('training_csv_file.csv', mode='r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_start = 0
    row_count = 0
    columns = []
    columns_string = "Columns: "
    for row in csv_reader:
        if(line_start == 4 and not row[0] in (None, "")):
            for item in row:
                if not item in (None, "", " "):
                    columns_string = columns_string + item + ' '
            print(columns_string)
            columns = row

        elif(row == columns):
            continue

        elif(line_start>4 and not row[0] in (None, "")):
            row_count += 1
            row_string = 'Row '+str(row_count)+': '
            for item in row:
                if not item in (None, "", " "):
                    row_string = row_string + item + ' '
            print(row_string)
        line_start += 1
    print(f'Processed {row_count} rows')



