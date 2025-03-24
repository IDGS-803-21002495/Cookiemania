from flask import Flask, render_template
from models import db
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig

app = Flask(__name__)
csrf = CSRFProtect()
app.config.from_object(DevelopmentConfig)

@app.route("/")
@app.route("/index")
def index():
	return render_template("index.html")

if __name__ == '__main__':
	csrf.init_app(app)
	db.init_app(app)
	with app.app_context():
		db.create_all()
		
	app.run(debug=True)