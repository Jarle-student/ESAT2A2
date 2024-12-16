from flask import Flask, redirect

app = Flask(__name__)

# This decorator tells Flask to call the redirect_link function when someone enters '/' in the address bar.
@app.route('/')
def redirect_link():
    # Code 302 means 'Found' and is used for temporary redirects.
    return redirect('https://www.google.com', code=302)


if __name__=="__main__":
    app.run()
