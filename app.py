from dotenv import load_dotenv
import streamlit as st
import os
from PIL import Image
import pdf2image
import google.generativeai as genai
import io
import base64

# Load environment variables
load_dotenv()

# Configure API key for Google Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Path to Poppler binaries (replace with your actual path)
poppler_path = r"C:\Users\Administrator\poppler-24.08.0\Library\bin"

# Define the function to get the Gemini response
def get_gemini_response(input_text, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-pro')
    response = model.generate_content([input_text, pdf_content[0], prompt])
    return response.text

# Define the function to handle the uploaded PDF file
def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        # Convert PDF to image using the Poppler path
        images = pdf2image.convert_from_bytes(uploaded_file.read(), poppler_path=poppler_path)

        # Get the first page
        first_page = images[0]

        # Convert the first page to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        # Encode the image to base64
        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()  # encode to base 64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No PDF file uploaded")

# Streamlit App
st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")

# Job description input
input_text = st.text_area("Job Description:", key="input")

# Resume file uploader
uploaded_file = st.file_uploader("Upload your resume (PDF)...", type=["pdf", "docx", "txt","jpg","jpeg"])

# Success message on file upload
if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

# Buttons for different actions
submit1 = st.button("Tell Me about the Resume")
submit2 = st.button("How can the Resume be Improved?")
submit3 = st.button("Percentage match")

# Input prompts
input_prompt1 = """
 You are an experienced HR with Tech Experience in the field of any of the job role from Data Science,Machine Learning,Full Stack, Web Development, Big Data Engineering,DEVOPS,Data Analyst and your task is to review the provided resume against the job description for these profiles.
 Please share your professional evaluation on whether the candidate's profile align with the job description provided.
 Highlight the strengths and weaknesses of the applicant in relation to the specified job description provided.
 """
input_prompt2 =  """
 You are an experienced HR with many years of Tech Experience in the field of any of the job role from Data  Science,Machine Learning,Full Stack, Web Development, Big Data Engineering,DEVOPS,Data Analyst and your task here is to review the given resume against the job description provided.
 Please share your professional evaluation and insights on how the candidate's profile can be improved to match the job description provided.
 Also add the missing skills required  to make the candidate a perfect fit for the job description provided.
 """

input_prompt3 = """
 You are an skilled ATS (Application Tracking System) scanner with a deep understanding in any job role of Data Science,Machine Learning,Full Stack, Web Development, Big Data Engineering,DEVOPS,Data Analyst and deep ATS functionality.
 Your task is to evaluate the resume against the provided job description.Give me the percentage match if the resume matches the job description.
 First the output should come as percentage and then keywords missing and last final thoughts.
"""

# Actions based on button clicks
if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader("The Response is:")
        st.write(response)
    else:
        st.write("Please upload the resume")

elif submit2:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt2, pdf_content, input_text)
        st.subheader("The Response is:")
        st.write(response)
    else:
        st.write("Please upload the resume")


elif submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt3, pdf_content, input_text)
        st.subheader("The Response is:")
        st.write(response)
    else:
        st.write("Please upload the resume")
