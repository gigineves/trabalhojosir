
import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from pytube import YouTube
import re

def extract_video_id(url):
   
    match = re.search(r"shorts/([a-zA-Z0-9_-]+)", url)
    if match:
        return match.group(1)  
    match = re.search(r"v=([a-zA-Z0-9_-]+)", url)
    if match:
        return match.group(1)
    raise ValueError("ID do vídeo não encontrado na URL")
print ('extract_video_id(url)')
def get_captions(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['pt', 'en'])
        full_text = " ".join([entry['text'] for entry in transcript])
        return full_text
    except (TranscriptsDisabled, NoTranscriptFound):
        return None
print( 'get_captions(video_id)')
def generate_wordcloud(text):
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    fig, ax = plt.subplots(figsize=(10, 5)) 
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    plt.tight_layout()
    return fig
print('generate_wordcloud(text)')
def main():
    st.title("Gerador de Nuvem de Palavras para YouTube Shorts")
    st.write("Cole a URL de um YouTube Short (ou vídeo normal) e veja a nuvem de palavras das legendas!")
    url = st.text_input("Cole a URL do YouTube Shorts: ")
print('main()')
    if url:
       try:
            video_id = extract_video_id(url)
            st.info(f"Tentando extrair legendas para o vídeo: **{video_id}**")

            text = get_captions(video_id)

            if text:
                st.success("Legendas encontradas! Gerando nuvem de palavras...")
               
                fig = generate_wordcloud(text)
                st.pyplot(fig)
            else:
                st.warning("Não foi possível obter legendas para esse vídeo. Isso pode acontecer se as legendas forem desabilitadas ou não existirem.")
        except ValueError as ve:
            st.error(f"Erro na URL: {ve}")
        except Exception as e:
            st.error(f"Ocorreu um erro inesperado: {e}") 

if __name__ == "__main__":
    main()

  
      
