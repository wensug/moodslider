from http.server import SimpleHTTPRequestHandler, HTTPServer
import xml.etree.ElementTree as ET
import sqlite3
import json
#some of the libraries used like http.server, sqlite3 are not suitable for production but due to the time and simplicity of the project, I decided to use them. 

PORT = 8080
PROGRAMMES_TABLE = 'programmes'

class S(SimpleHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        print("GET")
        return SimpleHTTPRequestHandler.do_GET(self)


    def do_POST(self):
        if self.path == '/upload':
            # Because the form from HTTP sending the WebKitFormBoundary, we need to stip the response in order to get the xml file
            line = ""
            xml = ""
            while "<?xml" not in line:
                line = self.rfile.readline().decode('utf-8')
                if "<?xml" in line:
                    xml += line
                    break
            line = self.rfile.readline().decode('utf-8')
            while 'WebKitFormBoundary' not in line:
                xml += line
                line = self.rfile.readline().decode('utf-8')
            process_xml(xml)
            self._set_response()
            self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))

        elif self.path == '/recommendations':
            print("POST - recommendations")
            content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
            post_body = self.rfile.read(content_length).decode('utf-8')
            programmes = fetch_recommendations(post_body.split('=')[1].split(','))
            self._set_response()
            self.wfile.write(json.dumps(programmes).encode('utf-8'))
        return



def init_db():
    conn = sqlite3.connect(':memory:')
    c = conn.cursor()
    c.execute("CREATE TABLE {table_name} (name text, img_path text, mood text)".format(table_name=PROGRAMMES_TABLE))
    conn.commit()
    c.close()
    return conn


def process_xml(xml):
    p = ET.XMLParser(encoding='utf-8')
    root = ET.fromstring(xml, parser=p)
    cursor = DB_CON.cursor()
    for programme in root.iter('programme'):
        name = programme.find('name').text
        mood = programme.find('mood').text
        image_path = programme.find('image_path').text
        cursor.execute("""INSERT INTO {table_name} VALUES ('{name}', '{image_path}', '{mood}')""".format(table_name=PROGRAMMES_TABLE,name=name, image_path=image_path, mood=mood))
    DB_CON.commit()
    cursor.close()
    return


def fetch_recommendations(moods):
    cursor = DB_CON.cursor()
    cursor.execute(
        """
        SELECT name, img_path
        FROM {table_name}
        WHERE mood IN ('{moods}')
        LIMIT 5
        """.format(table_name=PROGRAMMES_TABLE, moods="','".join(moods)))
    rows = cursor.fetchall()
    return rows



DB_CON = init_db()
try:
    server = HTTPServer(('', PORT), S)
    print("serving at port", PORT)
    server.serve_forever()
except Exception:
    DB_CON.close()