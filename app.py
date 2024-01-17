from flask import Flask, render_template, request, jsonify, g
import sqlite3

DATABASE = 'stickynotes.db'

app = Flask(__name__)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row  # Enable dictionary-like access to row items
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/main")
def main():
    return render_template('main.html')


@app.route("/hobby")
def hobby():
    return render_template('hobby.html')


@app.route("/portfolio")
def portfolio():
    return render_template('portfolio.html')


@app.route("/contact")
def contact():
    return render_template('contact.html')


@app.route("/notes", methods=['GET', 'POST', 'PUT', 'DELETE'])
def notes():
    db = get_db()
    cursor = db.cursor()

    if request.method == 'GET':
        cursor.execute('SELECT * FROM notes')
        notes = cursor.fetchall()
        notes_list = [{'id': note['id'], 'content': note['content']} for note in notes]
        return jsonify(notes_list)

    if request.method == 'POST':
        content = request.json['content']
        cursor.execute('INSERT INTO notes (content) VALUES (?)', (content,))
        db.commit()
        return jsonify(id=cursor.lastrowid, content=content)

    if request.method == 'PUT':
        note_id = request.json['id']
        content = request.json['content']
        cursor.execute('UPDATE notes SET content = ? WHERE id = ?', (content, note_id))
        db.commit()
        return jsonify(id=note_id, content=content)

    if request.method == 'DELETE':
        note_id = request.json['id']
        cursor.execute('DELETE FROM notes WHERE id = ?', (note_id,))
        db.commit()
        return jsonify(id=note_id)

    return render_template('shoutout.html')  # This should point to the actual notes page template


@app.route('/initdb')
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
    return 'Initialized the database.'


@app.route('/notes/update', methods=['POST'])
def update_note():
    note_id = request.json['id']
    new_content = request.json['content']
    conn = get_db()
    conn.execute('UPDATE notes SET content = ? WHERE id = ?', (new_content, note_id))
    conn.commit()
    return jsonify({'id': note_id, 'content': new_content})


@app.route('/notes/delete', methods=['POST'])
def delete_note():
    note_id = request.json['id']
    conn = get_db()
    conn.execute('DELETE FROM notes WHERE id = ?', (note_id,))
    conn.commit()
    return jsonify({'id': note_id})
@app.route("/shoutout")
def shoutout():
    return render_template('shoutout.html')


if __name__ == "__main__":
    app.run()
