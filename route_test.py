import streamlit as st
import pandas as pd
import sqlite3

def fee_details():

    # Define a dictionary with default fees for each bus route
    DEFAULT_FEES = {'1': 25000, '2': 24000, '3': 24500, '4': 23500, '5': 26000, '6': 25500}

    # Define a function to create the database table
    def create_table():
        conn = sqlite3.connect('students.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS students
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT,
                 bus_route TEXT,
                 department TEXT,
                 year TEXT,
                 fee_paid INTEGER)''')
        conn.commit()
        conn.close()

    # Define a function to add a student to the database
    def add_student(name, route, dept, year, fee):
        conn = sqlite3.connect('students.db')
        c = conn.cursor()
        c.execute("INSERT INTO students (name, bus_route, department, year, fee_paid) VALUES (?, ?, ?, ?, ?)",
                  (name, route, dept, year, fee))
        conn.commit()
        conn.close()

    # Define a function to retrieve all students from the database
    def get_students():
        conn = sqlite3.connect('students.db')
        c = conn.cursor()
        c.execute("SELECT * FROM students")
        rows = c.fetchall()
        conn.close()
        return rows

    # Define a function to update a student in the database
    def update_student(id, name, route, dept, year, fee):
        conn = sqlite3.connect('students.db')
        c = conn.cursor()
        c.execute("UPDATE students SET name=?, bus_route=?, department=?, year=?, fee_paid=? WHERE id=?",
                  (name, route, dept, year, fee, id))
        conn.commit()
        conn.close()

    # Define the Streamlit app
    def app():
        st.title('Bus Fee Manager')

        # Create the database table if it doesn't exist
        create_table()

        # Retrieve all students from the database
        student_rows = get_students()

        # Convert the rows to a DataFrame for display
        student_data = pd.DataFrame(student_rows, columns=['ID', 'Name', 'Bus Route', 'Department', 'Year', 'Fee Paid'])

        # Calculate the remaining fee for each student
        student_data['Remaining Fee'] = student_data.apply(lambda row: DEFAULT_FEES.get(row['Bus Route'], 0) - row['Fee Paid'], axis=1)

        st.table(student_data)
    
        # Calculate the total amount of fees
        total_fees = student_data['Fee Paid'].sum()

        # Show the total amount of fees collected
        st.markdown(f'Total Fees Collected: Rupees {total_fees}')

        # Calculate the total remaining fees
        total_remaining_fees = student_data['Remaining Fee'].sum()

        # Show the total amount of fees collected
        st.markdown(f'Total Remaining Fees : Rupees {total_remaining_fees}')




    
        # Add a form for users to edit student information
        with st.form(key='edit_student'):
            for index, row in student_data.iterrows():
                if st.checkbox(f"Edit Student {row['ID']}"):
                    edit_name = st.text_input('Name', value=row['Name'])
                    edit_route = st.selectbox('Bus Route', options=['1', '2', '3', '4', '5', '6'], index=int(row['Bus Route'])-1)
                    edit_dept = st.text_input('Department', value=row['Department'])
                    edit_year = st.text_input('Year', value=row['Year'])
                    edit_fee_paid = st.number_input('Fee Paid', value=row['Fee Paid'])

                    edit_default_fee = DEFAULT_FEES.get(edit_route, 0)
                    edit_remaining_fee = edit_default_fee - edit_fee_paid

                    if st.form_submit_button(f"Update Student {row['ID']}"):
                        conn = sqlite3.connect('students.db')
                        c = conn.cursor()
                        c.execute("UPDATE students SET name=?, bus_route=?, department=?, year=?, fee_paid=? WHERE id=?",
                                  (edit_name, edit_route, edit_dept, edit_year, edit_fee_paid, row['ID']))
                        conn.commit()
                        conn.close()

                        st.success(f'Student {row["ID"]} updated successfully!')
            st.form_submit_button('Submit')


        # Add a form for users to input student information
        with st.form(key='add_student'):
            st.header('Add New Student')
            name = st.text_input('Name')
            route = st.selectbox('Bus Route', options=['1', '2', '3', '4', '5', '6'])
            dept = st.text_input('Department')
            year = st.text_input('Year')
            fee_paid = st.number_input('Fee Paid')

            # Calculate the remaining fee based on the default fee for the selected route
            default_fee = DEFAULT_FEES.get(route, 0)
            remaining_fee = default_fee - fee_paid

            submit_button = st.form_submit_button(label='Add Student')

            # If the form is submitted, add the student to the database
            if submit_button:
                add_student(name, route, dept, year, fee_paid)
                st.success('Student added successfully!')


  




    app()

fee_details()
