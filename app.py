from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from model import point, road
from settings import *
import googlemaps

API_KEY = ''
client = googlemaps.Client(key=API_KEY)

def get_distance(cord1, cord2):
    distance = client.distance_matrix(cord1, cord2)
    try:
        return distance['rows'][0]['elements'][0]['distance']['value']
    except:
        return None

@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add():
    if request.method == 'POST' and request.form.get('name') and request.form.get('coordinates'):
        p = point(request.form.get('coordinates'), request.form.get('name'))
        db.session.add(p)
        db.session.commit()
        return str(p.id)
    return 'Failed to add'

@app.route('/delete', methods=['DELETE'])
def delete():
    if request.method == 'DELETE' and request.form.get('id'):
        p = point.query.get(request.form.get('id'))
        db.session.delete(p)
        db.session.commit()
        return ''
    return 'Failed to delete'

def every_road(points):
    roads_list = []
    for p in points:
        for destination in points:
            if p != destination:
                roads_list.append(road(p.id, destination.id, get_distance(p.cord, destination.cord,)))
    return roads_list

def distance(a, x, roads):
    for r in roads:
        if r.origin == a.id and r.destination == x.id:
            return r.distance

def nearest_neighbour(a, points, roads):
    return min(points, key=lambda x: distance(a, x, roads))

def first(points):
    return next(iter(points))

def nn_tour(points, roads):
    start = points[0]
    tour = [start]
    unvisited = set(set(points) - {start})
    while unvisited:
        c = nearest_neighbour(tour[-1], unvisited, roads)
        tour.append(c)
        unvisited.remove(c)
    return tour

@app.route('/nn_algorithm', methods=['GET'])
def nn_algorithm():
    pnt = []
    points_list = point.query.all()
    for i in points_list:
        pnt.append(i)
    try:
        tour = nn_tour(points=pnt, roads=every_road(pnt))
    except:
        return 'Failed'
    return '[' + ', '.join(['"' + i.name + '"' for i in tour]) +']'

@app.route('/listing')
def listing():
    query = point.query.all()
    txt = str([[i.id, i.name, i.cord] for i in query])
    return txt.replace("'", '"')

if __name__ == '__main__':
    app.run(debug=True)