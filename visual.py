# importing necessary libraries
import streamlit as st
import google.generativeai as genz
from dotenv import load_dotenv
import os
load_dotenv()
from PIL import Image 
import io
import pyttsx3
import re
import easyocr

st.set_page_config(   
                page_title="Visual_Pair_X  App",
                page_icon="🧊",
                layout="wide",
                initial_sidebar_state="expanded")

st.sidebar.image("ai.jpg",width=270)
st.sidebar.title("Hi , I'm  :red[**AirX**]")
st.sidebar.caption("Your :blue[**BeLoved**] Assistant🤖")
st.sidebar.html("<p><hr><p/>")
query_file=st.sidebar.file_uploader(" \n \n🗳️**Please Input Your File Here..**")

# Creating a layout titles for streamlit
st.title("Application for :red[Visually Impaired] !")
st.write("Powered by **:red[AI]** ")
st.write("-"*30)    

# Defining AI functionalities           
genz.configure(api_key=os.getenv("api_key"))
ai_role="""You're an expert and kind-hearted AI assistant who helps visually impaired people,
            Enabling users to understand effectively.
            You have to help them in every aspect and respond to each question they ask.
            use a word "Dear".if you don't know the answer politely tell them.
        """

model=genz.GenerativeModel(model_name = "models/gemini-1.5-flash",system_instruction=ai_role)
#prompt=st.text_input("Ask your Query...")               

    
if st.sidebar.button("🔍 :blue[**Get_Details**] "):
    if query_file:
        try:   
            # Setting Up the TTS      
            engine=pyttsx3.init()
            engine.setProperty('rate',150)
            engine.setProperty("volume",0.9)
            voices=engine.getProperty('voices')
            engine.setProperty('voice',voices[1].id)
 
            # Read the uploaded file 
            img = Image.open(query_file) 
            st.image(img, caption='Uploaded Image',width=300)
            
            # capturing text from images..OCR------------------
            
            read=easyocr.Reader(['en'])
            results=read.readtext(img)
            container = st.container(border=True)
            
            with st.spinner(":blue[**Capturing text from Images**]"):
                container.write("**🖼️ Text extraction result from** :red[**OCR - Feature !**] :")
                    
                if results:
                    found_text ="Extracted Text is of :" + ' '.join(result[1] for result in results) 
                    container.write(found_text)  
                    engine.say(found_text)  
                    engine.runAndWait()
                else:
                    no_text = "My friend, No text found in the image you uploaded ."
                    container.write(no_text)
                    engine.say(no_text) 
                    engine.runAndWait()
                
            
                        
            # Object identification promt role for ai----------------------
            
            with st.spinner(":blue[**Object Identification**]"):
                prompt="name only the objects and items in the image without any description . "
                cont = st.container(border=True)     
                response = model.generate_content([img,prompt])
                cont.write("**🖼️ Text result of** :red[**Object Identification - Feature !**] :")
                cont.write(" ")
                cont.write(response.text)
                
                
                # TTS for Gen response
                clean=re.sub(r'\*', '',response.text)
                engine.say(clean)
                engine.runAndWait()

                
            # Context specific promt role for ai----------------------
            with st.spinner(':blue[**Context Specific**]'):
                    
                prompt2="provide task specific guidance based on uploaded image using ai abilites,for safety and situation awareness"
                cont2 = st.container(border=True)     
                response2 = model.generate_content([img,prompt2])
                cont2.write("**🖼️ Text result for Safety & Situation Awareness** :red[**Content Specific - Feature !**] :")
                cont2.write(" ")
                cont2.write(response2.text)
                
                # TTS for Gen response
                clean2=re.sub(r'\*', '',response2.text)
                engine.say(clean2)
                engine.runAndWait() 
                
    
            # Real Time scene understanding promt role for ai----------------------
            
            with st.spinner(":blue[**Real Time Scene Understanding**]"):
                
                prompt3="Generate descriptive text for the uploaded image depicting the scenes in 150 words using ai abilites."
                cont3 = st.container(border=True)     
                response3 = model.generate_content([img,prompt3])
                cont3.write("**🖼️ Text result for Content generation** :red[**Real Time Scene Understanding - Feature !**] :")
                cont3.write(" ")
                cont3.write(response3.text)
        
                # TTS for Gen response
                clean3=re.sub(r'\*', '',response3.text)
                engine.say(clean3)
                engine.runAndWait()    
                
    
            st.write("-"*30)
            
            combined_text = f"OCR-Text\n{results}\n\nIdentificaton:\n{response}\n\nSpecific:\n{response2}\n\nSpecific:\n{response3}"
            st.download_button("🔻Download Script",response.text)   

        except Exception as e:
            st.error(f"An error has occured: {e}")

    else:
        st.warning("Please Input Your File !")

# Audio Blocking
audio_stop=st.sidebar.button("🔇:red[**Stop_Audio**]")
if audio_stop:
    try:
        if "py_engine" not in st.session_state:
            st.session_state.py_engine=pyttsx3.init()
        
        st.session_state.py_engine.stop()
        st.success("Audio Engine Ended")
    except Exception as e:
        st.error(f"Audio Engine Failed to Interrupt. Error {e}")
        
    