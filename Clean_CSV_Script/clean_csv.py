import csv

# Open the CSV file to clean
with open("v1 HCAHPS 2022.csv", "r") as infile, open("cleaned_HCAHPS_2022.csv", "w", newline="") as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    for row in reader:
        # Ensure each row has the correct number of columns
        if len(row) == 16:  # Adjust to your actual number of columns
            writer.writerow(row)
        else:
            print(f"Row misaligned: {row}")  # Debugging info
