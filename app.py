# Requirements (comentados para referencia):
# streamlit==1.32.0
# textblob==0.17.1
# plotly==5.18.0
# googletrans==3.1.0a0

import streamlit as st
from textblob import TextBlob
from googletrans import Translator
import plotly.graph_objects as go
import time

# Instalar NLTK data necesario para TextBlob
import nltk
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

# Configuración inicial
st.set_page_config(
    page_title="Analizador de Sentimientos",
    page_icon="🎭",
    layout="wide"
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

# Título principal con estilo
st.markdown("""
    <h1 style='text-align: center; color: #2E86C1;'>
        🎭 Analizador Avanzado de Sentimientos
    </h1>
""", unsafe_allow_html=True)

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
    - 0: Muy objetivo
    - 1: Muy subjetivo
    """)
    
    # Selector de idioma
    st.markdown("### 🌐 Configuración de Idioma")
    language = st.selectbox(
        "Selecciona el idioma de entrada:",
        ["Español", "English"],
        index=0
    )

# Tabs principales
tab1, tab2, tab3 = st.tabs(["📝 Análisis de Texto", "📊 Visualización", "✍️ Corrección"])

# Inicializar el traductor
translator = Translator()

with tab1:
    # Campo de entrada de texto
    text_input = st.text_area("Ingresa el texto a analizar:", height=150)
    
    if text_input:
        with st.spinner('Analizando...'):
            try:
                # Traducir al inglés si el texto está en español
                if language == "Español":
                    translation = translator.translate(text_input, src='es', dest='en')
                    analysis_text = translation.text
                else:
                    analysis_text = text_input
                
                polarity, subjectivity = analyze_sentiment(analysis_text)
                
                # Mostrar resultados con estilo
                col1, col2, col3 = st.columns(3)
                
                emoji, sentiment_label, color = get_sentiment_info(polarity)
                
                with col1:
                    st.markdown(f"""
                        <div style='text-align: center; padding: 20px; background-color: {color}; border-radius: 10px; color: white;'>
                            <h3>Sentimiento</h3>
                            <h2>{emoji} {sentiment_label}</h2>
                        </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                        <div style='text-align: center; padding: 20px; background-color: #17a2b8; border-radius: 10px; color: white;'>
                            <h3>Polaridad</h3>
                            <h2>{polarity:.2f}</h2>
                        </div>
                    """, unsafe_allow_html=True)
                    
                with col3:
                    st.markdown(f"""
                        <div style='text-align: center; padding: 20px; background-color: #6f42c1; border-radius: 10px; color: white;'>
                            <h3>Subjetividad</h3>
                            <h2>{subjectivity:.2f}</h2>
                        </div>
                    """, unsafe_allow_html=True)
                    
                # Almacenar en el historial
                if 'texts_analyzed' not in st.session_state:
                    st.session_state.texts_analyzed = []
                    st.session_state.polarities = []
                    st.session_state.subjectivities = []
                
                if text_input not in st.session_state.texts_analyzed:
                    st.session_state.texts_analyzed.append(text_input)
                    st.session_state.polarities.append(polarity)
                    st.session_state.subjectivities.append(subjectivity)
                    
            except Exception as e:
                st.error(f"Error en el análisis: {str(e)}")

with tab2:
    if 'texts_analyzed' in st.session_state and st.session_state.texts_analyzed:
        # Gráfico de dispersión
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=st.session_state.polarities,
            y=st.session_state.subjectivities,
            mode='markers+text',
            text=[f'Texto {i+1}' for i in range(len(st.session_state.texts_analyzed))],
            textposition='top center',
            marker=dict(
                size=12,
                color=st.session_state.polarities,
                colorscale='RdYlGn',
                showscale=True
            )
        ))
        
        fig.update_layout(
            title='Análisis de Sentimientos - Distribución',
            xaxis_title='Polaridad',
            yaxis_title='Subjetividad',
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Mostrar historial
        with st.expander("Ver Historial de Análisis"):
            for i, (text, pol, sub) in enumerate(zip(
                st.session_state.texts_analyzed,
                st.session_state.polarities,
                st.session_state.subjectivities
            )):
                st.write(f"**Texto {i+1}:**")
                st.write(f"- Contenido: {text}")
                st.write(f"- Polaridad: {pol:.2f}")
                st.write(f"- Subjetividad: {sub:.2f}")
                st.write("---")
    else:
        st.info("Aún no hay datos para visualizar. Analiza algunos textos primero.")

with tab3:
    correction_text = st.text_area("Ingresa el texto a corregir:", height=150, key='correction')
    if correction_text:
        try:
            blob = TextBlob(correction_text)
            corrected_text = str(blob.correct())
            st.success("Texto corregido:")
            st.write(corrected_text)
            
            # Mostrar diferencias
            if correction_text != corrected_text:
                st.warning("Cambios realizados:")
                st.write(f"Original: {correction_text}")
                st.write(f"Corregido: {corrected_text}")
        except Exception as e:
            st.error(f"Error en la corrección: {str(e)}")

# Agregar footer
st.markdown("""
    <div style='text-align: center; margin-top: 30px; padding: 20px; background-color: #f8f9fa;'>
        <p>Desarrollado con ❤️ usando Streamlit y TextBlob</p>
    </div>
""", unsafe_allow_html=True)
