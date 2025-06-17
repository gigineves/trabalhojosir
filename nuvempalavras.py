import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from pytube import YouTube
import re
from googleapiclient.discovery import build 


YOUTUBE_API_KEY = "AIzaSyDUYBTIuUDKZWA7UL_il8IDwtC1_N4tNJQ" 


def extract_video_id(url):
    match = re.search(r"shorts/([a-zA-Z0-9_-]+)", url)
    if match:
        return match.group(1)   
    match = re.search(r"v=([a-zA-Z0-9_-]+)", url)
    if match:
        return match.group(1)
    raise ValueError("ID do vídeo não encontrado na URL")

def get_captions(video_id):
    
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['pt', 'en'])
        full_text = " ".join([entry['text'] for entry in transcript])
        return full_text
    except (TranscriptsDisabled, NoTranscriptFound):
        st.info("Legendas não encontradas com youtube_transcript_api. Tentando com YouTube Data API v3...")
       
        try:
            youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
            
            
            captions_response = youtube.captions().list(
                part='snippet',
                videoId=video_id
            ).execute()

            if captions_response and captions_response.get('items'):
               
                caption_id = None
                for item in captions_response['items']:
                    if item['snippet']['language'] in ['pt', 'en']:
                        caption_id = item['id']
                        break
                if not caption_id: 
                    caption_id = captions_response['items'][0]['id']

               

                st.warning("A YouTube Data API v3 detectou legendas, mas não pode baixá-las diretamente para o público. A 'youtube_transcript_api' é geralmente mais eficaz para baixar o conteúdo.")
                return None 
            else:
                return None 
        except Exception as e:
            st.error(f"Erro ao tentar obter legendas com YouTube Data API v3: {e}")
            return None 
def generate_wordcloud(text):
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    fig, ax = plt.subplots(figsize=(10, 5)) 
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    plt.tight_layout()
    return fig

def main():
    st.title("Gerador de Nuvem de Palavras para YouTube Shorts e Vídeos")
    st.write("Cole a URL de um YouTube Short (ou vídeo normal) e veja a nuvem de palavras das legendas!")

    url = st.text_input("Cole a URL do YouTube aqui:") 

    if url: 
        try: 
            video_id = extract_video_id(url)
            st.info(f"Tentando extrair legendas para o vídeo: {video_id}") 
            text = get_captions(video_id) 
            if text: 
                st.success("Legendas encontradas! Gerando nuvem de palavras...") 
                fig = generate_wordcloud(text) 
                st.pyplot(fig) 
            else:
                st.warning("Não foi possível obter legendas para esse vídeo. Isso pode acontecer se as legendas forem desabilitadas, não existirem, ou se for um YouTube Short sem legendas acessíveis pelas APIs.") 
       
        except ValueError as ve: 
            st.error(f"Erro na URL: {ve}") 
       
        except Exception as e: 
            st.error(f"Ocorreu um erro inesperado: {e}") 

if __name__ == "__main__":
    main()

      
