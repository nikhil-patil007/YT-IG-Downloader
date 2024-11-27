from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
import os
import yt_dlp
import instaloader

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['DOWNLOAD_FOLDER'] = 'static/downloads'

# Ensure download folder exists
os.makedirs(app.config['DOWNLOAD_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url')
        if not url:
            flash('Please provide a valid URL.', 'error')
            return redirect(url_for('index'))

        # YouTube Download Logic
        if 'youtube.com' in url or 'youtu.be' in url:
            try:
                ydl_opts = {
                    'outtmpl': f"{app.config['DOWNLOAD_FOLDER']}/%(title)s.%(ext)s",
                    'format': 'best[ext=mp4]/best',
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                flash('YouTube video downloaded successfully.', 'success')
            except Exception as e:
                flash(f"Error downloading YouTube video: {e}", 'error')

        # Instagram Download Logic
        elif 'instagram.com' in url:
            try:
                loader = instaloader.Instaloader(download_pictures=True, download_videos=True)
                profile_name = url.split('/')[-2]
                download_path = os.path.join(app.config['DOWNLOAD_FOLDER'], profile_name)
                os.makedirs(download_path, exist_ok=True)
                loader.download_profile(profile_name, profile_pic=False, fast_update=True)
                flash('Instagram content downloaded.', 'success')
            except Exception as e:
                flash(f"Error downloading Instagram content: {e}", 'error')

        # Unsupported URL
        else:
            flash('Unsupported URL. Please provide a valid YouTube or Instagram link.', 'error')

        return redirect(url_for('index'))

    return render_template('index.html')

@app.route('/downloads/<path:filename>')
def download_file(filename):
    return send_from_directory(app.config['DOWNLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
