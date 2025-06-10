
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
    # Padrão normal de URL
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
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.tight_layout()
    plt.show()
print('generate_wordcloud(text)')
def main():
   url = st.text_input("Cole a URL do YouTube Shorts: ")
print('main()')
   if url:
       try:
           video_id = extract_video_id(url)
           print(f"[+] Extraindo legendas do vídeo ID: {video_id}")
           text = get_captions(video_id)
           if text:
               print("[+] Legendas encontradas. Gerando nuvem de palavras...")
               generate_wordcloud(text)
           else:
               print("[-] Não foi possível obter legendas para esse vídeo.")
       except Exception as e:
           print(f"Erro: {e}")

if __name__ == "__main__":
    main()

  
      
