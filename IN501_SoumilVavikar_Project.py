"""_summary_
    Program takes STUDENTDATA.TXT as input and provides the user with 8 options to analyze the student's data provided in the STUDENTDATA.TXT file. 
    The options provided are:
        1 - Display average grade for all students"
        2 - Display average grade for each program "
        3 - Display highest grade record"
        4 - Display lowest grade record"
        5 - Display students in MSIT"
        6 - Display students in MSCM"
        7 - Display all students in sorted order by student ID"
        8 - Display invalid records"
    
    _raises_
    The program raises exceptions like "ValueError", "InvalidInputFile", "InvalidMenuOption", and "InvalidRecord"
    
    _returns_
    The program would create a file for each type of option above, if the file is already present, it replaces the existing file with the new values.
"""

import os
from statistics import mean


# Defining a class student which will hold student's information
class Student:
    # Init method to initialize the class object
    def __init__(self, student_id, first_name, last_name, grade_score, degree):
        self.student_id = student_id
        self.first_name = first_name
        self.last_name = last_name
        self.grade_score = grade_score
        self.degree = degree

    # str method to print the data in the object
    def __str__(self):
        return "StudentId: {}, First Name: {}, Last Name: {}, Grade: {}, Degree: {}".format(
            self.student_id,
            self.first_name,
            self.last_name,
            self.grade_score,
            self.degree,
        )

    def __repr__(self):
        return self.__str__()


# Defining exception class for invalid input file.
class InvalidInputFile(Exception):
    pass


# Defining exception class for invalid menu option.
class InvalidMenuOption(Exception):
    pass


# Defining invalid student record exception.
class InvalidRecord(Exception):
    pass


# Method will check if a string is a float or not
def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False


# This method will write the records to the file.
def write_records_to_file(filename, records, is_list):
    # Writing the invalid records to the BADRECORDS.TXT file.
    here = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(here, filename)
    file = open(filepath, "w")
    if is_list:
        for record in records:
            file.write(record + "\n")
    else:
        file.write(records)
    file.close()


# Convert the student object into comma separated string in desired sequence
def get_student_str(student):
    return "{},{},{},{},{}".format(
        student.student_id,
        student.first_name,
        student.last_name,
        student.grade_score,
        student.degree,
    )


# This method will print the initial menu for the program.
def print_menu_capture_user_input():
    print_menu()
    return capture_action_to_perform()

# This method will print the menu.
def print_menu():
    print("--------------------------------------------------------")
    print("*************** Students Record Analysis ***************")
    print("--------------------------------------------------------")
    print("1 - Display average grade for all students")
    print("2 - Display average grade for each program ")
    print("3 - Display highest grade record")
    print("4 - Display lowest grade record")
    print("5 - Display students in MSIT")
    print("6 - Display students in MSCM")
    print("7 - Display all students in sorted order by student ID")
    print("8 - Display invalid records")
    print("9 - Exit the program")
    print()
    print("Please select one of the options from above (1 - 9)")
    
# This method will capture the user input for which action has to be performed
def capture_action_to_perform():
    action_to_perform = 0
    is_valid_input = False
    while (False == is_valid_input):
        try:
            # Capture the user input
            action_to_perform = int(input())
            # Check if a valid menu option is entered.
            if action_to_perform < 1 or action_to_perform > 9:
                raise InvalidMenuOption(
                    "Invalid menu option selected. Valid values are between 1 and 9"
                )
            is_valid_input = True
            return action_to_perform
        except InvalidMenuOption as imo:
            is_valid_input = False
            print(imo)
            print_menu()
        except ValueError as ve:
            is_valid_input = False
            print(
                "Invalid menu option selected. Valid values are between 1 and 9. Please try again."
            )
            print_menu()
    
    # returning the valid action to perform.
    return action_to_perform


# This method will read the input file
def read_input_file(file):
    here = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(here, file)
    # Open the input file in read mode
    with open(filename, "r") as file:
        try:
            # Read all the lines of the file into a list
            records = file.readlines()
            return records
        except Exception as ex:
            print("Exception occurred while reading the input file. Error:", ex)
            raise InvalidInputFile("Invalid input file. Error: {}".format(ex))


