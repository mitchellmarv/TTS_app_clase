import streamlit as st
import os
import time
import glob
import base64
from gtts import gTTS
from PIL import Image


# ============================================================
# CONFIGURACIÓN DE LA PÁGINA
# ============================================================

st.set_page_config(
    page_title="Asistente de Audio",
    page_icon="🔊",
    layout="centered"
)


# ============================================================
# ESTILOS
# ============================================================

st.markdown("""
<style>

    /* Fondo general */
    .stApp {
        background-color: #F5F7FB;
    }

    /* Título */
    .main-title {
        text-align: center;
        font-size: 38px;
        font-weight: 700;
        color: #252A34;
        margin-bottom: 5px;
    }

    /* Subtítulo */
    .subtitle {
        text-align: center;
        font-size: 17px;
        color: #6B7280;
        margin-bottom: 30px;
    }

    /* Tarjetas */
    .card {
        background-color: white;
        padding: 25px;
        border-radius: 18px;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.08);
        margin-bottom: 20px;
    }

    /* Texto de las secciones */
    .section-title {
        font-size: 22px;
        font-weight: 600;
        color: #252A34;
        margin-bottom: 10px;
    }

    /* Texto pequeño */
    .helper-text {
        color: #6B7280;
        font-size: 14px;
        margin-bottom: 10px;
    }

    /* Botón */
    .stButton > button {
        width: 100%;
        border-radius: 12px;
        height: 50px;
        font-size: 17px;
        font-weight: 600;
        border: none;
    }

    /* Área de texto */
    textarea {
        border-radius: 12px !important;
    }

    /* Separador */
    .divider {
        margin-top: 15px;
        margin-bottom: 15px;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# CARPETA TEMPORAL
# ============================================================

if not os.path.exists("temp"):
    os.mkdir("temp")


# ============================================================
# ENCABEZADO
# ============================================================

st.markdown(
    '<div class="main-title">🔊 Asistente de Audio</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Convierte cualquier texto en una experiencia de audio.'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# IMAGEN
# ============================================================

image = Image.open("gato_raton.png")

st.image(
    image,
    width=350
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("🔊 Asistente de Audio")

    st.write(
        "Escribe o pega cualquier texto y conviértelo "
        "en audio de manera sencilla."
    )

    st.divider()

    st.subheader("🌎 Idioma")

    option_lang = st.selectbox(
        "Selecciona el idioma del audio:",
        ("Español", "English")
    )

    if option_lang == "Español":
        lg = "es"
    else:
        lg = "en"

    st.divider()

    st.info(
        "💡 Puedes pegar aquí textos largos, "
        "historias, apuntes, instrucciones o cualquier contenido "
        "que quieras escuchar."
    )


# ============================================================
# SECCIÓN DE TEXTO
# ============================================================

st.markdown(
    '<div class="card">',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-title">📝 Introduce tu texto</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="helper-text">'
    'Copia y pega aquí el texto que quieres escuchar.'
    '</div>',
    unsafe_allow_html=True
)

text = st.text_area(
    "Texto",
    placeholder="Escribe o pega tu texto aquí...",
    height=220,
    label_visibility="collapsed"
)

st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# FUNCIÓN TEXT TO SPEECH
# ============================================================

def text_to_speech(text, lg):

    tts = gTTS(
        text=text,
        lang=lg
    )

    # Nombre seguro para el archivo
    my_file_name = "audio_generado"

    file_path = f"temp/{my_file_name}.mp3"

    tts.save(file_path)

    return file_path


# ============================================================
# BOTÓN CONVERTIR
# ============================================================

if st.button("🎧 Convertir texto a audio"):

    if text.strip() == "":

        st.warning(
            "⚠️ Primero escribe o pega un texto."
        )

    else:

        with st.spinner("🎙️ Generando tu audio..."):

            audio_path = text_to_speech(
                text,
                lg
            )

        st.success(
            "✅ ¡Tu audio está listo!"
        )

        # ====================================================
        # REPRODUCTOR
        # ====================================================

        st.markdown(
            '<div class="card">',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="section-title">🎵 Tu audio</div>',
            unsafe_allow_html=True
        )

        audio_file = open(
            audio_path,
            "rb"
        )

        audio_bytes = audio_file.read()

        st.audio(
            audio_bytes,
            format="audio/mp3"
        )

        st.markdown("</div>", unsafe_allow_html=True)


        # ====================================================
        # DESCARGA
        # ====================================================

        with open(audio_path, "rb") as f:

            data = f.read()

        bin_str = base64.b64encode(data).decode()

        download_link = f"""
        <a href="data:audio/mp3;base64,{bin_str}"
           download="audio_generado.mp3"
           style="
               display:block;
               text-align:center;
               background-color:#252A34;
               color:white;
               padding:12px;
               border-radius:12px;
               text-decoration:none;
               font-weight:600;
               margin-top:10px;
           ">
           ⬇️ Descargar audio
        </a>
        """

        st.markdown(
            download_link,
            unsafe_allow_html=True
        )


# ============================================================
# LIMPIEZA DE ARCHIVOS ANTIGUOS
# ============================================================

def remove_files(n):

    mp3_files = glob.glob(
        "temp/*mp3"
    )

    if len(mp3_files) != 0:

        now = time.time()
        n_days = n * 86400

        for f in mp3_files:

            if os.stat(f).st_mtime < now - n_days:

                os.remove(f)


remove_files(7)
