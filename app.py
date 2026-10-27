from flask import Flask, request, redirect, send_from_directory
import yt_dlp
import os

app = Flask(__name__)

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/download')
def download():
    video_url = request.args.get('url')

    if not video_url:
        return "URL nahi diya gaya!", 400

    try:
        ydl_opts = {
            'format': 'best',
            'quiet': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            direct_url = info.get('url')
            
            if not direct_url:
                return "Video link extract nahi ho paya.", 500
                
            return redirect(direct_url)

    except Exception as e:
        print(f"Error: {e}")
        return "Video download karne mein error aaya. YouTube ki restriction ho sakti hai.", 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    
