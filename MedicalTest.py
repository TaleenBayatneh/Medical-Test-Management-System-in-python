import datetime
import csv
from datetime import datetime
############################################################################################################
############################################################################################################
######################################
# medical test class 
class MedicalTest:
    def __init__(self, name, normal_range, unit, turnaround_time): 
        self.name = name
        self.normal_range = normal_range
        self.unit = unit
        self.turnaround_time = turnaround_time

    def __str__(self):
        return f'Name: {self.name}; Range: > {self.normal_range[0]}, < {self.normal_range[1]}; Unit: {self.unit}, {self.turnaround_time}'


######################################
# medical test manangment system class 
class MedicalTestManagementSystem:
    def __init__(self):
        self.medical_tests = {}

    
    # add medical test entered to medical test file (write)
    def add_medical_test(self, name, normal_range, unit, turnaround_time):
        # store the test in the dictionary
        self.medical_tests[name] = MedicalTest(name, normal_range, unit, turnaround_time)
        
        # append the new test information to the file
        with open('C:\\Users\\hp\\AppData\\Local\\Microsoft\\Windows\\INetCache\\IE\\VDQYOA94\\medicalTest.txt', 'a') as file:
            file.write(f'{self.medical_tests[name]}\n')
        
        print("Medical test added and saved to file successfully.")

    
    def load_medical_tests(self):
        try:
            with open('C:\\Users\\hp\\AppData\\Local\\Microsoft\\Windows\\INetCache\\IE\\VDQYOA94\\medicalTest.txt', 'r') as file:
                for line in file:
                    line = line.strip()
                    if line:  # ensure the line is not empty
                        # split the line by ';' first
                        parts = line.split(';')

                        if len(parts) < 3:
                            print(f"Skipping invalid line: {line}")
                            continue

                        # handle the last part by splitting it by the new ',' 
                        last_part = parts[2].rsplit(',', 1)
                        if len(last_part) != 2:
                            print(f"Skipping invalid last part: {line}")
                            continue

                        # do update parts to include unit and turnaround time correctly after spliting
                        parts[2] = last_part[0]  # unit
                        parts.append(last_part[1].strip())  # turnaround time

                        # extract the name
                        name_part = parts[0].split(':')
                        if len(name_part) < 2:
                            print(f"Skipping invalid name part: {line}")
                            continue
                        name = name_part[1].strip()

                        # extract the range
                        range_part = parts[1].split('Range:')[1].strip()
                        try:
                            if '>,<' in range_part:
                                range_min_str, range_max_str = [x.strip() for x in range_part.split(',')]
                                range_min = float(range_min_str.split('>')[1].strip())
                                range_max = float(range_max_str.split('<')[1].strip())
                            elif '>' in range_part and '<' in range_part:
                                range_min_str, range_max_str = [x.strip() for x in range_part.split(',')]
                                range_min = float(range_min_str.split('>')[1].strip())
                                range_max = float(range_max_str.split('<')[1].strip())
                            elif '>' in range_part:
                                range_min_str = range_part.split('>')[1].strip()
                                range_min = float(range_min_str)
                                range_max = float('inf')  # no upper bound
                            elif '<' in range_part:
                                range_max_str = range_part.split('<')[1].strip()
                                range_min = float('-inf')  # no lower bound
                                range_max = float(range_max_str)
                            else:
                                print(f"Unexpected range format: {range_part}. Skipping: {line}")
                                continue
                        except (IndexError, ValueError) as e:
                            print(f"Error parsing range: {e}. Skipping: {line}")
                            continue

                        # extract the unit
                        unit_part = parts[2].split('Unit:')[1].strip()

                        # extract the turnaround time from the new last part
                        turnaround_time = parts[3].strip()

                        # create a new MedicalTest object and store it in the dictionary
                        self.medical_tests[name] = MedicalTest(name, (range_min, range_max), unit_part, turnaround_time)

        except FileNotFoundError:
            print(f"No existing test records found. Starting fresh.")
        except Exception as e:
            print(f"An error occurred while loading medical tests: {e}")



    # add medical test (let user add test) option in menu then add it to file
    def add_medical_test_from_input(self):
        # test name validation
        while True:
            name = input("Enter test name: ")
            if name.isalpha(): # check if entered name contain only characters
                break
            else: # if not ask user to re enter name until its valid 
                print("!! Invalid input, The test name must contain characters only !!")

        # normal range validation
        while True:
            try:
                normal_range_input = input("Enter normal range (min-max), if there is only max enter min = 0: ")
                normal_range = tuple(map(float, normal_range_input.split('-')))
                if len(normal_range) == 2 and all(isinstance(x, float) for x in normal_range): # check if user input is in format (min-max) and min max values are float
                    break
                else: # if user input is NOT in format (min-max)
                    print("!! Invalid input, Please enter the range in the format: min-max !!")
            except ValueError: # if user input for min max values are NOT float
                print("!! Invalid input, The normal range must contain integers only !!")

        # unit validation
        while True:
            unit = input("Enter result unit: ")
           
            if all(char.isalpha() or char == '/' or char == " " for char in unit): # check if user input for 'unit' has no integers
                break
            else: # if user input for unit contain integers
                print("!! Invalid input, The unit must contain only characters and '/' (no integeres) !!")

        # turnaround time validation
        while True:
            try:
                turnaround_time_input = input("Enter turnaround time (DD-hh-mm): ") # read user input
                turnaround_time = tuple(map(int, turnaround_time_input.split('-'))) # split to start checking
                
                if len(turnaround_time) == 3: # if user input in format DD-hh-mm
                    days, hours, minutes = turnaround_time # define days, hours, minutes to check their values
                    
                    # check if all parts are within the valid ranges
                    if (0 <= days <= 99 and
                        0 <= hours <= 23 and
                        0 <= minutes <= 59):
                        turnaround_time = turnaround_time_input  # convert to string format for storage
                        break
                    else: # if parts are NOT within the valid ranges
                        print("!! Invalid input, 'DD' must be between 00 and 99, 'hh' must be between 00 and 23, and 'mm' must be between 00 and 59 !!")
                else: # if input is not in format DD-hh-mm
                    print("!! Invalid input, Please enter the turnaround time in the format: DD-hh-mm !!")
            except ValueError: # if input is not integers
                print("!! Invalid input, The turnaround time must contain integers only !!")

        # after checking validation for all test fileds 
        # call add_medical_test method to add the test and save to file
        self.add_medical_test(name, normal_range, unit, turnaround_time)
        print("Medical test added successfully.")

    
    # print medical tests dictionary to check
    def print_medical_tests(self):
        if not self.medical_tests:
            print("No medical tests available.")
        else:
            print("\nStored Medical Tests:")
            for name, test in self.medical_tests.items():
                print(test)
    

    # save after any change in medical tests dictionary due to update option
    def save_medical_tests(self):
        """Save all medical tests from the dictionary to the file."""
        with open('C:\\Users\\hp\\AppData\\Local\\Microsoft\\Windows\\INetCache\\IE\\VDQYOA94\\medicalTest.txt', 'w') as file:
            for test in self.medical_tests.values():
                file.write(f'Name: {test.name}; Range: > {test.normal_range[0]}, < {test.normal_range[1]}; Unit: {test.unit}, {test.turnaround_time}\n')


    # update test option in menu (can update more than one filed in a test)
    def update_medical_test(self):
        # read medical test file contant to print to user 
        with open('C:\\Users\\hp\\AppData\\Local\\Microsoft\\Windows\\INetCache\\IE\\VDQYOA94\\medicalTest.txt', 'r') as file:
            lines = file.readlines()  # read all lines into a list
        i=1
        # print each line
        for line in lines:
            print(f'{i} {line.strip()}')
            i+=1

        i-=1 # i is the number of lines (tests)
        print("Enter line (Test) you want to update:")
        while True:
            try:
                # read user input and try to convert the input to an integer
                updateTest= input()
                updateTest=int(updateTest)
                # check if the number is between the range (1 - i'number of tests')
                if 1 <= updateTest <= i:
                    break 
                else: # handle the case where the input is an integer but NOT in range
                    print(f"!!Enter number between 1 and {i}:")
            except ValueError:
                # handle the case where the input is not an integer
                print("!!Invalid entry, enter an integer:")

        # read test name based on user choice
        test_name = list(self.medical_tests.keys())[updateTest - 1]

        # if not found
        if test_name not in self.medical_tests:
            print(f"Test with name {test_name} not found.")
            return

        # if found       
        test = self.medical_tests[test_name]
        print(f"\nCurrent record for {test_name}: {test}")

        # let user chose fileds to update
        fields_to_update = input("Enter the fields to update [name, range, unit, turnaround time] ** if more than one separate them by commas **: ").strip().split(',')

        for field in map(str.strip, fields_to_update):
            if field == 'name': # if 'name' filed were chosen
                while True:
                    new_name = input("Enter new test name: ").strip()
                    if new_name.isalpha(): # check if entered name contain only characters
                        break
                    else: # if not ask user to re enter name until its valid 
                        print("!! Invalid input, The new test name must contain characters only !!")

                if new_name:
                    self.medical_tests[new_name] = self.medical_tests.pop(test_name)
                    test.name = new_name
                    test_name = new_name
                    

            elif field == 'range':  # if 'range' field was chosen
                while True:
                    try:
                        new_range = input("Enter new range (min-max): ").strip()
                        # split the input and map to float
                        normal_range = tuple(map(float, new_range.split('-')))
                        
                        if len(normal_range) == 2:# check if the range has 2 elements (min max) and both are floats
                            range_min, range_max = map(float, new_range.split('-'))
                            test.normal_range = (range_min, range_max)# if yes update the test's range (min max)
                            break
                        else: # if new range is NOT in format min-max
                            print("!! Invalid input, Please enter the new range in the format: min-max !!")
                    except ValueError: # if new range is NOT numerical 
                        print("!! Invalid input, The new range must contain numerical values (min-max) !!")



            elif field == 'unit': # if 'unit' filed were chosen
                while True:
                    new_unit = input("Enter new unit: ").strip()
                
                    if all(char.isalpha() or char == '/' or char == " " for char in new_unit): # check if user input for 'unit' has no integers
                        test.unit = new_unit
                        break
                    else: # if user input for unit contain integers
                        print("!! Invalid input, The unit must contain only characters and '/' (no integeres) !!")

            
            elif field == 'turnaround time': # if 'turnaround time' filed were chosen
                while True:
                    try:
                        new_turnaround_time = input("Enter new turnaround time (DD-hh-mm): ").strip()
                        turnaround_time = tuple(map(int, new_turnaround_time.split('-'))) # split to start checking
                        
                        if len(turnaround_time) == 3: # if user input in format DD-hh-mm
                            days, hours, minutes = turnaround_time # define days, hours, minutes to check their values
                            
                            # check if all parts are within the valid ranges
                            if (0 <= days <= 99 and
                                0 <= hours <= 23 and
                                0 <= minutes <= 59):
                                test.turnaround_time = new_turnaround_time
                                break
                            else: # if parts are NOT within the valid ranges
                                print("!! Invalid input, 'DD' must be between 00 and 99, 'hh' must be between 00 and 23, and 'mm' must be between 00 and 59 !!")
                        else: # if input is not in format DD-hh-mm
                            print("!! Invalid input, Please enter the turnaround time in the format: DD-hh-mm !!")
                    except ValueError: # if input is not integers
                        print("!! Invalid input, The turnaround time must contain integers only !!")


                    
            else: # if NO filed were chosen or wrong files entery (skip update)
                print(f"Unknown field: {field}. Skipping update.")
        # done updating
        # save updated tests to the file
        self.save_medical_tests()
        # print updated test
        print(f"Updated record for {test_name}: {test}")

        
