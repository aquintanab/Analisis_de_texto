import streamlit as st
from textblob import TextBlob

# Título simple
st.title('Analizador de Sentimientos')
st.write('Analiza el sentimiento de cualquier texto')

# Área de texto para input
text_input = st.text_area("Escribe el texto a analizar:", height=100)

if text_input:
    # Realizar análisis
    blob = TextBlob(text_input)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
    
    # Determinar el sentimiento
    if polarity > 0:
        sentiment = "Positivo 😊"
    elif polarity < 0:
        sentiment = "Negativo 😔"
    else:
        sentiment = "Neutral 😐"
    
    # Mostrar resultados
    st.write("### Resultados del análisis:")
    st.write(f"Sentimiento: {sentiment}")
    st.write(f"Polaridad: {polarity:.2f}")
    st.write(f"Subjetividad: {subjectivity:.2f}")
    
    # Interpretación
    st.write("\n### Interpretación:")
    
    # Polaridad
    st.write("**Polaridad:**")
    if polarity > 0.5:
        st.write("El texto es muy positivo")
    elif polarity > 0:
        st.write("El texto es ligeramente positivo")
    elif polarity < -0.5:
        st.write("El texto es muy negativo")
    elif polarity < 0:
        st.write("El texto es ligeramente negativo")
    else:
        st.write("El texto es neutral")
    
    # Subjetividad
    st.write("\n**Subjetividad:**")
    if subjectivity > 0.7:
        st.write("El texto es muy subjetivo (opiniones personales)")
    elif subjetivity > 0.3:
        st.write("El texto tiene un balance entre hechos y opiniones")
    else:
        st.write("El texto es muy objetivo (basado en hechos)")

# Sección de corrección
st.write("\n### Corrección de texto")
correction_text = st.text_area("Escribe el texto a corregir:", key="correction")

if correction_text:
    blob = TextBlob(correction_text)
    corrected = str(blob.correct())
    
    if corrected != correction_text:
        st.write("Texto corregido:")
        st.write(corrected)
    else:
        st.write("No se encontraron errores que corregir")
