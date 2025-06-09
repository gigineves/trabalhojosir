import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re

def get_video_id(url):
    """
    Extrai o ID do vídeo de uma URL do YouTube.
    """
    # Padrão de regex para encontrar o ID do vídeo em diferentes formatos de URL
    video_id_match = re.search(r'(?:v=|\/shorts\/|youtu\.be\/)([a-zA-Z0-9_-]{11})', url)
    return video_id_match.group(1) if video_id_match else None

def get_transcript(video_id):
    """
    Obtém a transcrição de um vídeo do YouTube.
    """
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['pt', 'en'])
        # Concatena o texto de todas as partes da transcrição
        full_transcript = " ".join([d['text'] for d in transcript_list])
        return full_transcript
    except Exception as e:
        st.error(f"Não foi possível obter a legenda: {e}")
        return None

def generate_word_cloud(text):
    """
    Gera e exibe uma nuvem de palavras.
    """
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)

# --- Interface do Streamlit ---

st.set_page_config(page_title="Nuvem de Palavras de YouTube Shorts", page_icon="☁️")

st.title("☁️ Gerador de Nuvem de Palavras para YouTube Shorts")
st.markdown("Cole a URL de um YouTube Shorts abaixo para gerar uma nuvem de palavras a partir da sua legenda.")

# Input da URL
url = st.text_input("URL do YouTube Shorts:", placeholder="https://www.youtube.com/shorts/...")

if st.button("Gerar Nuvem de Palavras"):
    if url:
        video_id = get_video_id(url)
        if video_id:
            with st.spinner("Extraindo legenda..."):
                transcript = get_transcript(video_id)
            if transcript:
                with st.spinner("Gerando a nuvem de palavras..."):
                    st.subheader("Nuvem de Palavras:")
                    generate_word_cloud(transcript)
        else:
            st.error("URL inválida. Por favor, insira uma URL de um vídeo do YouTube.")
    else:
        st.warning("Por favor, insira uma URL.")



