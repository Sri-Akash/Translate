from flask import Flask, render_template, request, jsonify, session, Response
import speech_recognition as sr
import pyttsx3
from googletrans import Translator, LANGUAGES
from flask_ngrok import run_with_ngrok

# Initialize Flask
app = Flask(__name__)
app.secret_key = 'sriakash@7695978704'

run_with_ngrok(app)

# Initialize global variables

rec = sr.Recognizer()
translator = Translator(service_urls=["translate.google.com"])
tts = pyttsx3.init()


@app.route('/')
def home():
    session['text'] = ""
    session['trans'] = ""
    session['lang'] = ""
    return render_template('index.html')


@app.route('/mic-on')
def recognize():
    try:
        with sr.Microphone() as source:
            rec.adjust_for_ambient_noise(source)
            audio = rec.listen(source)

        text = rec.recognize_google(audio)

    except sr.UnknownValueError:
        text = "Google Speech Recognition could not understand the audio."
    except sr.RequestError as e:
        text = f"Could not request results from Speech Recognition Service: {e}"

    session['text'] = text
    return render_template('index.html', spoken=text)


@app.route('/get_languages', methods=['GET'])
def get_languages():
    languages = list(LANGUAGES.values())
    return jsonify(languages=languages)


@app.route('/convert', methods=['GET', 'POST'])
def convert():
    selected_lang = request.form.get('lang')

    session['lang'] = selected_lang

    text = session.get('text', '')

    if not text:
        return render_template('index.html', translated="No text to translate")

    translation = translator.translate(text, dest=selected_lang).text
    session['trans'] = translation

    return render_template('index.html', translated=translation)


@app.route('/speak-on')
def speak():
    translation = session.get('trans', '')
    if translation:
        tts.say(translation)
        tts.runAndWait()
    return render_template('index.html', translated=translation)


@app.route('/download')
def download():
    text_content = session.get('trans', '')

    response = Response(text_content, content_type='text/plain')
    response.headers["Content-Disposition"] = "attachment; filename=downloaded_text.txt"

    return response


if __name__ == '__main__':
    app.run()
