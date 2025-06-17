import streamlit as st
from googleapiclient.discovery import build
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')
nltk.download('punkt')

stop_words_pt = set(stopwords.words('portuguese'))
stop_words_en = set(stopwords.words('english'))

def extract_video_id(url):
    """Extrai o ID do vídeo da URL."""
    match = re.search(r"(?:v=|\/shorts\/|youtu\.be\/)([a-zA-Z0-9_-]{11})", url)
    return match.group(1) if match else None

def get_video_comments(video_id, api_key, max_results=100):
    """Busca comentários usando a API v3."""
    try:
        youtube = build('youtube', 'v3', developerKey=api_key)
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=max_results,
            textFormat="plainText"
        )
        response = request.execute()
        return " ".join([item['snippet']['topLevelComment']['snippet']['textDisplay'] for item in response.get('items', [])])
    except Exception as e:
        st.error(f"Erro ao buscar comentários: {e}")
        return None

def generate_wordcloud(text):
    """Gera a nuvem de palavras."""
    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color='white',
        stopwords=stop_words_pt.union(stop_words_en)
    ).generate(text)
    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")
    return fig

st.set_page_config(page_title="Nuvem de Comentários do YouTube", layout="wide")
st.title("☁️ Nuvem de Palavras - Comentários do YouTube")

api_key = st.secrets.get("YOUTUBE_API_KEY", "")
url = st.text_input("Cole a URL do vídeo do YouTube:")
max_comments = st.slider("Número máximo de comentários:", 10, 200, 50)

if url and api_key:
    video_id = extract_video_id(url)
    if video_id:
        if st.button("Gerar Nuvem de Palavras"):
            with st.spinner("Buscando comentários..."):
                comments_text = get_video_comments(video_id, api_key, max_comments)
            if comments_text:
                with st.spinner("Criando nuvem de palavras..."):
                    st.pyplot(generate_wordcloud(comments_text))
            else:
                st.warning("Nenhum comentário encontrado.")
    else:
        st.error("URL inválida.")
elif not api_key:
    st.error("Chave da API do YouTube não configurada.")


      
