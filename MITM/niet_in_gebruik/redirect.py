"""
Deze code is gekopieërd van grepper. Gegenereerd door 'You (ai)'.
"""

from flask import Flask, redirect

app = Flask(__name__)

# Deze decorator vertelt Flask dat de functie redirect_link moet worden aangeroepen als iemand in de adressenbalk '/' in geeft.
@app.route('/')
def redirect_link():
    # Code 302 betekent 'Found' en wordt gebruikt voor tijdelijke omleidingen.
    return redirect('https://www.google.com', code=302)


if __name__=="__main__":
    app.run()