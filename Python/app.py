from flask import Flask, render_template, request, jsonify, session, Response, redirect, url_for, send_file
import speech_recognition as sr
import pyttsx3
from googletrans import Translator, LANGUAGES
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import io


from gtts import gTTS


# Initialize Flask
app = Flask(__name__)
app.secret_key = 'sriakash@7695978704'

# Initialize global variables

translator = Translator(service_urls=["translate.google.com"])

# Connecting to DB

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'credentials_db'

mysql = MySQL(app)


# End point for Signin Page
@app.route("/")
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    session['text'] = ""
    session['trans'] = ""
    session['lang'] = ""
    msg = ''
    if request.method == 'POST' and 'txt_user' in request.form and 'txt_pass' in request.form:
        username = request.form['txt_user']
        password = request.form['txt_pass']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM tbl_signup WHERE username = % s AND password = % s', (username, password,))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            session['email'] = account['email']
            session['password'] = account['password']
            return render_template('home.html', user=session.get('username'), email=session['email'],
                                   pasw=session['password'])
        else:
            msg = 'Incorrect username / password !'
    return render_template('signin.html', msg=msg)


# End point for Signup Page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    msg = ""
    if request.method == 'POST' and 'txt_user' in request.form and 'txt_pass' in request.form and 'txt_email' in request.form:
        user = request.form["txt_user"]
        email = request.form["txt_email"]
        pasw = request.form["txt_pass"]
        conf = request.form["txt_conf"]
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM tbl_signup WHERE username = % s', (user,))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif len(user) < 4:
            msg = 'User name must be greater than 3.'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', user):
            msg = 'Username must contain only characters and numbers !'
        elif pasw != conf:
            msg = 'Password does\'t matched with Confirm Password.'
        else:
            cursor.execute('INSERT INTO tbl_signup VALUES (NULL, % s, % s, % s)', (user, email, pasw))
            mysql.connection.commit()
            msg = 'You have successfully registered !'
            return render_template('signin.html')
    return render_template('signup.html', msg=msg)


# End point for Signout
@app.route('/signout')
def signout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    session.pop('password', None)
    session.pop('email', None)
    return redirect(url_for('signin'))


# End point for Redirecting to Home Page
@app.route('/redirect-home')
def redirect_home():
    return render_template('home.html')


# End point for Language Translator App
@app.route('/demoLangTrans')
def app_lang_trans():
    return render_template('index.html')


# End point for Turn on the Mic on Language Translator App
@app.route('/mic-on')
def recognize():
    try:
        rec = sr.Recognizer()
        with sr.Microphone() as source:
            rec.adjust_for_ambient_noise(source, duration=0.2)
            audio = rec.listen(source, timeout=5)

        text = rec.recognize_sphinx(audio)

    except sr.UnknownValueError:
        text = "Speech Recognition could not understand the audio."
    except sr.RequestError as e:
        text = f"Could not request results from Speech Recognition Service: {e}"

    session['text'] = text
    return render_template('index.html', spoken=session['text'])


# End point for Initializing languages on Language Translator App
@app.route('/get_languages', methods=['GET'])
def get_languages():
    languages = list(LANGUAGES.values())
    return jsonify(languages=languages)


# End point for convert the text on Language Translator App
@app.route('/convert', methods=['GET', 'POST'])
def convert():
    vowel = alpha = digits = sym = space = 0
    words = 1
    selected_lang = request.form.get('lang')

    session['lang'] = selected_lang

    text = session.get('text', '')

    if not text:
        return render_template('index.html', translated="No text to translate")

    translation = translator.translate(text, dest=selected_lang).text
    session['trans'] = translation
    for char in translation:
        if char.isspace():
            space += 1
            words += 1
        elif char.isalpha():
            alpha += 1
            if char in "aeiou":
                vowel += 1
        elif char.isdigit():
            digits += 1
        else:
            sym += 1

    session['text'] = text
    return render_template('index.html', translated=translation, spoken=text, words=words, alphabets=alpha, digits=digits, specialChars=sym, whitespaces=space, vowel=vowel)


# End point for Turn on the Voice on Language Translator App
@app.route('/speak-on')
def speak():
    translation = session.get('trans', '')
    if translation:
        tts = pyttsx3.init()
        tts.say(translation)
        tts.runAndWait()
    return render_template('index.html', translated=translation, spoken=session['text'])


# End point for Download the Text File on Language Translator App
@app.route('/download')
def download():
    text_content = session.get('trans', '')

    response = Response(text_content, content_type='text/plain')
    response.headers["Content-Disposition"] = "attachment; filename=downloaded_text.txt"

    return response


# End point for Text to Speech App
@app.route('/demoTextSpeech')
def app_text_to_speech():
    return render_template('textToSpeech.html')


# End point for Download the Audio file on Text to Speech App
@app.route('/download-audio', methods=['GET', 'POST'])
def download_audio():
    text = request.form.get('input_text')

    if not text.strip():
        return render_template('textToSpeech.html', err="Text cannot be empty.")

    audio_buffer = io.BytesIO()
    tta = gTTS(text)
    tta.write_to_fp(audio_buffer)
    audio_buffer.seek(0)

    return send_file(audio_buffer, as_attachment=True, download_name='audio.mp3', mimetype='audio/mp3')


if __name__ == '__main__':
    app.run(debug=True)
