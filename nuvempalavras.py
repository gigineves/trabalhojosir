import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re
from googleapiclient.discovery import build

# --- MELHORIA DE SEGURANÇA ---
# Carregue a chave da API do gerenciamento de segredos do Streamlit.
# Crie um arquivo .streamlit/secrets.toml e adicione sua chave lá.
# Exemplo de .streamlit/secrets.toml:
# YOUTUBE_API_KEY = "SUA_CHAVE_DE_API_AQUI"
YOUTUBE_API_KEY = st.secrets["AIzaSyDUYBTIuUDKZWA7UL_il8IDwtC1_N4tNJQ"]

def extract_video_id(url):
    """Extrai o ID do vídeo de uma URL do YouTube."""
    # Padrão para URLs de vídeos longos e curtos (shorts)
    match = re.search(r"(?:v=|\/shorts\/|youtu\.be\/)([a-zA-Z0-9_-]{11})", url)
    if match:
        return match.group(1)
    raise ValueError("ID do vídeo não encontrado na URL. Verifique se a URL é válida.")

def get_captions(video_id):
    """Tenta obter as legendas de um vídeo, primeiro com youtube_transcript_api, depois com a API do YouTube."""
    try:
        # Tenta buscar legendas em português ou inglês
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['pt', 'en'])
        full_text = " ".join([entry['text'] for entry in transcript])
        return full_text
    except (TranscriptsDisabled, NoTranscriptFound):
        st.info("Legendas não encontradas com a 'youtube_transcript_api'.")
        st.warning("Isso pode ocorrer se as legendas estiverem desativadas ou não existirem para este vídeo.")
        return None
    except Exception as e:
        st.error(f"Ocorreu um erro ao buscar legendas: {e}")
        return None

def generate_wordcloud(text):
    """Gera e exibe uma nuvem de palavras a partir de um texto."""
    wordcloud = WordCloud(width=800, height=400, background_color='white', collocations=False).generate(text)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    plt.tight_layout()
    return fig

def main():
    """Função principal da aplicação Streamlit."""
    st.set_page_config(page_title="Gerador de Nuvem de Palavras do YouTube", layout="wide")
    st.title("Gerador de Nuvem de Palavras para Vídeos do YouTube")
    st.write("Cole a URL de um vídeo do YouTube (normal ou Short) para criar uma nuvem de palavras a partir de suas legendas.")

    url = st.text_input("Cole a URL do YouTube aqui:", placeholder="Ex: https://www.youtube.com/watch?v=dQw4w9WgXcQ")

    if url:
        try:
            video_id = extract_video_id(url)
            with st.spinner(f"Processando vídeo com ID: {video_id}..."):
                text = get_captions(video_id)
                if text:
                    st.success("Legendas encontradas! Gerando a nuvem de palavras...")
                    fig = generate_wordcloud(text)
                    st.pyplot(fig)
                else:
                    st.warning("Não foi possível gerar a nuvem de palavras pois não foram encontradas legendas para este vídeo.")

        except ValueError as ve:
            st.error(f"Erro na URL: {ve}")
        except Exception as e:
            st.error(f"Ocorreu um erro inesperado: {e}")

if __name__ == "__main__":
    main()

      
