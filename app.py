from flask import Flask, render_template, request
from datetime import datetime
import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import csv

# Email konfiguracija
EMAIL_USER = "djolepavlov12@gmail.com"        # tvoj email
EMAIL_PASS = "iqezenibpdujrkei"   # lozinka ili App Password
EMAIL_TO = "djolepavlov12@gmail.com"          # gde želiš da stižu rezervacije

# Funkcija za slanje email-a
def posalji_email(ime, telefon, datum, vreme, sada):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_USER
    msg['To'] = EMAIL_TO
    msg['Subject'] = f"Nova rezervacija od {ime}"

    body = f"""
    Nova rezervacija:
    Ime: {ime}
    Telefon: {telefon}
    Datum rezervacije: {datum} u {vreme}
    Kreirano: {sada}
    """
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)
        server.quit()
        print("Email poslat!")
    except Exception as e:
        print("Greška pri slanju email-a:", e)


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/rezervacije', methods=['GET', 'POST'])
def rezervacije():
    if request.method == 'POST':
        ime = request.form['ime']
        telefon = request.form['telefon']
        datum = request.form['datum']
        vreme = request.form['vreme']
        sada = datetime.now().strftime("%d.%m.%Y %H:%M")  # datum kada je rezervisano

        # Čuvanje u CSV fajl
        with open("rezervacije.csv", "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([sada, ime, telefon, datum, vreme])

        return render_template("potvrda.html", ime=ime, datum=datum, vreme=vreme, sada=sada)

    # Prikaz forme za rezervacije + prikaz prethodnih rezervacija
    rezervacije_lista = []
    try:
        with open("rezervacije.csv", "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            rezervacije_lista = list(reader)
    except FileNotFoundError:
        pass

    return render_template('rezervacije.html', rezervacije=rezervacije_lista)

if __name__ == '__main__':
    app.run(debug=True)