############################################################################################################
############################################################################################################
######################################
# MedicalRecord class 
class MedicalRecord:
    def __init__(self, patient_id, name, test_date, result_value, unit, status, results_date=None):
        self.patient_id = patient_id
        self.name = name
        self.test_date = test_date
        self.result_value = result_value
        self.unit = unit
        self.status = status
        self.results_date = results_date

    def __str__(self):
        return (f"{self.patient_id}: {self.name}, {self.test_date}, {self.result_value}, {self.unit}, {self.status}, {self.results_date if self.results_date else 'N/A'}")

# MedicalRecordManagementSystem class
class MedicalRecordManagementSystem:
    def __init__(self, medical_test_system):
        self.medical_test_system = medical_test_system
        self.medical_records = []

    def add_medical_record(self, patient_id, name, test_date, result_value, unit, status, results_date=None):
        record = MedicalRecord(patient_id, name, test_date, result_value, unit, status, results_date)
        self.medical_records.append(record)
        
        with open('C:\\Users\\hp\\AppData\\Local\\Microsoft\\Windows\\INetCache\\IE\\VDQYOA94\\medicalRecord.txt', 'a') as file:
            file.write(f'{record}\n')
        
        print("Medical record added and saved to file successfully.")


    def save_medical_records(self):
        """Save all medical records from the list to the file."""
        with open('C:\\Users\\hp\\AppData\\Local\\Microsoft\\Windows\\INetCache\\IE\\VDQYOA94\\medicalRecord.txt', 'w') as file:
            for record in self.medical_records:
                file.write(f'{record}\n')
    
            


    def load_medical_records(self):
        self.medical_records = []  # Reset the list
        try:
            with open('C:\\Users\\hp\\AppData\\Local\\Microsoft\\Windows\\INetCache\\IE\\VDQYOA94\\medicalRecord.txt', 'r') as file:
                for line in file:
                    #print(f"Reading line: {line.strip()}")
                    parts = line.strip().split(': ', 1)
                    if len(parts) < 2:
                        continue
                    patient_id = parts[0]
                    rest = parts[1].split(', ')
                    if len(rest) < 5:
                        continue
                    name = rest[0]
                    test_date = rest[1]
                    result_value = rest[2]
                    unit = rest[3]
                    status = rest[4]
                    results_date = rest[5] if len(rest) > 5 else None
                    record = MedicalRecord(patient_id, name, test_date, result_value, unit, status, results_date)
                    self.medical_records.append(record)
        except FileNotFoundError:
            print("Medical record file not found.")
        except Exception as e:
            print(f"An error occurred while loading medical records: {e}")



