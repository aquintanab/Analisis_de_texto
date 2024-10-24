import streamlit as st
from textblob import TextBlob
from googletrans import Translator

# Configuración inicial
st.set_page_config(
    page_title="Analizador de Sentimientos",
    page_icon="🎭"
)

# Función para analizar el sentimiento
def analyze_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity, blob.sentiment.subjectivity

# Función para obtener emoji y color basado en la polaridad
def get_sentiment_info(polarity):
    if polarity >= 0.6:
        return "😊", "Muy Positivo", "#28a745"
    elif polarity >= 0.2:
        return "🙂", "Positivo", "#7fb800"
    elif polarity <= -0.6:
        return "😢", "Muy Negativo", "#dc3545"
    elif polarity <= -0.2:
        return "🙁", "Negativo", "#ff6b6b"
    else:
        return "😐", "Neutral", "#ffc107"

# Título principal
st.title('🎭 Analizador de Sentimientos')

# Sidebar con información
with st.sidebar:
    st.markdown("## ℹ️ Información")
    st.info("""
    **Métricas de Análisis:**
    
    📊 **Polaridad (-1 a 1):**
    - -1: Muy negativo
    - 0: Neutral
    - 1: Muy positivo
    
    📈 **Subjetividad (0 a 1):**
    <div style='text-align: center; margin-top: 30px; padding: 20px; background-color: #f8f9fa;'>
        <p>Desarrollado con ❤️ usando Streamlit y TextBlob</p>
    </div>
""", unsafe_allow_html=True)
