import http.server
import socketserver

# A simple script to use the python CGI server in python3
# Using CGIHTTPRequestHandler in place of SimpleHTTPRequestHandler
# allows python scripts to be called as an action (POST)

# define the handler to be the CGI server
handler = http.server.CGIHTTPRequestHandler

# point the handler to a directory with scripts
handler.cgi_directories = ["/cgi-scripts"]

# define the server using the handler
PORT = int(input("Specify port: ") or 8000)
httpd = socketserver.TCPServer(("0.0.0.0", PORT), handler)

# Set variables which the CGIHTTPRequestHandler expects
httpd.server_name = "myServer"
httpd.server_port = PORT

print("staring CGI server...")

## simple demo script for showing how to connect to an sqlite DB 
# from Python, and run a simple SQL query 

# import the python library for SQLite 
import sqlite3

# connect to the database file, and create a connection object
db_connection = sqlite3.connect('restaurants.db')

# create a database cursor object, which allows us to perform SQL on the database. 
db_cursor = db_connection.cursor()

n_id = int(input("Which neighborhood? "))

# run a first query 
db_cursor.execute(f"""
	SELECT r.name
	FROM restaurants as r
	WHERE r.neighborhood_id = {n_id}""")

# store the result in a local variable. 
# this will be a list of tuples, where each tuple represents a row in the table
list_restaurants = db_cursor.fetchall()

db_cursor.execute(f"""SELECT name FROM neighborhoods WHERE id='{n_id}'""")
n_name = db_cursor.fetchone()[0]

print("list_restaurants contents:")
print(list_restaurants)
print(str(n_name))

db_connection.close()

html_list = ""
for restaurant in list_restaurants:
	html_list += f"""
		<li>
		{restaurant[0]}
		</li>
	"""

f_html = open("index.html", "w")
f_html.write(f"""<!DOCTYPE html>
<html>
<head>
	<title>Restaurants</title>
</head>
<body>
	<div id="main">
		<h1>Restaurants in {n_name}</h1>
		<ul>
			{html_list}
		</ul>
	</div>
</body>
</html>""")
f_html.close()

# run the server. To kill it, issue Ctrl + C
httpd.serve_forever()