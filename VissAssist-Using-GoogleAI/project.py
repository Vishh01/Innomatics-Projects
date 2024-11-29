
import streamlit as st
from PIL import Image
import pytesseract
import os
import io
from io import BytesIO
from gtts import gTTS
import tempfile
import base64, httpx
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI

# # Setup API Key
f = open('finalkey.txt')
genai_key = f.read()


# defining prompts for specific task
# Scene Description
prompt1 = ChatPromptTemplate.from_messages([
    ("system", """Return the requested response object in english.\n
     You are an AI assistant helping visually impaired individuals by describing the scene in the image.\n
     analyzes an uploaded image and generates a descriptive textual output that effectively interprets the scene.
     The output should include details about the objects present, their relationships, and any notable activities 
     occurring in the image. This will enable visually impaired users to understand their surroundings better and 
     engage with their environment more effectively."""),
    ("human", [
        {"type": "text", "text": " "},
        {
            "type": "image_url",
            "image_url": {"url": "data:image/jpeg;base64,{input_image}"},
        },
    ]),
])

# Object detection
prompt2 = ChatPromptTemplate.from_messages([
    ("system", """Return the requested response object in english.\n
     You are an AI assistant helping visually impaired individuals by describing the image.\n
     analyzes an image and generates a textual output identifies and highlights each key objects or obstacles within the uploaded image. 
     This functionality should provide insights regarding the location and nature of these objects to enhance user 
     safety and situational awareness. The application should clearly communicate the identified objects to help
     users navigate their environment more safely."""),
    ("human", [
        {"type": "text", "text": " "},
        {
            "type": "image_url",
            "image_url": {"url": "data:image/jpeg;base64,{input_image}"},
        },
    ]),
])     

# Dailt task   
prompt3 = ChatPromptTemplate.from_messages([
    ("system", """ Return the requested response object in english.\n
     You are an AI assistant helping visually impaired individuals by describing the image.\n
     Design a personalized assistance feature that offers task-specific guidance based on the content of the 
     uploaded image. This could include recognizing common household items, reading labels, or providing 
     context-specific information relevant to the user's needs. It should generate actionable 
     insights that help visually impaired users perform daily tasks independently and effectively.
     Suggestions for actions or precautions for the visually impaired user."""),
    ("human", [
        {"type": "text", "text": " "},
        {
            "type": "image_url",
            "image_url": {"url": "data:image/jpeg;base64,{input_image}"},
        },
    ]),
])

#********************************************************************************************     
# defining functions for the tasks

def extract_text_from_image(image):
    """Extracts text from the given image using OCR."""
    text = pytesseract.image_to_string(image)
    return text


def text_to_speech(text):
    """Converts the given text to speech and saves it as an audio file."""
    tts = gTTS(text=text, lang='en')
    
    # Use a temporary file to save the audio
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
        tts.save(tmp_file.name)
        return tmp_file.name


# Convert image to base64
def image_to_base64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")  # Save as JPEG
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str

def describe_scene(image):
    chain = prompt1 | model | output_parser
    describe = {"input_image" : image}
    output = chain.invoke(describe)
    return output


def detect_object(image):
    chain = prompt2 | model | output_parser
    describe = {"input_image" : image}
    output = chain.invoke(describe)
    return output

def daily_task(image):
    chain = prompt3 | model | output_parser
    describe = {"input_image" : image}
    output = chain.invoke(describe)
    return output

#********************************************************************************************

# Initialize the model & output parser
model = ChatGoogleGenerativeAI(model="gemini-1.5-flash",google_api_key = genai_key)

output_parser = StrOutputParser()

#*****************************************STREAMLIT APPLICATION***************************************************

# Title of the app
st.markdown("<h1 style='text-align: center; color: #32CD32;'>   VissAssist 🔍</h1> ", unsafe_allow_html=True)
st.markdown("<div style='text-align: center; color: #B0B0B0;'>Empowering Accessibility Through Image Intelligence. </div>", unsafe_allow_html=True)

# Sidebar

col1, col2, col3 = st.columns([1, 1, 1])  # Adjust the ratios as needed

with col2:
    # Center column
    st.image('2.png', width=150)  # Adjust width as needed

# Using object notation
st.sidebar.title(':blue[📖 About]')
add_selectbox = st.sidebar.selectbox(
    " ",
    ("","Features", "User Guide",)
)

# Feature data
features = """
### **Key Features**

- :gray-background[:orange[**Real-Time Scene Understanding** 🌐 :]]\n   *Generates descriptive text to interpret uploaded images.*
------------------------------------------------------------------------------------
- :gray-background[:orange[**Text-to-Speech Conversion** 🔊 :]]\n   *Utilizes OCR to extract text from images and converts it into audible speech.*
------------------------------------------------------------------------------------
- :gray-background[:orange[**Object and Obstacle Detection** 🛑 :]]\n   *Identifies and highlights objects/obstacles in images.*
------------------------------------------------------------------------------------
- :gray-background[:orange[**Personalized Assistance** 🤝 :]]\n   *Offers task-specific guidance by recognizing items and providing relevant context for daily activities.*
"""

