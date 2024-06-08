from flask import Flask, request, render_template, send_from_directory
from pytube import YouTube, exceptions
import os

app = Flask(__name__)
app.config['DOWNLOAD_FOLDER'] = 'downloads'

if not os.path.exists(app.config['DOWNLOAD_FOLDER']):
    os.makedirs(app.config['DOWNLOAD_FOLDER'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    print(f"Received URL: {url}")  # Débogage : Affiche l'URL reçue
    try:
        yt = YouTube(url)
        stream = yt.streams.get_highest_resolution()
        file_path = os.path.join(app.config['DOWNLOAD_FOLDER'], stream.default_filename)
        stream.download(output_path=app.config['DOWNLOAD_FOLDER'])
        return send_from_directory(app.config['DOWNLOAD_FOLDER'], stream.default_filename, as_attachment=True)
    except exceptions.VideoUnavailable:
        error_message = "Error: The video is unavailable."
        print(error_message)
        return error_message
    except exceptions.AgeRestrictedError:
        error_message = "Error: The video is age-restricted and cannot be accessed without logging in."
        print(error_message)
        return error_message
    except Exception as e:
        error_message = f"Error: {str(e)}"
        print(error_message)
        return error_message

if __name__ == '__main__':
    app.run(debug=True)
