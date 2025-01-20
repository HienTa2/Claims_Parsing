import re
from pathlib import Path

def parse_837(file_path):
    """
    Parses an 837 file and extracts claims into a dictionary.
    Returns a dictionary of claims with Claim ID as the key.
    """
    claims = {}
    try:
        input_path = Path(file_path)
        if not input_path.exists():
            print(f"Error: Input file '{file_path}' does not exist.")
            return claims

        with input_path.open('r') as input_file:
            content = input_file.read()
            segments = re.split(r'~\n?', content)

        for segment in segments:
            if segment.startswith("CLM"):  # Claim Information
                parts = segment.split("*")
                claims[parts[1]] = {
                    "Claim ID": parts[1],
                    "Amount Billed": parts[2],
                    "Claim Type": parts[5]
                }
        return claims
    except Exception as e:
        print(f"Error parsing 837 file: {e}")
        return claims

def parse_835(file_path):
    """
    Parses an 835 file and extracts payments into a dictionary.
    Returns a dictionary of payments with Claim ID as the key.
    """
    payments = {}
    try:
        input_path = Path(file_path)
        if not input_path.exists():
            print(f"Error: Input file '{file_path}' does not exist.")
            return payments

        with input_path.open('r') as input_file:
            content = input_file.read()
            segments = re.split(r'~\n?', content)

        for segment in segments:
            if segment.startswith("CLP"):  # Payment Information
                parts = segment.split("*")
                payments[parts[1]] = {
                    "Claim ID": parts[1],
                    "Amount Billed": parts[3],
                    "Amount Paid": parts[4],
                    "Adjustment": parts[5]
                }
        return payments
    except Exception as e:
        print(f"Error parsing 835 file: {e}")
        return payments

def match_837_835(claims_file, payments_file, output_file_path):
    """
    Matches claims in the 837 file with payments in the 835 file.
    Outputs a reconciliation summary to a file.
    """
    claims = parse_837(claims_file)
    payments = parse_835(payments_file)

    unmatched_claims = []
    reconciliation = []

    for claim_id, claim_data in claims.items():
        if claim_id in payments:
            payment_data = payments[claim_id]
            reconciliation.append({
                "Claim ID": claim_id,
                "Amount Billed (837)": claim_data["Amount Billed"],
                "Amount Paid (835)": payment_data["Amount Paid"],
                "Adjustment (835)": payment_data["Adjustment"]
            })
        else:
            unmatched_claims.append(claim_data)

    # Write reconciliation summary to file
    try:
        output_path = Path(output_file_path)
        with output_path.open('w', encoding='utf-8') as output_file:
            output_file.write("Reconciliation Summary:\n")
            for match in reconciliation:
                output_file.write(f"Claim ID: {match['Claim ID']}, "
                                  f"Amount Billed (837): ${match['Amount Billed (837)']}, "
                                  f"Amount Paid (835): ${match['Amount Paid (835)']}, "
                                  f"Adjustment (835): ${match['Adjustment (835)']}\n")

            output_file.write("\nUnmatched Claims (837):\n")
            for claim in unmatched_claims:
                output_file.write(f"Claim ID: {claim['Claim ID']}, Amount Billed: ${claim['Amount Billed']}\n")

        print(f"Reconciliation report saved to: {output_file_path}")
    except Exception as e:
        print(f"Error writing reconciliation report: {e}")

# Usage
claims_file_path = '../837/sample_837.txt'  # Path to the 837 file
payments_file_path = '../835/sample_835.txt'  # Path to the 835 file
output_file_path = '../835/reconciliation_report.txt'  # Path to save the reconciliation report
match_837_835(claims_file_path, payments_file_path, output_file_path)
