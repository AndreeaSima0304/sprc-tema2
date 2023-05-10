from flask import json, Response, request, Blueprint
import psycopg2 as psycopg2

countries = Blueprint("countries", __name__)

db_host = 'postgresql'
db_port = '5432'


@countries.route("/api/countries", methods=["GET", "POST"])
def get_post_requests():
    connection = psycopg2.connect(
        host=db_host,
        port=int(db_port),
        database="SPRC",
        user="postgres",
        password="postgres123")
    cursor = connection.cursor()
    if request.method == "GET":
        cursor.execute("SELECT * FROM Tari;")
        fields = {'id': int, 'nume': str, 'lat': float, 'lon': float}
        res = [{list(fields.keys())[i]: record[i] for i in range(len(list(fields.keys())))} for record in cursor.fetchall()]
        return Response(status=200,
                        response=json.dumps(res),
                        mimetype='application/json')
    else:
        data = request.get_json()
        if len(data.keys()) != 3:
            return Response(status=400)
        nume = data["nume"]
        lat = data["lat"]
        lon = data["lon"]
        if nume == "" or nume is None or lat == "" or lat is None or lon == "" or lon is None:
            return Response(status=400)
        try:
            query = "INSERT INTO Tari (nume, lat, lon) VALUES ('" + nume + "'," + str(lat) + "," + str(lon) + ");"

            cursor.execute(query)
            connection.commit()
        except:
            return Response(status=409)

        cursor.execute("SELECT MAX(id) FROM Tari;")
        return Response(
            status=201,
            response=json.dumps({'id': cursor.fetchone()[0]}),
            mimetype='application/json'
        )


@countries.route("/api/countries/<id_req>", methods=["DELETE", "PUT"])
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
            cursor.execute("DELETE FROM Tari WHERE id = " + id_req + ";")
            if not cursor.rowcount:
                return Response(status=404)
        except:
            return Response(status=400)
        connection.commit()
        return Response(status=200)

    else:
        data = request.get_json()
        if len(data.keys()) != 4:
            return Response(status=400)
        id = data["id"]
        nume = data["nume"]
        lat = data["lat"]
        lon = data["lon"]
        if nume == "" or nume is None or lat == "" or lat is None or lon == "" or lon is None:
            return Response(status=400)
        try:
            cursor.execute("UPDATE Tari SET id = " + id + ", nume = '" + nume + "', lat = " + str(lat) + ", lon = " + str(lon) + " WHERE id = " + id_req + ";")
            if not cursor.rowcount:
                return Response(status=404)
        except:
            return Response(status=400)
        connection.commit()
        return Response(status=200)
