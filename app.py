from flask import Flask, render_template, request, flash, redirect,url_for
import requests
import os

app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY")

@app.route('/', methods=['GET','POST'])
def weatherApp():
    if request.method == 'POST':
        cityName = request.form.get('cityname')
        api = os.getenv("OPENWEATHER_API_KEY")
        url = f"https://api.openweathermap.org/data/2.5/weather?q={cityName}&appid={api}"
        if not cityName:
            flash('Please Enter the City Name...')
            return redirect('/')
        else:
            try:
                resp = requests.get(url)
                data = resp.json()
                if resp.status_code == 200:
                    return render_template(
                        'index.html',
                        dataProvided=True,
                        temp=data['main']['temp']-273.15,
                        fl=data['main']['feels_like']-273.15,
                        visibility=data['visibility'],
                        windspeed=data['wind']['speed'],
                        country=data['sys']['country']
                    )
                else:
                    if resp.status_code == 404:
                        flash(f'Error Code {resp.status_code}. City Not Found!')
                        return redirect('/')
                    else:
                        flash(f'Error Code {resp.status_code}.')
                        return redirect('/')
            except Exception as e:
                flash(f'Error {e} occured. Please Try Again Later')
                return redirect('/')
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)