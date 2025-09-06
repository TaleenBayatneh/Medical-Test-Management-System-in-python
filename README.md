#  Medical Test Management System  

A robust **Python-based command-line application** for managing medical test definitions and patient records.  
Built with object-oriented principles, it features comprehensive data validation, advanced filtering, reporting, and data portability.  

---

##  Features  

### Core Management  
- **Medical Test Catalog**: Define and manage medical tests, including their normal ranges, units, and turnaround times.  
- **Patient Records**: Create, read, update, and delete patient test records.  
- **Data Validation**: Ensures data integrity with strict validation for IDs, names, dates, numerical values, and units.  

### Advanced Functionality  
- **Smart Filtering & Search**: Find records using multiple criteria like Patient ID, test name, status, date ranges, and abnormal results.  
- **Summary Reports**: Generate statistical reports showing min, max, and average values for test results and turnaround times.  
- **Data Portability**: Import and export records to/from CSV files for easy data exchange.  

---

##  Usage

When you run the script, you will see the main menu, choose one of them and you will get the operation you want:

```
Medical Test Management System
1. Add New Medical Test
2. Add Test Record
3. Update Patient Record
4. Update Medical Test
5. Filter Medical Tests
6. Generate Summary Report
7. Export to CSV
8. Import from CSV
9. Exit
```

---

###  Key Operations  

- **Adding a Test (Option 1)**  
  Define a new type of medical test. The system will ask for:  
  - **Test name** (e.g., "Vitamin D")  
  - **Normal range** (e.g., `20-50`)  
  - **Unit** (e.g., `ng/mL`)  
  - **Turnaround time** (e.g., `02-12-30` → 2 days, 12 hours, 30 minutes)  
  Each test is stored in `medicalTest.txt` and validated for proper formatting.  

- **Adding a Record (Option 2)**  
  Log a new test result for a patient. The system validates:  
  - Patient ID (7-digit number only)  
  - Test name (must exist in the catalog)  
  - Date format (`YYYY-MM-DD HH:MM`)  
  - Result value (numeric)  
  - Unit (must match the test type)  
  - Status (pending, completed, or reviewed)  
  Records are stored in `medicalRecord.txt`.  

- **Updating Patient Records (Option 3)**  
  Modify an existing test record for a patient. You can update:  
  - Test result values  
  - Test status (e.g., from *pending* → *completed*)  
  - Date/time of the test  
  - Any incorrect or outdated information  

- **Updating Medical Tests (Option 4)**  
  Edit an existing medical test definition. This is useful when:  
  - Normal ranges need to be adjusted  
  - Units change (e.g., mg/dL → mmol/L)  
  - Turnaround time is updated  

- **Filtering Records (Option 5)**  
  Search patient records using one or multiple filters:  
  - By Patient ID  
  - By Test Name (e.g., all "Hgb" tests)  
  - By Status (pending, completed, reviewed)  
  - By Date Range (e.g., last week, last month)  
  - By Abnormal Results (outside the normal range)  
  Filtering makes it easy to find trends and specific cases.  

- **Generating Reports (Option 6)**  
  Create a **summary report** for filtered records. The report includes:  
  - Minimum, maximum, and average test values  
  - Average turnaround time  
  - Number of abnormal results  
  - Statistics grouped by test type  

- **Exporting to CSV (Option 7)**  
  Save filtered or all patient records to a `.csv` file. This makes it easy to:  
  - Share data with other applications  
  - Analyze results in Excel or Google Sheets  

- **Importing from CSV (Option 8)**  
  Load patient records from a `.csv` file into the system. This allows:  
  - Bulk uploading of records  
  - Integration with external databases  
  - Easy migration of patient data  

- **Exiting the Application (Option 9)**  
  Safely closes the program. All data is saved to text files (`medicalTest.txt` and `medicalRecord.txt`) before exiting.  

---

### Supported Test Types

* Hemoglobin (Hgb)
* Blood Glucose Test (BGT)
* LDL Cholesterol
* Systolic Blood Pressure (systole)
* Diastolic Blood Pressure (diastole)

---

##  Data Storage

* **`medicalTest.txt`**: Stores definitions for all medical tests.
* **`medicalRecord.txt`**: Stores all patient test records in a custom format.
* **CSV files**: Used for importing and exporting records in a universal format.

---