# This method will validate the student record and make sure all the requirements are met
def is_valid_student_record(fields):
    try:
        # Checking if the student record has all five fields.
        if 5 != len(fields):
            raise InvalidRecord(
                "Record should have five fields (StudentId, FirstName, LastName, Grade, Degree). Invalid record:{}".format(
                    fields
                )
            )
        else:
            # Removing the trailing regex for \n
            fields[4] = fields[4].replace("\n", "")

        # Validate the studentId. It should be a 4 digit integer value.
        if 4 != len(fields[0]) and not fields[0].isnumeric():
            raise InvalidRecord(
                "StudentId should be a 4 digit number. Invalid record: {}".format(
                    fields
                )
            )
        # Validating the first name. The length of the first name should be present and should be less than or equals to 10 chars
        elif 10 < len(fields[1]) or 0 == len(fields[1]):
            raise InvalidRecord(
                "First Name is missing OR has more than 10 chars. Invalid record: {}".format(
                    fields
                )
            )
        # Validating the last name. The length of the first name should be present and should be less than or equals to 10 chars
        elif 10 < len(fields[2]) or 0 == len(fields[2]):
            raise InvalidRecord(
                "Last Name is missing OR has more than 10 chars. Invalid record: {}".format(
                    fields
                )
            )
        # Checking if the grade provided for the student is valid or not (should be between 0 and 100)
        elif not isfloat(fields[3]) or 100 < float(fields[3]) < 0:
            raise InvalidRecord(
                "Grade should be between 0 and 100. Invalid record:{}".format(fields)
            )
        # Checking if the Degree program for the student is one of MSIT or MSCM
        elif "MSCM" != fields[4] and "MSIT" != fields[4]:
            raise InvalidRecord(
                "Degree program should be one of MSIT or MSCM. Invalid record: {}".format(
                    fields
                )
            )
        # If all the validations pass, logging the valid student record
        else:
            # Uncomment the below line to print valid records for debugging/testing purposes.
            # print("Valid student record:{}".format(fields))
            return True
    except InvalidRecord as ir:
        # Uncomment the below print statement to debug/test the method for invalid records.
        # print(ir)
        return False
    except ValueError as ve:
        print(
            "Error occured while validating the student records in the input file. Please check value types in the input file."
        )
        raise ve
    except Exception as ex:
        print(
            "Error occured while validating the student records in the input file. Please check the input file format."
        )
        raise ex


# This method will take grade percentage as input and return the grade value between A to D and F for Fail.
def calculate_student_grade(grade_percentage: float):
    if 90 <= float(grade_percentage) <= 100:
        return "A"
    elif 80 <= float(grade_percentage) <= 89:
        return "B"
    elif 70 <= float(grade_percentage) <= 79:
        return "C"
    elif 60 <= float(grade_percentage) <= 69:
        return "D"
    else:
        return "F"


# This method will print the records in proper manner.
def print_records(records):
    for record in records:
        print(record)


# This method will calculate the average grade score and print it
def calculate_avg_score(grade_scores, course):
    if 0 == len(grade_scores):
        return (
            "No students present for the degree/course - {} in the Input file.".format(
                course
            )
        )
    else:
        # getting the average grade score
        avg_grade_score = round(mean(grade_scores), 1)
        # getting average grade as per the average grade score
        avg_grade = calculate_student_grade(avg_grade_score)
        return "Average grade for degree/course {} is {}, and average grade score is {}".format(
            course, avg_grade, avg_grade_score
        )


# This method will perform the selected action on the student data present in the input file.
def perform_selected_action(action: int, students, invalid_records):
    if 1 == action:
        display_avg_grade_for_students(students)
    elif 2 == action:
        display_avg_grade_for_programs(students)
    elif 3 == action:
        display_highest_grade_record(students)
    elif 4 == action:
        display_lowest_grade_record(students)
    elif 5 == action:
        students_in_course(students, "MSIT", True)
    elif 6 == action:
        students_in_course(students, "MSCM", True)
    elif 7 == action:
        display_students_sorted_by_id(students)
    elif 8 == action:
        display_invalid_records(invalid_records)


# This method will calculate the avg grade for students, print it to the console and the output file.
def display_avg_grade_for_students(students):
    print("display_avg_grade_for_students: Displaying the avg grade for students")
    grade_scores = []
    for student in students:
        grade_scores.append(float(student.grade_score))
    record = calculate_avg_score(grade_scores, "MSIT and MSCM combined")
    print(record)
    # Writing the student with highest grade to a file
    write_records_to_file("AVERAGE_GRADE_FOR_ALL_STUDENTS.TXT", record, False)


# This method will calculate the avg grade per program, print it to the console and the output file.
def display_avg_grade_for_programs(students):
    print("display_avg_grade_for_programs: Displaying the avg grade for programs")
    # Getting all the students as per course.
    students_in_MSIT = students_in_course(students, "MSIT", False)
    students_in_MSCM = students_in_course(students, "MSCM", False)
    grade_scores_in_MSIT = []
    grade_scores_in_MSCM = []
    records = []
    # Building a list of grade scores for students per course
    if 0 != len(students_in_MSIT):
        for student in students_in_MSIT:
            grade_scores_in_MSIT.append(float(student.grade_score))
        records.append(calculate_avg_score(grade_scores_in_MSIT, "MSIT"))

    if 0 != len(students_in_MSCM):
        for student in students_in_MSCM:
            grade_scores_in_MSCM.append(float(student.grade_score))
        records.append(calculate_avg_score(grade_scores_in_MSCM, "MSCM"))

    # Printing and writing to he file, the calculated average grade scores for courses
    print_records(records)
    write_records_to_file("AVERAGE_GRADES_FOR_PROGRAMS.TXT", records, True)


