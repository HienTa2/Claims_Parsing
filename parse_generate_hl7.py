import json
import csv
import logging
import socket
from pathlib import Path

# Configure logging
logging.basicConfig(filename='hl7_parser.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def log_error(message):
    logging.error(message)
    print(f"Error: {message}")

def log_info(message):
    logging.info(message)
    print(message)

def validate_hl7(segments):
    """
    Validates HL7 file structure.
    """
    required_segments = ["MSH", "PID", "OBR", "OBX"]
    errors = []

    # Check for required segments
    for segment in required_segments:
        if not any(s.startswith(segment) for s in segments):
            errors.append(f"Missing required segment: {segment}")

    # Validate field counts for specific segments
    for segment in segments:
        parts = segment.split("|")
        if segment.startswith("MSH") and len(parts) < 12:
            errors.append("Invalid MSH segment: Missing required fields.")
        if segment.startswith("PID") and len(parts) < 8:
            errors.append("Invalid PID segment: Missing required fields.")

    return errors

def write_json(data, output_path):
    """
    Writes parsed data to a JSON file.
    """
    with open(output_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4)

def write_csv(observations, output_path):
    """
    Writes observation details to a CSV file.
    """
    with open(output_path, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["Test Name", "Result", "Units", "Reference Range"])
        writer.writeheader()
        writer.writerows(observations)

def parse_and_analyze_hl7(file_path, output_json, output_csv):
    """
    Parses and analyzes an HL7 file. Outputs JSON and CSV files for structured data.
    """
    try:
        input_path = Path(file_path)
        if not input_path.exists():
            log_error(f"File not found: {file_path}")
            return

        log_info(f"Reading HL7 file: {file_path}")
        with input_path.open('r') as input_file:
            content = input_file.read().strip()
            segments = content.split("\n")

        # Validate HL7 structure
        errors = validate_hl7(segments)
        if errors:
            log_error("Validation errors found:")
            for error in errors:
                log_error(error)
            return

        # Parse HL7 segments
        parsed_segments = []
        observations = []

        for segment in segments:
            if segment.strip():
                parts = segment.split("|")
                segment_type = parts[0]

                if segment_type == "MSH":  # Message Header
                    sending_app = parts[2]
                    receiving_app = parts[4]
                    message_type = parts[8]
                    parsed_segments.append({"Segment": "MSH", "Message Type": message_type, "From": sending_app, "To": receiving_app})

                elif segment_type == "PID":  # Patient Information
                    patient_name = parts[5].replace("^", " ")
                    dob = parts[7]
                    gender = parts[8]
                    parsed_segments.append({"Segment": "PID", "Patient Name": patient_name, "DOB": dob, "Gender": gender})

                elif segment_type == "OBR":  # Observation Request
                    order_number = parts[3]
                    test_name = parts[4]
                    parsed_segments.append({"Segment": "OBR", "Order Number": order_number, "Test Name": test_name})

                elif segment_type == "OBX":  # Observation Result
                    test_name = parts[3]
                    result = parts[5]
                    units = parts[6]
                    reference_range = parts[7]
                    observations.append({
                        "Test Name": test_name,
                        "Result": result,
                        "Units": units,
                        "Reference Range": reference_range
                    })

        # Save structured data to JSON and CSV
        write_json(parsed_segments, output_json)
        write_csv(observations, output_csv)

        log_info(f"Parsing complete. JSON: {output_json}, CSV: {output_csv}")
        log_info("Summary of Observations:")
        for obs in observations:
            log_info(f"  Test Name: {obs['Test Name']}, Result: {obs['Result']} {obs['Units']} (Reference: {obs['Reference Range']})")

    except Exception as e:
        log_error(f"An unexpected error occurred: {e}")

def process_real_time_hl7(port):
    """
    Processes HL7 messages in real-time from a given port.
    """
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(("0.0.0.0", port))
        server_socket.listen(1)
        log_info(f"Listening for HL7 messages on port {port}...")

        while True:
            conn, addr = server_socket.accept()
            log_info(f"Connection established with {addr}")
            data = conn.recv(4096).decode("utf-8").strip()  # Increase buffer size if needed
            if data:
                log_info("HL7 message received.")
                segments = data.split("\n")
                # Validate and parse segments dynamically
                errors = validate_hl7(segments)
                if errors:
                    log_error("Validation errors in real-time message:")
                    for error in errors:
                        log_error(error)
                    continue  # Skip further processing for invalid messages

                # Log parsed observations inline
                observations = []
                for segment in segments:
                    parts = segment.split("|")
                    if segment.startswith("OBX"):  # Observations
                        test_name = parts[3]
                        result = parts[5]
                        units = parts[6]
                        reference_range = parts[7]
                        observations.append({
                            "Test Name": test_name,
                            "Result": result,
                            "Units": units,
                            "Reference Range": reference_range
                        })

                log_info("Real-time Observations:")
                for obs in observations:
                    log_info(f"  Test Name: {obs['Test Name']}, Result: {obs['Result']} {obs['Units']} (Reference: {obs['Reference Range']})")

            conn.close()
    except Exception as e:
        log_error(f"An error occurred in real-time processing: {e}")

# Usage
# Parse and analyze a static HL7 file
file_path = 'hL7/sample_oru.hl7'  # Replace with your file path
output_json = 'hl7/output_hl7.json'
output_csv = 'hl7/output_hl7.csv'
parse_and_analyze_hl7(file_path, output_json, output_csv)

# Uncomment to enable real-time HL7 processing
# process_real_time_hl7(12345)  # Replace 12345 with your desired port
