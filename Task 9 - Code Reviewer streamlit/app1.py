# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 02:04:05 2024

@author: Vishal
"""

import google.generativeai as genai
import streamlit as st
import base64

# Configure the Google AI API key
genai.configure(api_key="AIzaSyB4tK6azgrb_-VQSgsNT2BW29ABjwaxJII")

# def analyze_code(code):
#     """Analyze the submitted code using Google AI API."""
#     model = genai.GenerativeModel('gemini-1.5-flash')
#     response = model.generate_content(f"You are a helpful AI code reviewer. "
#     "Students will ask you to review their code in Python. "
#     "You are expected to reply in as much detail as possible. "
#     "Make sure to give a bug report separately for each bug. "
#     "Provide all options and suggestions for each bug/error in the code below the bug report. "
#     "Ensure that only the code part is in code snippet format. "
#     "Please review the following Python code for potential bugs and suggest fixes:\n\n"
#     f"{code}")
#     return response.text

# Title of the app
st.title(":grey[Python Code Reviewer Application  ]-:blue[with Google AI] 💻")
# st.write(":red[Submit your Python code below for review:]")

# Subtitle of the app
# st.subheader(":red[Enter yours Python code for detailed analysis and receive insightful suggestions and improvements instantly!]")

def analyze_code(code):
    """Analyze the submitted code using Google AI API."""
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(f"Please review the following Python code for errors or improvements:\n\n{user_code}\n\nProvide feedback and suggest fixes if necessary.")
    return response.text

# Code input area
user_code = st.text_area("Submit your Python code below for review: ", height=100,placeholder ='Type or Paste your code here....')

# Custom CSS for the text area
st.markdown(
    """
    <style>
    /* Style for the Streamlit text area */
    .stTextArea {
        background-image: rgb(0,0,0);
        -webkit-text-fill-color: red;
    }
    
    .stTextArea [data-baseweb=base-input] {
        background-color:white-grey !important;
        -webkit-text-fill-color: green;
        border: 2px solid black !important;
    }
   
    </style>
    
    """,
    unsafe_allow_html=True
)

# Submit button
if st.button("Review Code"):
    if user_code:
        with st.spinner("Analyzing your code..."):
            feedback = analyze_code(user_code)
            st.success("Code review completed!")
            st.subheader("Feedback:")
            
            # Check if feedback contains code
            if "```python" in feedback:
                # Split the feedback to separate the code from the text
                parts = feedback.split("```python")
                # Display the text part
                st.markdown(parts[0], unsafe_allow_html=True)
                # Display the code snippet
                code_snippet = parts[1].split("```")[0]  # Get the code before the closing ```
                st.code(code_snippet, language='python')
            else:
                st.markdown(feedback, unsafe_allow_html=True)            
    else:
        st.error("Please enter some Python code to review.")


st.markdown(
    """
    <style>
    /* Style for the Streamlit text area */
    .stTextArea {
        background-image: rgb(0,0,0);
        -webkit-text-fill-color: red;
    }
    
    .stTextArea [data-baseweb=base-input] {
        background-color:white-grey !important;
        -webkit-text-fill-color: green;
        border: 2px solid black !important;
    }
   
    </style>
    
    """,
    unsafe_allow_html=True
)

# Function to set a faint background image with an overlay
def set_faint_background_image(image_path, overlay_opacity=0.5):
    # Load the image and encode it in base64
    with open(image_path, "rb") as img_file:
        img_data = base64.b64encode(img_file.read()).decode()

    # Create the CSS for background image and overlay
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpeg;base64,{img_data}");
            background-size: cover; /* Ensures the image covers the entire screen */
            background-position: center; /* Centers the image */
            height: 100vh; /* Full height of the viewport */
            width: 100vw; /* Full width of the viewport */
            position: relative;
        }}
        .overlay {{
            position: absolute;
            top: 0;
            left: 0;
            height: 100%;
            width: 100%;
            background-color: rgba(255, 255, 255, {overlay_opacity}); /* Faint overlay */
            z-index: 1; /* Ensures overlay stays on top */
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    # Add an overlay to make the background faint
    st.markdown('<div class="overlay"></div>', unsafe_allow_html=True)

# Set the path to your image file
image_path = "static/2.jpg"  # Replace with your image file path

# Set the faint background image with desired overlay opacity
set_faint_background_image(image_path, overlay_opacity=0.5)  # Adjust the overlay opacity value as needed