# Instruction data
User_Guide = """
### **User  Guide**

- :gray-background[:orange[**Upload an Image** 📤 :]]\n   *Click the upload button to select an image from your device.*
------------------------------------------------------------------------------------
- :gray-background[:orange[**Select Features** ⚙️ :]]\n   *Choose the desired functionalities (scene understanding, text-to-speech, etc.) to apply to your image.*
------------------------------------------------------------------------------------
- :gray-background[:orange[**Receive Output** 📬 :]]\n   *View descriptive text, listen to extracted speech, or see highlighted objects as per selected features.*
------------------------------------------------------------------------------------
- :gray-background[:orange[**Explore Further** 🔍 :]]\n   *Use the personalized assistance feature for additional task support based on your uploaded image.* 
"""

# Display selected content in the sidebar
if add_selectbox == "Features":
    st.sidebar.image("gemini.jpg")
    st.sidebar.markdown(features)
elif add_selectbox == "User Guide":
    st.sidebar.image("userguide.png")
    st.sidebar.markdown(User_Guide)

# Main Page
# File uploader widget
uploaded_file = st.file_uploader(":blue[📷 Choose an image...]", type=["jpg", "jpeg", "png"])

# Check if an image has been uploaded
if uploaded_file is not None:
    # Open the image file
    image = Image.open(uploaded_file)
    # Display the image
    st.image(image, caption='Uploaded Image.', use_container_width=True)
    
# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["👁️Real-Time Scene Understanding", "📋 Text-to-Speech", "⚠️Object and Obstacle Detection", "💼 Daily Task"])

# Scene Understanding
with tab1:
    col1, col2, col3 = st.columns(3)
    
    if col2.button("Analyse Image",icon=":material/search_insights:",key="submit_button", use_container_width=False):
        
        try:
            with st.spinner("Analysing Scene..."):
                # Convert image to base64
                img_str = image_to_base64(image)
                # Describe scene
                output = describe_scene(img_str)
                
                st.subheader(':blue[✨Description💡:]')
                st.markdown(f'<div style="color: white; background-color: ; padding: 0px; border-radius: 1px;">{output}</div>', unsafe_allow_html=True)
                                
                # Convert text to speech and provide audio playback
                audio_file = text_to_speech(output)
                st.audio(audio_file, format='audio/mp3')
                st.success("Text-to-Speech Conversion Completed!")
        except:
            st.error("Please upload image to analyse.")
           


# Text to speech
with tab2:
    c1, c2, c3 = st.columns(3)
    
    if c2.button("Analyse Image",icon=":material/search_insights:",key="TTS_button", use_container_width=False):
        
        try:
            with st.spinner("Extracting text..."):
                # Extract text and display
                text = extract_text_from_image(image)
                # st.success("Text extraction completed!")
                st.subheader(':blue[✨Extracted text💡:]')
                # st.write(text)
                # Ensure that we handle the case where text might be empty
                if text.strip():
                    # Display the text in a non-editable format
                    st.markdown(f'<div style="color: white; background-color: ; padding: 0px; border-radius: 1px;">{text}</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<p style="color: white;">No text found in the image.</p>', unsafe_allow_html=True)
                
                
                # Convert text to speech and provide audio playback
                audio_file = text_to_speech(text)
                st.audio(audio_file, format='audio/mp3')
                st.success("Text-to-Speech Conversion Completed!")
                
        except:
            st.error("Please upload image to analyse.")
        
# Object detection
with tab3:
    c1, c2, c3 = st.columns(3)
    
    if c2.button("Analyse Image",icon=":material/search_insights:",key="Object_detect", use_container_width=False):
    
        try:
            with st.spinner("Analysing image..."):
                # Convert image to base64
                img_str1 = image_to_base64(image)
                # Describe scene
                output1 = detect_object(img_str1)
                
                st.subheader(':blue[✨Description:]')
                st.markdown(f'<div style="color: white; background-color: ; padding: 0px; border-radius: 1px;">{output1}</div>', unsafe_allow_html=True)
                                
                # Convert text to speech and provide audio playback
                audio_file = text_to_speech(output1)
                st.audio(audio_file, format='audio/mp3')
                st.success("Text-to-Speech Conversion Completed!")
        except:
            st.error("Please upload image to analyse.")
        
        
# Daily task
with tab4:
    c1, c2, c3 = st.columns(3)
    
    if c2.button("Analyse Image",icon=":material/search_insights:",key="Daily_task", use_container_width=False):
    
        try:
            with st.spinner("Analysing image..."):
                # Convert image to base64
                img_str2 = image_to_base64(image)
                # Describe scene
                output2 = daily_task(img_str2)
                
                st.subheader(':blue[✨Description:]')
                st.markdown(f'<div style="color: white; background-color: ; padding: 0px; border-radius: 1px;">{output2}</div>', unsafe_allow_html=True)
                                
                # Convert text to speech and provide audio playback
                audio_file = text_to_speech(output2)
                st.audio(audio_file, format='audio/mp3')
                st.success("Text-to-Speech Conversion Completed!")
        except:
            st.error("Please upload image to analyse.")
        

#********************************************************************************************
