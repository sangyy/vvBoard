from xugu import read_value
import logging
import logging.handlers
import datetime
import sqlite3


app = Flask(__name__)


@app.route("/save")
def main_handler():
     now = datetime.datetime.now()
     str_now = now.strftime("%Y-%m-%d %H:%M:%S")
     log = logging.getLogger("xugu")
     log.setLevel(logging.DEBUG)
     handler = logging.handlers.RotatingFileHandler("example.txt", maxBytes=1024,
                                                    backupCount=1)
     handler.setLevel(logging.DEBUG)
     log.addHandler(handler)
     log.debug(str_now)
     conn = sqlite3.connect('example.db')
     c = conn.cursor()
     c.execute('''CREATE TABLE IF NOT EXISTS access_log
                  (date TEXT)''')
     c.execute(
          "INSERT INTO access_log VALUES ('%s')" % str_now)
     conn.commit()
     conn.close()
     return 'accept!'

@app.route("/query")
def query_handler():
     conn = sqlite3.connect('example.db')
     c = conn.cursor()
     c.execute("SELECT count(*) from access_log")
     data = c.fetchall()
     count = data[0][0]
     return "recv: %s" % count

@app.route("/read_adc/<pin>")
def read_adc(pin):
     data = read_value(pin)
     return data

app.run("0.0.0.0", port=5000)
