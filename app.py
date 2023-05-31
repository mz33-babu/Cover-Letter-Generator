# import libraries
import streamlit as st
import openai
import json
from docx import Document
from docx.shared import Inches

with open('config.json') as f:
    config = json.load(f)

# State important variables
openai.api_key = config['api_key']

# Define functions
def get_cv():
    cv_text = st.text_area('Paste your cv')
    return cv_text

def get_job_description():
    job_desc = st.text_area('Paste the job Description')

def generate_docx(text):
    document = Document
    document.add_heading('Cover Letter')
    document.add_paragraph(text)
    document.save('cover_letter.docx')

def cover_letter_generator(cv, job_description):
    cv_prompt = f"""

                Generate a compelling cover letter using the details from my CV:
                {cv} and the provided job description:
                {job_description}. The cover letter should effectively and accurately highlight my skills and experiences in relation to the job requirements.
                """

    response = openai.Completion.create(
                    model="text-davinci-003",
                    prompt=cv_prompt,
                    max_tokens=512,
                    temperature=0.2 #creativity of generation scale of 0.1-2.0
                    )
    
    cover_letter = response.choices[0].text

    return cover_letter

def main():
    st.set_page_config(page_title="Project Kurusha", page_icon=":rocket:")
    st.title(" Cover Letter Generator")
    cv_text = get_cv()
    if cv_text:
        job_desc = get_job_description()
        if job_desc:
            if st.button('Generate Cover Letter'):
                response = cover_letter_generator(cv_text, job_desc)
                generate_docx(response)
                with open('cover_letter.docx', 'rb') as docx_file:
                    st.download_button('Download', data=docx_file, file_name='cover_letter.docx')
                
if __name__  == '__main__':
    main()      
