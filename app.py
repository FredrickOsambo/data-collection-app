import streamlit as st
import pandas as pd
import os
import re

# File to store data
DATA_FILE = "collected_data.csv"

# Load existing data or create a new file
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    return pd.DataFrame(columns=["Name", "Year Group", "Ministry", "Course", "Phone Number", "Email Address", "Baptised", "Place of Residence"])

def save_data(data):
    data.to_csv(DATA_FILE, index=False)

def validate_phone(phone):
    return re.fullmatch(r"\+?\d{10,15}", phone) is not None

def validate_email(email):
    return re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email) is not None

# Streamlit UI
st.title(" Chiromo Data Collection Platform")
st.write("Enter the required details below:")

# Form inputs
with st.form("entry_form", clear_on_submit=True):
    name = st.text_input("Name")
    year_of_study = st.selectbox("Year Group", ["Waggoners", "Bereans", "Valours", "Millerites", "Seraphs", "Sojourners"])
    ministry = st.selectbox("Ministry", ["Maranatha", "Melodians", "Mustard Seed"])
    course = st.text_input("Course")
    phone_number = st.text_input("Phone Number")
    email = st.text_input("Email Address")
    baptised = st.radio("Baptised?", ["Yes", "No"])
    residence = st.text_input("Place of Residence")
    submit = st.form_submit_button("Save Entry")

# Handle form submission
if submit:
    if not validate_phone(phone_number):
        st.error("Invalid phone number. Please enter a valid format.")
    elif not validate_email(email):
        st.error("Invalid email address. Please enter a valid email.")
    else:
        new_entry = pd.DataFrame([[name, year_of_study, ministry, course, phone_number, email, baptised, residence]], 
                                  columns=["Name", "Year Group", "Ministry", "Course", "Phone Number", "Email Address", "Baptised", "Place of Residence"])
        data = load_data()
        data = pd.concat([data, new_entry], ignore_index=True)
        save_data(data)
        st.success("Entry saved successfully!")

# Display collected data
st.write("## Collected Data")
data = load_data()
updated_data = st.data_editor(data, num_rows="dynamic")

# Save updated data if edited
if not updated_data.equals(data):
    save_data(updated_data)
    st.success("Changes saved successfully!")

# Export to Excel
if st.button("Download Data as Excel"):
    excel_file = "collected_data.xlsx"
    data.to_excel(excel_file, index=False)
    with open(excel_file, "rb") as f:
        st.download_button("Download Excel File", f, file_name=excel_file, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
