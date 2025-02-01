from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
import os
from uuid import uuid4

app = Flask(__name__)
app.secret_key = 'supersecretkey'
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

messages = []

# Ruta principal para iniciar sesión
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        if username.strip():
            session['username'] = username
            session['user_id'] = str(uuid4())
            return redirect(url_for('chat'))
    return render_template('login.html')

# Me odio a mi mismo por hacerlo en ingles solo porque se ve chido qihrcfgvvqbdghj
@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        text = request.form.get('text', '')
        image = request.files.get('image')

        image_path = ''
        if image and image.filename:
            image_filename = f"{uuid4()}_{image.filename}"
            image_path = os.path.join(UPLOAD_FOLDER, image_filename)
            image.save(image_path)

        messages.append({
            'user_id': session['user_id'],
            'username': session['username'],
            'text': text,
            'image_path': image_path
        })

    return render_template('chat.html', messages=messages, username=session['username'])

@app.route('/clear', methods=['POST'])
def clear_messages():
    messages.clear()
    # Eliminar imágenes cargadas
    for filename in os.listdir(UPLOAD_FOLDER):
        os.remove(os.path.join(UPLOAD_FOLDER, filename))
    return redirect(url_for('chat'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)
