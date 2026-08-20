import streamlit as st 
import os 
import time 
import glob 
from gtts import gTTS 
from PIL import Image 
import base64 
 
st.title("Conversión de Texto a Audio") 

image = Image.open('gato_raton.png') 
st.image(image, width=350) 

with st.sidebar: 
    st.subheader("Selecciona el idioma del audio.") 
 
try: 
    os.mkdir("temp") 
except: 
    pass 
 
st.subheader("Un fragmento.") 

# Texto que será convertido directamente a audio
text = (
    'Mira, / Mayo de 1985 Ahora volvían, y aunque todo había salido más o menos como lo había previsto, '
    'algo que no había previsto había regresado: ese miedo loco, ese fastidio… esa sensación de Otro. '
    'Odiaba el miedo, lo hubiera atacado y devorado si hubiera podido… pero el miedo bailaba burlonamente '
    'fuera de su alcance, y solo podía matar el miedo matándolos a ellos. '
    'Seguro que no había necesidad de tanto miedo; ahora eran mayores, y su número se había reducido de siete a cinco. '
    'Cinco era un número poderoso, pero no tenía la cualidad mística y talismánica del siete. '
    'Es cierto que su lacayo no había podido matar al bibliotecario, pero el bibliotecario moriría en el hospital. '
    'Más tarde, justo antes del amanecer, enviaría a un enfermero con una mala adicción a las pastillas '
    'para acabar con el bibliotecario de una vez por todas.'
)

st.write(text)
 
tld = 'com' 
 
option_lang = st.selectbox( 
    "Selecciona el lenguaje", 
    ("Español", "English")
) 

if option_lang == "Español": 
    lg = 'es' 

if option_lang == "English": 
    lg = 'en' 
 
 
def text_to_speech(text, tld, lg): 
     
    tts = gTTS(text, lang=lg) 

    my_file_name = "audio"

    tts.save(f"temp/{my_file_name}.mp3") 

    return my_file_name
 
 
if st.button("🎧 Escuchar texto"): 

     result = text_to_speech(text, 'com', lg)

     audio_file = open(f"temp/{result}.mp3", "rb") 

     audio_bytes = audio_file.read() 

     st.markdown("## 🔊 Tu audio:") 

     st.audio(
         audio_bytes, 
         format="audio/mp3", 
         start_time=0
     ) 
 
     with open(f"temp/{result}.mp3", "rb") as f: 
         data = f.read() 
 
     def get_binary_file_downloader_html(
         bin_file, 
         file_label='File'
     ): 
        bin_str = base64.b64encode(data).decode() 

        href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Download {file_label}</a>' 

        return href 

     st.markdown(
         get_binary_file_downloader_html(
             "audio.mp3", 
             file_label="Audio File"
         ), 
         unsafe_allow_html=True
     ) 
 
 
def remove_files(n): 

    mp3_files = glob.glob("temp/*mp3") 

    if len(mp3_files) != 0: 

        now = time.time() 
        n_days = n * 86400 

        for f in mp3_files: 

            if os.stat(f).st_mtime < now - n_days: 

                os.remove(f) 

                print("Deleted ", f) 
 
 
remove_files(7)
