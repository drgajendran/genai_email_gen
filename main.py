import streamlit as st
import google.generativeai as genai
from fpdf import FPDF
import tempfile

# Configure Gemini API
genai.configure(api_key="AIzaSyD3fsB8rMk3PFpfWX4UbjX5lXzGG_lcUPQ")
model = genai.GenerativeModel('gemini-2.0-flash')

def generate_email(prompt, tone, format_style):
    full_prompt = f"Write an email in {tone} tone and {format_style} format based on the following:\n\n{prompt}"
    response = model.generate_content(full_prompt)
    return response.text

def save_pdf(content):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    for line in content.split('\n'):
        pdf.multi_cell(0, 10, line)
    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(temp.name)
    return temp.name

st.title("📧 Email Generator using Gemini AI")
st.write("Enter your content, select the tone and format, and generate a professional email.")

user_input = st.text_area("Enter the main points or message for the email:")

tone = st.selectbox("Choose the tone of the email:", ["Formal", "Informal", "Friendly", "Professional"])

format_style = st.radio("Select the format of the email:", ["Business", "Casual", "Concise", "Detailed"])

if st.button("Generate Email"):
    if user_input.strip() == "":
        st.warning("Please enter some content.")
    else:
        email_output = generate_email(user_input, tone, format_style)
        st.session_state['email'] = email_output
        st.success("✅ Email generated!")
        st.text_area("Generated Email:", value=email_output, height=300)

        pdf_path = save_pdf(email_output)
        with open(pdf_path, "rb") as f:
            st.download_button("📥 Download as PDF", f, file_name="generated_email.pdf", mime="application/pdf")

if 'email' in st.session_state and st.button("🔁 Regenerate with New Tone/Format"):
    email_output = generate_email(user_input, tone, format_style)
    st.session_state['email'] = email_output
    st.text_area("Regenerated Email:", value=email_output, height=300)

    pdf_path = save_pdf(email_output)
    with open(pdf_path, "rb") as f:
        st.download_button("📥 Download Regenerated PDF", f, file_name="regenerated_email.pdf", mime="application/pdf")
