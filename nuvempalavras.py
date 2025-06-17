import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound, YouTubeRequestFailed
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re

# --- Configuração de Segurança ---
# Carrega a chave da API do Streamlit Secrets.
# Certifique-se de ter um arquivo .streamlit/secrets.toml no seu repositório com:
# YOUTUBE_API_KEY = "SUA_CHAVE_DE_API_AQUI"
YOUTUBE_API_KEY = st.secrets.get("YOUTUBE_API_KEY", "") # Usa .get para evitar erro se a chave não estiver configurada

def extract_video_id(url):
    """Extrai o ID do vídeo de uma URL do YouTube."""
    # Padrão para URLs de vídeos longos e curtos (shorts)
    match = re.search(r"(?:v=|\/shorts\/|youtu\.be\/)([a-zA-Z0-9_-]{11})", url)
    if match:
        return match.group(1)
    raise ValueError("ID do vídeo não encontrado na URL. Verifique se a URL é válida.")

def get_captions(video_id):
    """Tenta obter as legendas de um vídeo usando youtube_transcript_api."""
    try:
        # Tenta buscar legendas em português ou inglês
        # Se você for usar proxies, o argumento 'proxies' seria adicionado aqui.
        # Ex: transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['pt', 'en'], proxies=your_proxy_dict)
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['pt', 'en'])
        full_text = " ".join([entry['text'] for entry in transcript])
        return full_text
    except (TranscriptsDisabled, NoTranscriptFound):
        st.info("Legendas não encontradas para este vídeo com a 'youtube_transcript_api'.")
        st.warning("Isso pode ocorrer se as legendas estiverem desativadas ou não existirem nos idiomas português ou inglês.")
        return None
    except YouTubeRequestFailed as e:
        # Este erro geralmente indica um bloqueio de IP ou problema de conexão com o YouTube.
        st.error(f"Ocorreu um erro ao buscar legendas: {e}")
        st.warning("O YouTube pode estar bloqueando as requisições do seu IP (comum em servidores de nuvem). Considere usar proxies ou tente novamente mais tarde.")
        return None
    except Exception as e:
        st.error(f"Ocorreu um erro inesperado ao buscar legendas: {e}")
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
        # Verifica se a chave da API do YouTube está configurada.
        # Embora não esteja sendo usada diretamente para buscar legendas, é uma boa prática verificar.
        # Se a API do Google (googleapiclient) for usada em outro lugar, ela precisará desta chave.
        if not YOUTUBE_API_KEY and False: # Se você for usar a googleapiclient.discovery.build, remova o "and False"
             st.warning("A chave da API do YouTube não foi configurada. Algumas funcionalidades (se implementadas) podem não funcionar.")

        try:
            video_id = extract_video_id(url)
            with st.spinner(f"Processando vídeo com ID: {video_id}..."):
                text = get_captions(video_id)
                if text:
                    st.success("Legendas encontradas! Gerando a nuvem de palavras...")
                    fig = generate_wordcloud(text)
                    st.pyplot(fig)
                else:
                    st.warning("Não foi possível gerar a nuvem de palavras pois não foram encontradas legendas para este vídeo ou houve um erro.")

        except ValueError as ve:
            st.error(f"Erro na URL: {ve}")
        except Exception as e:
            st.error(f"Ocorreu um erro inesperado: {e}")

if __name__ == "__main__":
    main()


      
