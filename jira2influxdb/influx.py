from influxdb import InfluxDBClient

def connect(host, port, username, password,database):
    influxClient = InfluxDBClient(host, port, username, password,database)

