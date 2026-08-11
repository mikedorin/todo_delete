from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DB='todo.db'

def init_db():
    conn=sqlite3.connect(DB)
    conn.execute('CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, task TEXT NOT NULL, completed INTEGER DEFAULT 0)')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn=sqlite3.connect(DB)
    tasks=conn.execute('SELECT * FROM tasks ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    task=request.form.get('task','').strip()
    if task:
        conn=sqlite3.connect(DB)
        conn.execute('INSERT INTO tasks (task) VALUES (?)',(task,))
        conn.commit(); conn.close()
    return redirect(url_for('index'))

@app.route('/complete/<int:task_id>')
def complete(task_id):
    conn=sqlite3.connect(DB)
    conn.execute('UPDATE tasks SET completed=1 WHERE id=?',(task_id,))
    conn.commit(); conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete(task_id):
    conn=sqlite3.connect(DB)
    conn.execute('DELETE FROM tasks WHERE id=?',(task_id,))
    conn.commit(); conn.close()
    return redirect(url_for('index'))

init_db()

if __name__ == '__main__':
    app.run(debug=True)
