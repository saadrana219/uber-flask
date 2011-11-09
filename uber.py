from __future__ import with_statement
from contextlib import closing
import sqlite3
import json
from flask import Flask, request, g, make_response, render_template
from geopy import geocoders

DATABASE = 'uber.db'
DEBUG = True
geocoder = geocoders.Google()

app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
  return sqlite3.connect(app.config['DATABASE'])

def init_db():
  with closing(connect_db()) as db:
	  with app.open_resource('schema.sql') as f:
		  db.cursor().executescript(f.read())
		  db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/addresses', methods=['GET'])
def show_addresses():
  all_addresses = g.db.execute('select id, nickname, location, latitude, longitude from addresses').fetchall()
  entries = [dict(id=address[0], nickname=address[1], location=address[2], latitude=address[3], longitude=address[4]) for address in all_addresses]
  return json.dumps(entries)
	
@app.route('/addresses', methods=['POST'])
def create_address():
	try:
	  place, (lat, lng) = geocoder.geocode(request.json['location'])
	  address = g.db.execute('insert into addresses (nickname, location, latitude, longitude) values (?, ?, ?, ?)', [request.json['nickname'], request.json['location'], lat, lng])
	  g.db.commit()
	  response = make_response(json.dumps(dict(nickname=request.json['nickname'], location=request.json['location'], latitude=lat, longitude=lng)))
	  response.status_code = 201
	  return response
	except ValueError:
		response = make_response(json.dumps(dict(error='Uh oh, couldn\'t geocode that location.')))
		response.status_code = 500
		return response

@app.route('/addresses/<address_id>')
def show_address(address_id):
  address = g.db.execute("select nickname, location, latitude, longitude from addresses where id = ?", [str(address_id)]).fetchone()
  return json.dumps(dict(nickname=address[0], location=address[1], latitude=address[2], longitude=address[3]))

@app.route('/addresses/<int:address_id>', methods=['PUT'])
def edit_address(address_id):
	try:
		place, (lat, lng) = geocoder.geocode(request.json['location'])
		g.db.execute('update addresses set nickname = ?, location = ?, latitude = ?, longitude = ? where id = ?', [request.json['nickname'], request.json['location'], lat, lng, str(address_id)])
		g.db.commit()
		address = g.db.execute("select nickname, location, latitude, longitude from addresses where id = ?", [str(address_id)]).fetchone()
		return json.dumps(dict(nickname=address[0], location=address[1], latitude=address[2], longitude=address[3]))
	except ValueError:
		response = make_response(json.dumps(dict(error='Uh oh, couldn\'t geocode that address.')))
		response.status_code = 500
		return response

@app.route('/addresses/<int:address_id>', methods=['DELETE'])
def delete_address(address_id):
  address = g.db.execute('select nickname, location, latitude, longitude from addresses where id = ?', [str(address_id)]).fetchone()
  g.db.execute('delete from addresses where id = ?', [str(address_id)])
  g.db.commit()
  return json.dumps(dict(nickname=address[0], location=address[1], latitude=address[2], longitude=address[3]))

if __name__ == '__main__':
	app.run()