# This method will display the record with the highest grade and print it to the output file.
def display_highest_grade_record(students):
    print("display_highest_grade_record: Displaying the record with highest grade")
    student_with_highest_grades = get_student_str(
        max(students, key=lambda student: student.grade_score)
    )
    print(student_with_highest_grades)
    # Writing the student with highest grade to a file
    write_records_to_file(
        "STUDENT_WITH_HIGHEST_GRADES.TXT", student_with_highest_grades, False
    )


# This method will display the record with the lowest grade and print it to the output file.
def display_lowest_grade_record(students):
    print("display_lowest_grade_record: Displaying the record with lowest grade")
    student_with_lowest_grades = get_student_str(
        min(students, key=lambda student: student.grade_score)
    )
    print(student_with_lowest_grades)
    # Writing the student with lowest grade to a file
    write_records_to_file(
        "STUDENT_WITH_LOWEST_GRADES.TXT", student_with_lowest_grades, False
    )


# This method will display the student records for the course and print them to the output file.
# print_rec field is used to decide whether we want to print anything to console or file in this method or not.
def students_in_course(students, course, print_rec):
    if print_rec:
        print("students_in_course: Displaying the students in the course: {}".format(course))

    students_in_course = []
    for student in students:
        if course == student.degree:
            if print_rec:
                students_in_course.append(get_student_str(student))
            else:
                students_in_course.append(student)

    if print_rec:
        print_records(students_in_course)
        # Writing the student list in the course in the file.
        write_records_to_file(
            "STUDENTS_IN_COURSE_{}.TXT".format(course), students_in_course, True
        )

    return students_in_course


# This method will sort the students by id, print them on console and to the output file.
def display_students_sorted_by_id(students):
    print("display_students_sorted_by_id: Displaying list of students sorted by studentId")
    students.sort(key=lambda student: student.student_id)
    sorted_students = []
    for student in students:
        sorted_students.append(get_student_str(student))
    print_records(sorted_students)
    # Writing the sorted student list by student_id
    write_records_to_file("SORTED_STUDENTS_BY_ID.TXT", sorted_students, True)


# This method will display all the invalid records, and print them to the bad record file.
def display_invalid_records(invalid_records):
    print("display_invalid_records: Displaying the invalid records present in the input file.")
    print_records(invalid_records)
    # Writing the invalid records to the BADRECORDS.TXT file.
    write_records_to_file("BADRECORDS.TXT", invalid_records, True)
    print("\nBADRECORDS.TXT has been created.")


# This is the main method of the program.
if __name__ == "__main__":
    try:
        # Print the initial menu for the program and capture user input for action to be performed
        action_to_perform = print_menu_capture_user_input()

        # The program will continue to run till the time user doesn't enter 9 to exit the program.
        while 9 != action_to_perform:
            # The list of students
            students = []
            # List of invalid records
            invalid_records = []

            # Step 2 - Read the input file - STUDENTDATA.TXT and validat the data inside
            records = read_input_file("STUDENTDATA.TXT")
            for record in records:
                fields = record.split(",")
                # Checking if the student record is valid and meets all requirements
                is_valid = is_valid_student_record(fields)
                # If the record is valid, add it to Students
                if is_valid:
                    students.append(
                        Student(fields[0], fields[1], fields[2], fields[3], fields[4])
                    )
                # If the record is invalid, add it to invalid_records
                else:
                    record = record.replace("\n", "")
                    invalid_records.append(record)

            # Uncomment below line to print students list for debugging/testing
            # print(students)

            # If the students list is empty, throw error.
            if 0 == len(students):
                raise InvalidInputFile(
                    "No student records loaded from the input file. Please provide a valid input file with file name - STUDENTDATA.TXT"
                )

            # Perform selected action on the student data loaded from the input file.
            perform_selected_action(action_to_perform, students, invalid_records)
            action_to_perform = print_menu_capture_user_input()
        else:
            print("Exiting the program.")
            exit()

    # Handling the exceptions thrown in the application/program here.
    except InvalidMenuOption as imo:
        print("{}, Please try again and select valid menu option.".format(imo))
    except Exception as ex:
        print("Error occurred while running the program. Error:", ex)
