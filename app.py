from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from model import point, road
from settings import *
import googlemaps

API_KEY = 'key'
client = googlemaps.Client(key=API_KEY)

def get_distance(cord1, cord2):
    distance = client.distance_matrix(cord1, cord2)
    try:
        return distance['rows'][0]['elements'][0]['distance']['value']
    except:
        return None

@app.route('/', methods=['POST', 'GET'])
def index():
    query = point.query.filter(point.isDeleted == 0).all()
    # if request.method == 'POST' and form.validate():
        # query = point(form.coordinates.data)
        # db.session.add(query)
        # db.session.commit()
    #     points = set()
    #     roads = []
    #     tour = []
    #     arr = form.coordinates.data.split('\n')
    #     for i in range(len(arr)):
    #         arr[i] = arr[i].replace('\r', '')
    #         points.add(point(i, arr[i]))
    #     for origin in points:
    #         for destination in points:
    #             if origin != destination:
    #                 print(get_distance(origin.cord, destination.cord), origin.cord, destination.cord)
    return render_template('index.html', query=query)

@app.route('/add', methods=['POST'])
def add():
    if request.method == 'POST' and request.form.get('name') and request.form.get('coordinates'):
        p = point(request.form.get('coordinates'), request.form.get('name'))
        db.session.add(p)
        db.session.commit()
        return str(p.id)
    return 'Failed to add'

@app.route('/delete', methods=['POST'])
def delete():
    if request.method == 'POST' and request.form.get('id'):
        p = point.query.get(request.form.get('id'))
        p.isDeleted = 1
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
    start = first(points)
    tour = [start]
    unvisited = set(points - {start})
    while unvisited:
        c = nearest_neighbour(tour[-1], unvisited, roads)
        tour.append(c)
        unvisited.remove(c)
    return tour

@app.route('/nn_algorithm', methods=['GET'])
def nn_algorithm():
    pnt = set()
    points_list = point.query.filter(point.isDeleted == 0).all()
    for i in points_list:
        pnt.add(i)
    tour = nn_tour(pnt, roads=every_road(pnt))
    return '[' + ', '.join(["'" + i.name + "'" for i in tour]) +']'



if __name__ == '__main__':
    app.run(debug=True)