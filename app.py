from flask import Flask, render_template, flash, redirect
from config import *


app = Flask(__name__)
app.secret_key = SECRET


# Startpage
@app.route('/')
def startpage():
    return render_template('startpage.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
