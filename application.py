from flask import Flask, render_template, jsonify
# import boto3
# import dataset

# Create an instance of Flask class (represents our application)
# Pass in name of application's module (__name__ evaluates to current module name)
app = Flask(__name__, template_folder='./templates',static_folder='./templates/static')
application = app  # AWS EB requires it to be called "application"


# Provide a landing page with some documentation on how to use API
@app.route("/")
def home():
    return render_template('index.html')

@app.route("/overview")
def overview():
    return render_template('overview.html')

@app.route("/sentiment")
def sentiment():
    return render_template('sentiment.html')

@app.route("/stat_analysis")
def stat_analysis():
    return render_template('stat_analysis.html')

@app.route("/classification")
def classification():
    return render_template('classification.html')

if __name__ == "__main__":
    application.run()
