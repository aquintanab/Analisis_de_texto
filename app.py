import streamlit as st
from textblob import TextBlob

# Configuración de la página
st.set_page_config(
    page_title="Analizador de Sentimientos",
    page_icon="📊"
)

# Título y subtítulo
st.title('Analizador de Sentimientos')

# Agregar imagen
# Reemplaza 'ruta_de_tu_imagen.jpg' con la ruta real de tu imagen
# Por ejemplo: 'imagenes/analisis.jpg' o 'https://ejemplo.com/imagen.jpg'
try:
    st.image('sentimientos.jpg', 
             caption='Análisis de Sentimientos',
             use_column_width=True)
except:
    st.error("No se pudo cargar la imagen. Verifica la ruta del archivo.")

# Crear dos columnas
col1, col2 = st.columns([2, 1])

with col1:
    # Área de texto para input
    text_input = st.text_area("Escribe el texto a analizar:", height=150)

with col2:
    st.write("### Información")
    st.write("""
    Este analizador evalúa:
    - Polaridad (positivo/negativo)
    - Subjetividad (objetivo/subjetivo)
    """)

if text_input:
    try:
        # Realizar análisis
        blob = TextBlob(text_input)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        
        # Crear tres columnas para los resultados
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### Sentimiento")
            if polarity > 0:
                st.markdown("### 😊")
                st.write("Positivo")
            elif polarity < 0:
                st.markdown("### 😔")
                st.write("Negativo")
            else:
                st.markdown("### 😐")
                st.write("Neutral")
        
        with col2:
            st.markdown("### Polaridad")
            st.write(f"{polarity:.2f}")
            # Barra de progreso para polaridad
            st.progress((polarity + 1)/2)
        
        with col3:
            st.markdown("### Subjetividad")
            st.write(f"{subjectivity:.2f}")
            # Barra de progreso para subjetividad
            st.progress(subjectivity)
        
        # Interpretación detallada
        st.markdown("### Análisis Detallado")
        
        # Interpretación de polaridad
        st.write("**Polaridad:**")
        if polarity > 0.5:
            st.success("Este texto es muy positivo")
        elif polarity > 0:
            st.info("Este texto es ligeramente positivo")
        elif polarity < -0.5:
            st.error("Este texto es muy negativo")
        elif polarity < 0:
            st.warning("Este texto es ligeramente negativo")
        else:
            st.info("Este texto es neutral")
        
        # Interpretación de subjetividad
        st.write("**Subjetividad:**")
        if subjectivity > 0.7:
            st.write("📝 Este texto es muy subjetivo (basado en opiniones personales)")
        elif subjectivity > 0.3:
            st.write("📊 Este texto mezcla hechos y opiniones")
        else:
            st.write("📈 Este texto es muy objetivo (basado en hechos)")
            
    except Exception as e:
        st.error(f"Ocurrió un error al analizar el texto: {str(e)}")

# Footer
st.markdown("---")
st.markdown("### Cómo usar el analizador:")
st.write("""
1. Escribe o pega tu texto en el área de entrada
2. El análisis se realizará automáticamente
3. Revisa los resultados en las diferentes secciones
""")