#======================================================================================================================================================================
#======================================================================================================================================================================
#======================================================================================================================================================================
    def name_match(self, test_name):
        if isinstance(self.medical_test_system, MedicalTestManagementSystem):
            # looping through the medical tests in the system
            for test in self.medical_test_system.medical_tests.values():
                # extract test name from the format (Name (some description))
                test_name_in_test = test.name.split('(')[-1].split(')')[0].strip()
                
                # check if the entered test name matches any test names in the medical_test_system
                if test_name == test_name_in_test:
                    return True
        return False
    
    
    def unit_match(self, name, unit):
        # Ensure medical_test_system is correctly initialized and is an instance of MedicalTestManagementSystem
        if isinstance(self.medical_test_system, MedicalTestManagementSystem):
            for test in self.medical_test_system.medical_tests.values():
                # Extract the test name (inside the parentheses)
                test_name_in_test = test.name.split('(')[-1].split(')')[0].strip()

                # No need to split unit by ':' since the units seem to be directly provided
                unit_in_test = test.unit.strip()

                # Check if the entered name matches and if the unit matches
                if name.strip().lower() == test_name_in_test.lower() and unit.strip().lower() == unit_in_test.lower():
                    return True

        return False



    def is_it_float(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False
        

    def valid_date(self, date):
        try:
            date_t = datetime.strptime(date, "%Y-%m-%d %H:%M")
            year = date_t.year
            month = date_t.month
            day = date_t.day
            hour = date_t.hour
            minute = date_t.minute

            if not (1 <= year <= 2024):
                print("Invalid year")
                return False
            if not (1 <= month <= 12):
                print("Invalid month")
                return False
            if not (1 <= day <= 31):
                print("Invalid day")
                return False
            if not (0 <= hour <= 23):
                print("Invalid hour")
                return False
            if not (0 <= minute <= 59):
                print("Invalid minute")
                return False

            return True
        except ValueError:
            print("Invalid date format.")
            return False
    
    def is_valid_string(self, value):
        return value.isalpha()
        

    def is_valid_string_unit(self, value):
        
        if all(char.isalpha() or char == '/' or char == " " for char in value):
            return True

        else:
            return False
        
    def is_valid_string_status(self, value):
        valid_statuses = {"pending", "completed", "reviewed"}

        while True:
                if not value or value.lower() in valid_statuses:  # if input is empty or valid
                    return True
                else:
                    return False

    def update_record(self):
        # load records from medical record file
        with open('C:\\Users\\hp\\AppData\\Local\\Microsoft\\Windows\\INetCache\\IE\\VDQYOA94\\medicalRecord.txt', 'r') as file:
            lines = file.readlines()

        # display records to let user chose
        for i, line in enumerate(lines, start=1):
            print(f'{i} {line.strip()}')

        # select line to update (make sure user line input is valid)
        while True:
            try:
                line_num = int(input("Enter the line number to update (1-{}): ".format(len(lines))))
                if 1 <= line_num <= len(lines):
                    break
                else:
                    print(f"Please enter a number between 1 and {len(lines)}.")
            except ValueError:
                print("Invalid entry. Please enter an integer.")

        # extract selected line details
        selected_line = lines[line_num - 1].strip()
        patient_id, record_str = selected_line.split(":", 1)
        record_list = [item.strip() for item in record_str.split(",")]

        # field types
        field_types = ["name_string", "date", "result_float", "unit_string", "status_string", "result_date"]

        # display current record and its fields
        for index, value in enumerate(record_list):
            print(f"{index + 1}: {value} (Type: {field_types[index]})")

        # let user select fields to update (can chose one or more to update)
        while True:
            try:
                fields_to_update = input("Enter the field numbers you want to update (comma-separated): ")
                indices = [int(num.strip()) - 1 for num in fields_to_update.split(",")]

                if all(0 <= index < len(record_list) for index in indices):
                    break
                else:
                    print("Invalid field numbers. Please enter numbers corresponding to the fields displayed.")
            except ValueError:
                print("Invalid input. Please enter integers separated by commas.")

        # update user selected fields
        for index in indices:
            while True:
                new_value = input(f"Enter the new value for field {index + 1} ({field_types[index]}): ")

                if field_types[index] == "name_string":
                    if self.name_match(new_value):
                        record_list[index] = new_value
                        break
                    else:
                        print("Invalid entry. Please enter a valid string.")

                elif field_types[index] == "date":
                    if self.valid_date(new_value):
                        record_list[index] = new_value
                        break
                    else:
                        print("Invalid date format. Please use YYYY-MM-DD HH:MM format.")

                elif field_types[index] == "result_float":
                    if self.is_it_float(new_value):
                        record_list[index] = float(new_value)
                        break
                    else:
                        print("Invalid entry. Please enter a valid float value.")

                elif field_types[index] == "unit_string":
                    name_t = field_types.index("name_string")  
                    print(record_list[name_t])
                    if self.unit_match(record_list[name_t], new_value):
                        record_list[index] = new_value
                        break
                    else:
                        print("Invalid unit format.")

                elif field_types[index] == "status_string":
                    if self.is_valid_string_status(new_value):
                        record_list[index] = new_value

                        # check if the status was updated to 'completed'
                    status_index = field_types.index("status_string") 
                    if record_list[status_index] == "completed":
                        while True:
                            result_date = input("Enter the result date (YYYY-MM-DD HH:MM): ")
                            if self.valid_date(result_date):  # check if it's a valid date
                                record_list[5] = result_date  # append result date to the record
                                break
                            else:
                                print("Invalid entry. Please enter a valid date in YYYY-MM-DD HH:MM format.")
                        break
                    else:
                        print("Invalid status.")

                elif field_types[index] == "result_date":
                    status_index = field_types.index("status_string") 
                    if record_list[status_index] == "completed":
                        if self.is_valid_string_unit(new_value):
                            record_list[index] = new_value
                            break
                        else:
                            print("Invalid unit format.")
                    else:
                        print("this record test status is not (Completed) it can not have result date")
                        break
                
                else:
                    print("Unsupported field type. Cannot update.")

        # Save updated record
        updated_line = f"{patient_id}: {', '.join(str(v) for v in record_list)}\n"
        lines[line_num - 1] = updated_line

        with open('C:\\Users\\hp\\AppData\\Local\\Microsoft\\Windows\\INetCache\\IE\\VDQYOA94\\medicalRecord.txt', 'w') as file:
            file.writelines(lines)

        #self.save_medical_records()
        print("The file has been updated successfully.")
        


    def add_record(self):
        while True:
            # Input and validate patient ID
            while True:
                patient_id = input("Enter the patient ID (7 digits): ")
                if patient_id.isdigit() and len(patient_id) == 7:
                    break
                print("Invalid ID. Please enter a 7-digit number.")

            # Input and validate test name
            while True:
                test_name = input("Enter the Test name: ")
                if self.name_match(test_name):
                    break
                print("Invalid entry. Please enter the test name as a string containing only letters.")

            # Input and validate test date
            while True:
                test_date = input("Enter the Test date (YYYY-MM-DD HH:MM): ")
                if self.valid_date(test_date):
                    break
                print("Invalid date format. Please use YYYY-MM-DD HH:MM format.")

            # Input and validate test result
            while True:
                test_result = input("Enter the Test result: ")
                if self.is_it_float(test_result):
                    test_result = float(test_result)  # Convert to float after validation
                    break
                print("Invalid result. Please enter a numeric value.")

            # Input and validate unit
            while True:
                unit = input("Enter the unit: ") 
                if self.unit_match(test_name, unit):
                    break
                print("Invalid entry. Please enter the unit as a string containing only letters.")

            # Input and validate status
            while True:
                status = input("Enter the status (pending, completed, reviewed): ").lower()
                if status in {"pending", "completed", "reviewed"}:
                    break
                print("Invalid status. Please enter one of the following: pending, completed, reviewed.")

            # If status is completed, input and validate results date
            if status == "completed":
                while True:
                    result_date = input("Enter the results date (YYYY-MM-DD HH:MM): ")
                    if self.valid_date(result_date):
                        break
                    print("Invalid date format. Please use YYYY-MM-DD HH:MM format.")
            else:
                result_date = None

            # Create and add the new medical record
            new_record = MedicalRecord(patient_id, test_name, test_date, test_result, unit, status, result_date)
            self.medical_records.append(new_record)
            self.add_medical_record(patient_id, test_name, test_date, test_result, unit, status, result_date)
            print("Record added successfully.")

            # Ask if the user wants to add another record
            another = input("Do you want to add another record? (yes/no): ").lower()
            if another != "yes":
                break

            


#======================================================================================================================================================================
#======================================================================================================================================================================
#======================================================================================================================================================================




    # abnormal funtion to be called in filter option 
    def is_abnormal(self, record): # for this function we need to access medical_test_system to do the comparasions
        # make sure medical_test_system is correctly initialized and is an instance of MedicalTestManagementSystem
        if isinstance(self.medical_test_system, MedicalTestManagementSystem):
            test_name_in_record = record.name
            # match test name in record with a test in medical_test_system
            for test in self.medical_test_system.medical_tests.values():
                test_name_in_test = test.name.split('(')[-1].split(')')[0].strip() # split to take test name inside '()'
                if test_name_in_record == test_name_in_test: # compare names if match
                    min_normal, max_normal = test.normal_range # if match take range to compare with record test result
                    return not (min_normal < record.result_value < max_normal)
        return False
    

    # filter option in menu (user can chose one or more criteria)
    def filter_records(self):
        filtered_records = self.medical_records
        filters = []

        # filter by patient ID
        while True:
            patient_id_input = input("Enter Patient ID to filter (or leave empty and press enter): ")
            
            if patient_id_input == "":  # if input is empty break
                break
            
            try:
                # convert the input to an integer
                patient_id = int(patient_id_input)
                # if it get converted append the filter (id is integer)
                filters.append(lambda record: record.patient_id == patient_id)
                break  
            except ValueError: # if id is not integer, conversion to integer fails
                print("!! Invalid input, Please enter a valid integer for Patient ID !!")



       # filter by test name
        while True:
            test_name = input("Enter Test Name to filter ((or leave empty 'press enter')): ")
            if not test_name or all(char.isalpha() or char.isspace() for char in test_name):  # if input is empty or valid
                break
            print("!! Invalid input, Please enter a test name containing only characters and spaces !!")

        # if a valid test name was entered apply the filter
        if test_name:  # if user entered something
            test_name = test_name.lower()  # convert  to lowercase for comparison
            filters.append(lambda record: record.name.lower() == test_name)



        # filter by test status
        # define valid statuses
        valid_statuses = {"pending", "completed", "reviewed"}

        while True:
            status = input("Enter Test Status to filter (Pending, Completed, Reviewed) ((or leave empty 'press enter')): ")
            if not status or status.lower() in valid_statuses:  # if input is empty or valid
                break
            print("!! Invalid input, Please enter one of the following statuses: Pending, Completed, Reviewed !!")

        # if valid status was entered apply the filter
        if status:  # check if user entered something
            status = status.lower()  # convert to lowercase for comparison
            filters.append(lambda record: record.status.lower() == status)



        # filter by test date range
        # function to check if a date is valid and within the specified range
        def is_valid_date(date_str):
            try:
                year, month, day = map(int, date_str.split('-'))
                if not (0 <= year <= 2024):
                    return False
                if not (1 <= month <= 12):
                    return False
                if not (1 <= day <= 31):
                    return False
                
                return True
            except ValueError:
                return False

        # ask user to enter start date until valid input is entered
        while True:
            start_date_input = input("Enter Start Date (YYYY-MM-DD) to filter ((or leave empty 'press enter')): ")
            if not start_date_input or is_valid_date(start_date_input):
                break
            print("!! Invalid date input, Ensure it is in YYYY-MM-DD format and within the correct range !!")

        # ask user to enter end date until valid input is entered
        while True:
            end_date_input = input("Enter End Date (YYYY-MM-DD) to filter ((or leave empty 'press enter')): ")
            if not end_date_input or is_valid_date(end_date_input):
                break
            print("!! Invalid date input, Ensure it is in YYYY-MM-DD format and within the correct range !!")

        # if valid dates were entered apply filter
        if start_date_input and end_date_input:
            try:
                start_date = datetime.datetime.strptime(start_date_input, '%Y-%m-%d')
                end_date = datetime.datetime.strptime(end_date_input, '%Y-%m-%d')
                filters.append(lambda record: start_date <= record.test_date <= end_date)
            except ValueError:
                print("!! Invalid date format, Please use YYYY-MM-DD !!")



        # filter by turnaround time
        # function to check if a value is a valid integer and within a specific range ( 00 - 59 )
        def is_valid_turnaround_time(value_str):
            try:
                value = int(value_str)
                return 0 <= value <= 59
            except ValueError:
                return False

        # ask user to enter minimum turnaround time until valid input is entered
        while True:
            min_turnaround_time = input("Enter minimum turnaround time in minutes to filter ((or leave empty 'press enter')): ")
            if not min_turnaround_time or is_valid_turnaround_time(min_turnaround_time):
                break
            print("!! Invalid turnaround time input, input must be an integer between 00 and 59 !!")

        # ask user to enter maximum turnaround time until valid input is entered
        while True:
            max_turnaround_time = input("Enter maximum turnaround time in minutes to filter ((or leave empty 'press enter')): ")
            if not max_turnaround_time or is_valid_turnaround_time(max_turnaround_time):
                break
            print("!! Invalid turnaround time input, input must be an integer between 00 and 59 !!")

        # if valid inputs are entered
        if min_turnaround_time and max_turnaround_time:
            min_turnaround_time = int(min_turnaround_time)
            max_turnaround_time = int(max_turnaround_time)
            filters.append(lambda record: record.results_date and min_turnaround_time <= (record.results_date - record.test_date).total_seconds() / 60 <= max_turnaround_time)



        # filter by abnormal tests
        abnormal = input("Enter 'abnormal' or any key (except 'enter') to filter (or leave empty and press enter): ")
        if abnormal:
            filters.append(lambda record: self.is_abnormal(record))



        # apply each filter function to every record  
        for filter_func in filters:
            filtered_records = list(filter(filter_func, filtered_records))

        if filtered_records: # if filter records is not empty
            print("\nFiltered Records are:") 
            for record in filtered_records: # print filtered records one by one
                print(record)
        else: # if filter records is empty
            print("!! There is NO records matched your criteria !!")
        
        return filtered_records


    # print medical records list to check
    def print_medical_records(self):
        if not self.medical_records: # if medical records list is empty
            print("No medical records available.")
        else: # if medical records list is not empty
            print("\nStored Medical Records:")
            for record in self.medical_records:
                print(record)


    # generate summary report option in menu
    def generate_summary_report(self):
        # will use the same search and filter test options (call filter_records())
        filtered_records = self.filter_records()
    
        # if there are no filtered records (empty) 
        if not filtered_records: # cannot generate a report
            print("No records to generate a report.")
            return

        # this method will report filtered records including: Minimum test values, maximum test value, average test value, Minimum turnaround time, maximum turnaround time, average turnaround time. 
        # calculating min, max and average values
        min_value = min(record.result_value for record in filtered_records)
        max_value = max(record.result_value for record in filtered_records)
        avg_value = sum(record.result_value for record in filtered_records) / len(filtered_records)

        # Calculating (nim, max) turnaround time (( only completed records // only if recors have results_date filed ))
        completed_records = [record for record in filtered_records if record.results_date]
        if completed_records:
            min_turnaround = min((record.results_date - record.test_date).total_seconds() / 60 for record in completed_records)
            max_turnaround = max((record.results_date - record.test_date).total_seconds() / 60 for record in completed_records)
            avg_turnaround = sum((record.results_date - record.test_date).total_seconds() / 60 for record in completed_records) / len(completed_records)

            # printing values for summary report
            print("\nSummary Report:")
            # tests result values
            print(f"Minimum Test Value: {min_value}")
            print(f"Maximum Test Value: {max_value}")
            print(f"Average Test Value: {avg_value:.2f}")
            # turnaround time values for completed records
            print(f"Minimum Turnaround Time: {min_turnaround:.2f} minutes")
            print(f"Maximum Turnaround Time: {max_turnaround:.2f} minutes")
            print(f"Average Turnaround Time: {avg_turnaround:.2f} minutes")
        else: # if a record is not completed, will only print tests result values
            print("\nSummary Report:")
            print(f"Minimum Test Value: {min_value}")
            print(f"Maximum Test Value: {max_value}")
            print(f"Average Test Value: {avg_value:.2f}")
            print("No completed tests with turnaround time data.")



    #########################################################          
    def export_to_csv (self):
       
       with open('C:\\Users\\dell\\Desktop\\linux\\midecalRecord.txt', 'r') as file:
         lines = file.readlines()

       dict = {} 
       with open('C:\\Users\\dell\\Desktop\\linux\\midicalRecord.csv', 'w', newline='') as csv_f:
        csv_writer = csv.writer(csv_f)

        for line in lines:
         p_id, values = line.strip().split(":", 1)
    
         record_list = [value.strip() for value in values.split(",")]
    
         dict[p_id] = record_list

        for id, value in dict.items():
          csv_writer.writerow([id] + value)

       print("data has been exported to medicalRecord.csv successfully ")


 #########################################################    
    def import_to_csv(self):
       
       with open('C:\\Users\\dell\\Desktop\\linux\\midicalRecord.csv', mode='r') as csv_f:
         with open('C:\\Users\\dell\\Desktop\\linux\\midecalRecord.txt', mode='w') as file:
          for line in csv_f:
            file.write(line)

       print("data has been written to midicalRecord.txt successfully ")

 ########################################################

############################################################################################################
############################################################################################################
######################################
# menu function
def menu():
        print("\nMedical Test Management System")
        print("1. Add New Medical Test")
        print("2. Add Test Record")
        print("3. Update Patient Record")
        print("4. Update Medical Test")
        print("5. Filter medical Tests")
        print("6. Generate Summary Report")
        print("7. Export to CSV")
        print("8. Import from CSV")
        print("9. Exit")
 
        option = input("Select an option from the menu:")
        return option

######################################
# main function
def main():
    m=MedicalTestManagementSystem()
    m.load_medical_tests()
    m.print_medical_tests()
    r=MedicalRecordManagementSystem(m)
    r.load_medical_records()
    r.print_medical_records()
    
    while True:
        option = menu()

        if option == '1':
            m.add_medical_test_from_input()
 
        elif option == '2':
            r.add_record()
   
        elif option == '3':
            r.load_medical_records()
            r.update_record()

        elif option == '4':
            m.load_medical_tests()
            m.update_medical_test()

        elif option == '5':
            r.filter_records()
   
        elif option == '6':
            r.generate_summary_report()
   
        elif option == '7':
            r.export_to_csv()
    
        elif option == '8':
            r.import_to_csv()          

        elif option == '9':
            break

        else:
            print("!! Invalid option. Please try again.")

if __name__ == "__main__":
    main()