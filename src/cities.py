from flask import json, Response, request, Blueprint
import psycopg2 as psycopg2

cities = Blueprint("cities", __name__)

db_host = 'postgresql'
db_port = '5432'


@cities.route("/api/cities", methods=["GET", "POST"])
def get_post_requests():
    connection = psycopg2.connect(
        host=db_host,
        port=int(db_port),
        database="SPRC",
        user="postgres",
        password="postgres123")
    cursor = connection.cursor()
    if request.method == "GET":
        cursor.execute("SELECT * FROM Orase;")
        fields = {'id': int, 'idTara': int, 'nume': str, 'lat': float, 'lon': float}
        res = [{list(fields.keys())[i]: record[i] for i in range(len(list(fields.keys())))} for record in
               cursor.fetchall()]
        return Response(status=200,
                        response=json.dumps(res),
                        mimetype='application/json')
    else:
        data = request.get_json()
        if len(data.keys()) != 4:
            return Response(status=400)
        idTara = data["idTara"]
        nume = data["nume"]
        lat = data["lat"]
        lon = data["lon"]
        if idTara == "" or idTara is None or nume == "" or nume is None or lat == "" or lat is None or lon == "" or lon is None:
            return Response(status=400)
        try:
            query = "INSERT INTO Orase (idTara, nume, lat, lon) VALUES (" + str(idTara) + ", '" + nume + "'," + str(lat) + "," + str(lon) + ");"
            cursor.execute(query)
            connection.commit()
        except:
            return Response(status=409)

        cursor.execute("SELECT MAX(id) FROM Orase;")
        return Response(
            status=201,
            response=json.dumps({'id': cursor.fetchone()[0]}),
            mimetype='application/json'
        )


@cities.route("/api/cities/<id_req>", methods=["PUT", "DELETE"])
def del_put_requests(id_req):
    connection = psycopg2.connect(
        host=db_host,
        port=int(db_port),
        database="SPRC",
        user="postgres",
        password="postgres123")
    cursor = connection.cursor()
    if request.method == "DELETE":
        try:
            cursor.execute("DELETE FROM Orase WHERE id = " + id_req + ";")
            if not cursor.rowcount:
                return Response(status=404)
        except:
            return Response(status=400)
        connection.commit()
        return Response(status=200)

    else:
        data = request.get_json()
        if len(data.keys()) != 5:
            return Response(status=400)
        id = data["id"]
        idTara = data["idTara"]
        nume = data["nume"]
        lat = data["lat"]
        lon = data["lon"]
        if id == "" or id is None or idTara == "" or idTara is None or nume == "" or nume is None or lat == "" or lat is None or lon == "" or lon is None:
            return Response(status=400)
        try:
            cursor.execute(
                "UPDATE Orase SET id = " + id + ", idTara = " + str(idTara) + ", nume = '" + nume + "', lat = " + str(lat) + ", lon = " + str(lon) + " WHERE id = " + id_req + ";")
            if not cursor.rowcount:
                return Response(status=404)
        except:
            return Response(status=400)
        connection.commit()
        return Response(status=200)


@cities.route("/api/cities/country/<id_req>", methods=["GET"])
def get_requests_id(id_req):
    connection = psycopg2.connect(
        host=db_host,
        port=int(db_port),
        database="SPRC",
        user="postgres",
        password="postgres123")
    cursor = connection.cursor()
    try:
        cursor.execute(
            "SELECT * FROM Orase WHERE idTara = " + id_req + ";")
        if not cursor.rowcount:
            return Response(status=404)
    except:
        return Response(status=400)
    connection.commit()
    fields = {'id': int, 'idTara': int, 'nume': str, 'lat': float, 'lon': float}
    res = [{list(fields.keys())[i]: record[i] for i in range(len(list(fields.keys())))} for record in cursor.fetchall()]
    return Response(status=200,
                    response=json.dumps(res))
