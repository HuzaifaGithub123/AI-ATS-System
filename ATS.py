import base64
import io
from dotenv import load_dotenv # type: ignore
load_dotenv()
import streamlit as st
import os
from PIL import Image
from pdf2image import convert_from_bytes
import google.generativeai as genai # type: ignore

genai.configure(api_key="AIzaSyD_hfUdCpEQr-BRgLbD1QGJSuG8ZCn62YI")

def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text

def input_pdf_setup(upload_file):
    if upload_file is not None:
        # Convert the pdf to image
        images = convert_from_bytes(upload_file.read(), poppler_path=r"C:\poppler\poppler-24.08.0\Library\bin")
        first_page = images[0]

        # convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode() #encode to base 64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Set Page config
st.set_page_config(page_title="ATS Resume Expert", layout="centered")

# Page Header
st.markdown("<h1 style='text-align: center; color: #4B8BBE;'> ATS Tracking System</h1>", unsafe_allow_html=True)
st.markdown("Enter the Job Description Below")

# Job description input
input_text = st.text_area("Job Description", key="input", height=300)

# Resume upload
upload_resume = st.file_uploader("Upload your resume (PDF only))", type=["pdf"])
if upload_resume is not None:
    st.success("Resume uploaded successfully")

# Buttons
col1, col2 =st.columns(2)
with col1:
    submit1 = st.button("Tell me about the resume")
with col2:
    submit2 = st.button("How can I improve my skills")

input_prompt1 = """
You are an experienced Technical Human Resource Manager, your task is to review the provided resume against the job description.
Please share your professional evaluation or whether the candidate's profile aligns with the role. 
Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.    
"""

input_prompt2 = """
You are an skilled ATS (Applicant Tracking System)  scanner with a deep understanding of data science and ATS functionality,
Your task is to evaluate the resume against the provided job description. Give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""

if submit1:
    if upload_resume is not None:
        pdf_content = input_pdf_setup(upload_resume)
        response = get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader("The response is:")
        st.write(response)
    else:
        st.write("Please Upload the Resume")

elif submit2:
    if upload_resume is not None:
        pdf_content = input_pdf_setup(upload_resume)
        response = get_gemini_response(input_prompt2, pdf_content, input_text)
        st.subheader("The Response is:")
        st.write(response)
    else:
        st.write("Please Upload the resume")