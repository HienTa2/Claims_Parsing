# **Claims_Parsing**

## **Overview**
The **Claims_Parsing** project provides tools to parse, analyze, and reconcile healthcare EDI files (e.g., 837, 835) and HL7 messages. It helps developers and healthcare administrators process claims, generate reconciliation reports, and handle HL7 communication efficiently.

This project includes:
- **837 File Parsing:** Extract claims details.
- **835 File Parsing:** Extract payment details and adjustments.
- **837-835 Matching:** Reconcile claims with their corresponding remittances.
- **HL7 Processing:** Parse HL7 files to extract patient and observation data.

---

## **Project Structure**
```plaintext
Claims_Parsing/
├── .venv/                    # Virtual environment for dependencies
├── 835/                      # Sample 835 files
│   └── sample_835.txt        # Example EDI 835 file for testing
├── 837/                      # Sample 837 files
│   └── sample_837.txt        # Example EDI 837 file for testing
├── Claim_Scripts/            # Python scripts for claims processing
│   ├── match_837_835.py      # Script to reconcile 837 claims with 835 payments
│   ├── parse_837.py          # Script to parse 837 files
│   └── parse_generate_hl7.py # Script to parse and generate HL7 files
├── hl7/                      # Sample HL7 files
│   └── sample_oru.hl7        # Example HL7 ORU file
├── .gitignore                # Ignored files and directories
├── hl7_parser.log            # Log file for HL7 processing
├── LICENSE                   # Project license (to be specified)
└── README.md                 # Project documentation


