from flask import Flask, render_template, request, send_from_directory, redirect, url_for, flash
import yt_dlp
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

downloaded_videos = []

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', videos=downloaded_videos)

@app.route('/download_video', methods=['POST'])
def download_video():
    link = request.form['link']
    if link:
        try:
            ydl_opts = {'format': 'best', 'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s')}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(link, download=True)
                title = info.get('title', 'Unknown Title')
                filename = ydl.prepare_filename(info)
                downloaded_videos.append({
                    'title': title,
                    'filename': os.path.basename(filename)
                })
            flash("Download completed on server!", "success")
        except Exception as e:
            flash(f"Error: {e}", "error")
    else:
        flash("Please enter a valid link.", "error")

    return redirect(url_for('index'))

@app.route('/downloads/<filename>')
def download_file(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico')

if __name__ == '__main__':
    app.run(debug=True)
