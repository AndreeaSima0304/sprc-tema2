from flask import json, Response, request, Blueprint
import psycopg2 as psycopg2

temperatures = Blueprint("temperatures", __name__)

db_host = 'postgresql'
db_port = '5432'


@temperatures.route("/api/temperatures", methods=["GET", "POST"])
def get_post_requests():
    connection = psycopg2.connect(
        host=db_host,
        port=int(db_port),
        database="SPRC",
        user="postgres",
        password="postgres123")
    cursor = connection.cursor()
    if request.method == "GET":
        lat = request.args.get('lat', type=float)
        lon = request.args.get('lon', type=float)
        from_date = request.args.get('from', default='0001-01-01', type=str)
        until_date = request.args.get('until', default='9999-12-31', type=str)

        conds = []
        if lat:
            conds.append("lat = real '" + str(lat) + "'")
        if lon:
            conds.append("lon = real '" + str(lon) + "'")

        if conds:
            cursor.execute("SELECT id, valoare, TO_CHAR(timestamp, 'YYYY-MM-DD') \
                    		FROM Temperaturi WHERE \
                    	    timestamp BETWEEN TO_DATE('" + from_date + "', 'YYYY-MM-DD') \
                    		AND TO_DATE('" + until_date + "', 'YYYY-MM-DD') \
                    		AND idOras in (SELECT id FROM Orase WHERE "\
                            + ' AND '.join(conds) + ");")
        else:
            cursor.execute("SELECT id, valoare, TO_CHAR(timestamp, 'YYYY-MM-DD') \
                    FROM Temperaturi WHERE \
                    timestamp BETWEEN TO_DATE('" + from_date + "', 'YYYY-MM-DD') \
                    AND TO_DATE('" + until_date + "', 'YYYY-MM-DD');")

        fields = {'id': int, 'valoare': float, 'timestamp': str}
        res = [{list(fields.keys())[i]: record[i] for i in range(len(list(fields.keys())))} for record in cursor.fetchall()]
        return Response(status=200,
                        response=json.dumps(res),
                        mimetype='application/json')
    else:
        data = request.get_json()
        if len(data.keys()) != 2:
            return Response(status=400)
        idOras = data["idOras"]
        val = data["valoare"]
        if idOras == "" or idOras is None or val == "" or val is None:
            return Response(status=400)
        try:
            query = "INSERT INTO Temperaturi (idOras, valoare) VALUES (" + str(idOras) + "," + str(val) + ");"
            cursor.execute(query)
            connection.commit()
        except:
            return Response(status=409)

        cursor.execute("SELECT MAX(id) FROM Temperaturi;")
        return Response(
            status=201,
            response=json.dumps({'id': cursor.fetchone()[0]}),
            mimetype='application/json')


@temperatures.route("/api/temperatures/<id_req>", methods=["DELETE", "PUT"])
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
            cursor.execute("DELETE FROM Temperaturi WHERE id = " + id_req + ";")
            if not cursor.rowcount:
                return Response(status=404)
        except:
            return Response(status=400)
        connection.commit()
        return Response(status=200)

    else:
        data = request.get_json()
        if len(data.keys()) != 3:
            return Response(status=400)
        try:
            id = data["id"]
            idOras = data["idOras"]
            val = data["valoare"]
        except:
            return Response(status=400)
        if id == "" or id is None or idOras == "" or idOras is None or val == "" or val is None:
            return Response(status=400)
        try:
            cursor.execute("UPDATE Temperaturi SET id = " + str(id) + ", idOras = " + str(idOras) + ", valoare = " + str(val) + " WHERE id = " + id_req + ";")
            if not cursor.rowcount:
                return Response(status=404)
        except:
            return Response(status=400)
        connection.commit()
        return Response(status=200)


@temperatures.route("/api/temperatures/cities/<id_req>", methods=["GET"])
def get_cities_requests(id_req):
    connection = psycopg2.connect(
        host=db_host,
        port=int(db_port),
        database="SPRC",
        user="postgres",
        password="postgres123")
    cursor = connection.cursor()
    from_date = request.args.get('from', default='0001-01-01', type=str)
    until_date = request.args.get('until', default='9999-12-31', type=str)

    cursor.execute("SELECT id, valoare, TO_CHAR(timestamp, 'YYYY-MM-DD') \
                   FROM Temperaturi WHERE idOras = " + id_req +
                   " AND timestamp BETWEEN TO_DATE('" + from_date + "', 'YYYY-MM-DD') \
                    AND TO_DATE('" + until_date + "', 'YYYY-MM-DD');")

    fields = {'id': int, 'valoare': float, 'timestamp': str}
    res = [{list(fields.keys())[i]: record[i] for i in range(len(list(fields.keys())))} for record in
           cursor.fetchall()]
    return Response(status=200,
                    response=json.dumps(res),
                    mimetype='application/json')


@temperatures.route("/api/temperatures/countries/<id_req>", methods=["GET"])
def get_countries_requests(id_req):
    connection = psycopg2.connect(
        host=db_host,
        port=int(db_port),
        database="SPRC",
        user="postgres",
        password="postgres123")
    cursor = connection.cursor()
    from_date = request.args.get('from', default='0001-01-01', type=str)
    until_date = request.args.get('until', default='9999-12-31', type=str)

    cursor.execute("SELECT id, valoare, TO_CHAR(timestamp, 'YYYY-MM-DD') FROM Temperaturi \
                    WHERE timestamp BETWEEN TO_DATE('" + from_date + "', 'YYYY-MM-DD') \
                    AND TO_DATE('" + until_date + "', 'YYYY-MM-DD') AND idOras IN \
                    (SELECT id FROM Orase WHERE idTara = " + id_req + ");")

    fields = {'id': int, 'valoare': float, 'timestamp': str}
    res = [{list(fields.keys())[i]: record[i] for i in range(len(list(fields.keys())))} for record in
           cursor.fetchall()]
    return Response(status=200,
                    response=json.dumps(res),
                    mimetype='application/json')
