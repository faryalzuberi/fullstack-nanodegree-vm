from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
import cgitb
cgitb.enable()
# import CRUD operations
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Handler class extends from BaseHTTPRequestHandler
class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
            if self.path.endswith("/edit"):
                restaurantID = self.path.split("/")[2]
                restaurant = session.query(Restaurant).filter_by(id = restaurantID).one()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = "<html><body>"
                output += "%s<br>" % restaurant.name
                output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/edit'>" % restaurant.id
                output += "Edit<br><input name='restaurant' placeholder='%s' type='text'><br>" % restaurant.name
                output += "<input type='submit' value='Submit'></form>"
                output += "</html></body>"
                self.wfile.write(bytes(output, "utf8"))
                return
            if self.path.endswith("/delete"):
                restaurantID = self.path.split("/")[2]
                restaurant = session.query(Restaurant).filter_by(id = restaurantID).one()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = "<html><body>"
                output += "%s<br>" % restaurant.name
                output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/delete'>" % restaurant.id
                output += "Delete Restaurant %s ?<br>" % restaurant.name
                output += "<input type='submit' value='Delete'></form>"
                output += "</html></body>"
                self.wfile.write(bytes(output, "utf8"))
                return
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>Hello!"
                output += "<form method='POST' action='/hello' enctype='multipart/form-data'>"
                output += "<h2>What would you like me to say?</h2><br><input name='message' type='text'><br>"
                output += "<input type='submit' value='Submit'></form></body></html>"
                self.wfile.write(bytes(output, "utf8"))
                print(output)
                return
            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>&#161Hola!<br><a href='/hello'>Back to Hello</a>"
                output += "<form method='POST' action='/hello' enctype='multipart/form-data'>"
                output += "<h2>What would you like me to say?</h2><br><input name='message' type='text'><br>"
                output += "<input type='submit' value='Submit'></form></body></html>"
                self.wfile.write(bytes(output, "utf8"))
                print(output)
                return
            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = "<html><body>"
                output = "<a href='/restaurants/new'>Add a new Restaurant</a>"
                output += "Restaurants: <br>"
                restaurants = session.query(Restaurant).all()
                for restaurant in restaurants:
                    output += "<span> %s <span><br>" % restaurant.name
                    output += "<a href='/restaurants/%s/edit'>Edit</a><br>" % restaurant.id
                    output += "<a href='/restaurants/%s/delete'>Delete</a><br><br>" % restaurant.id
                output += "</html></body>"
                self.wfile.write(bytes(output, "utf8"))
                print(output)
                return
            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = "<html><body>"
                output += "<form method='POST' action='/restaurants/new' enctype='multipart/form-data'>"
                output += "<h2>Add a Restaurant</h2><br><input name='restaurant' placeholder='new Restaurant name' type='text'><br>"
                output += "<input type='submit' value='Submit'></form>"
                output += "</html></body>"
                self.wfile.write(bytes(output, "utf8"))
                print(output)
                return
            else:
                self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            # self.send_response(301)
            # self.send_header('Content-type', 'text/html')
            # self.end_headers()
            if self.path.endswith("restaurants/new"):
                ctype, pdict = cgi.parse_header(self.headers['content-type'])
                pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('restaurant')
                newrestaurant = Restaurant(name = "%s" % messagecontent[0])
                session.add(newrestaurant)
                session.commit()
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()
            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(self.headers['content-type'])
                pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('restaurant')
                restaurantID = self.path.split("/")[2]
                restaurant = session.query(Restaurant).filter_by(
                        id=restaurantID).one()
                restaurant.name == messagecontent[0]
                session.add(restaurant)
                session.commit()
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()
            if self.path.endswith("/delete"):
                restaurantID = self.path.split("/")[2]
                restaurant = session.query(Restaurant).filter_by(
                        id=restaurantID).one()
                session.delete(restaurant)
                session.commit()
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()
        except:
            pass
            ctype, pdict = cgi.parse_header(self.headers['content-type'])
            pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('restaurant')
            print("An error occured")

def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webserverHandler)
        server.serve_forever()
        print("Web server running on port %s" % port)

    except KeyboardInterrupt:
        print("^C entered, stopping web server...")
        server.socket.close()


if __name__ == '__main__':
    main()
