import streamlit as st
from googleapiclient.discovery import build
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re
from nltk.corpus import stopwords
import nltk

# Baixa stopwords (palavras irrelevantes como "o", "de", etc.)
nltk.download('stopwords')
stop_words_pt = set(stopwords.words('portuguese'))
stop_words_en = set(stopwords.words('english'))

# Configuração da API
YOUTUBE_API_KEY = st.secrets.get("YOUTUBE_API_KEY")  # Chave no secrets.toml

# --- Funções ---
def extract_video_id(url):
    """Extrai o ID do vídeo da URL."""
    match = re.search(r"(?:v=|\/shorts\/|youtu\.be\/)([a-zA-Z0-9_-]{11})", url)
    return match.group(1) if match else None

def get_video_comments(video_id, max_results=100):
    """Busca comentários usando a API v3."""
    try:
        youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=max_results,
            textFormat="plainText"
        )
        response = request.execute()
        
        comments = []
        for item in response.get('items', []):
            comment = item['snippet']['topLevelComment']['snippet']
            comments.append(comment['textDisplay'])
        
        return " ".join(comments)  # Junta todos os comentários em um único texto
    
    except Exception as e:
        st.error(f"Erro ao buscar comentários: {e}")
        return None

def clean_text(text):
    """Remove stopwords, links e caracteres especiais."""
    text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)  # Remove URLs
    text = re.sub(r'\W', ' ', text)  # Remove caracteres não alfanuméricos
    text = text.lower()  # Converte para minúsculas
    # Remove stopwords em português e inglês
    text = " ".join([word for word in text.split() if word not in stop_words_pt and word not in stop_words_en])
    return text

def generate_wordcloud(text):
    """Gera a nuvem de palavras."""
    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color='white',
        collocations=False,  # Evita repetições
        stopwords=stop_words_pt.union(stop_words_en)  # Filtra stopwords adicionais
    ).generate(text)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    return fig

# --- Interface Streamlit ---
st.set_page_config(page_title="Nuvem de Comentários do YouTube", layout="wide")
st.title("☁️ Nuvem de Palavras de Comentários do YouTube")

url = st.text_input("Cole a URL do vídeo:", placeholder="Ex: https://www.youtube.com/watch?v=...")
max_comments = st.slider("Número máximo de comentários:", 10, 200, 50)

if url:
    video_id = extract_video_id(url)
    if video_id:
        st.write(f"🔍 Analisando vídeo: `{video_id}`")
        
        if st.button("Gerar Nuvem de Palavras"):
            with st.spinner("Buscando comentários..."):
                comments_text = get_video_comments(video_id, max_results=max_comments)
            
            if comments_text:
                with st.spinner("Processando texto..."):
                    cleaned_text = clean_text(comments_text)
                    fig = generate_wordcloud(cleaned_text)
                
                st.success("Nuvem de palavras gerada!")
                st.pyplot(fig)
                
                # Opcional: Mostrar estatísticas
                st.subheader("📊 Estatísticas")
                col1, col2 = st.columns(2)
                col1.metric("Total de comentários", max_comments)
                col2.metric("Palavras únicas", len(set(cleaned_text.split())))
                
                # Opcional: Mostrar comentários brutos (expandível)
                with st.expander("Ver comentários originais"):
                    st.text(comments_text[:5000] + "...")  # Limita a exibição
            else:
                st.warning("Nenhum comentário encontrado ou vídeo sem permissão.")
    else:
        st.error("URL inválida. Exemplo válido: https://www.youtube.com/watch?v=dQw4w9WgXcQ")


      
