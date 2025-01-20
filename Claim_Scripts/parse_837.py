import re
from pathlib import Path

def parse_and_analyze_837(file_path, output_file_path):
    """
    Parses and analyzes an 837 EDI file. Extracts patient, claim, provider, and service details.
    Outputs a detailed summary and preserves segment terminators (~).
    """
    try:
        input_path = Path(file_path)
        output_path = Path(output_file_path)

        if not input_path.exists():
            print(f"Error: Input file '{file_path}' does not exist.")
            return

        print(f"Reading input file: {file_path}")
        with input_path.open('r') as input_file:
            content = input_file.read()
            segments = re.split(r'~\n?', content)

        # Initialize structures for analysis
        claims = []
        parsed_segments = []

        for segment in segments:
            if segment.strip():
                # Add segment to parsed output (preserve ~)
                parsed_segments.append(segment.strip() + '~')

                # Analyze specific segments
                if segment.startswith("CLM"):  # Claim Information
                    parts = segment.split("*")
                    claims.append({
                        "Claim ID": parts[1],
                        "Amount Billed": parts[2],
                        "Claim Type": parts[5]
                    })
                    parsed_segments.append(f"--> Claim ID: {parts[1]}, Amount Billed: {parts[2]}, Type: {parts[5]}")

                if segment.startswith("NM1*IL"):  # Patient Information
                    parts = segment.split("*")
                    parsed_segments.append(f"--> Patient Name: {parts[3]} {parts[4]}")

                if segment.startswith("DTP") and "472" in segment:  # Service Date
                    parts = segment.split("*")
                    parsed_segments.append(f"--> Service Date: {parts[3]}")

                if segment.startswith("NM1*85"):  # Provider Information
                    parts = segment.split("*")
                    parsed_segments.append(f"--> Provider: {parts[3]}")

                if segment.startswith("HI"):  # Diagnosis Codes
                    parts = segment.split("*")
                    diagnosis_code = parts[1].split(":")[1]
                    parsed_segments.append(f"--> Diagnosis Code: {diagnosis_code}")

                if segment.startswith("SV1"):  # Procedure Codes
                    parts = segment.split("*")
                    procedure_code = parts[1].split(":")[1]
                    parsed_segments.append(f"--> Procedure Code: {procedure_code}, Amount Charged: {parts[2]}")

        # Write parsed segments to output file
        with output_path.open('w', encoding='utf-8') as output_file:
            output_file.write("\n".join(parsed_segments) + "\n")

        print(f"Output file generated successfully: {output_file_path}")

        print("\nSummary of Claims:")
        for claim in claims:
            print(f"  Claim ID: {claim['Claim ID']}, Amount: ${claim['Amount Billed']}, Type: {claim['Claim Type']}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Usage
file_path_global = '../837/sample_837.txt'  # Path to your input file
output_file_path = '../837/output_837_segments_analyzed.txt'  # Path to save the output
parse_and_analyze_837(file_path_global, output_file_path)
