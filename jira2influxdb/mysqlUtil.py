#!/app/pluops/python/bin/python2.7
# -*- coding: UTF-8 -*-
import time
import sys
import requests

import MySQLdb
from jira2influxdb import jiraUtil
from influxdb import InfluxDBClient
import json

def createJiraConnection():
    return  MySQLdb.connect(host="39.104.202.48",user="admin",passwd="admin",db="",port=3306,charset="utf8")

def insertMysql2Influxdb(db, key):
    influxClient = InfluxDBClient("39.104.48.57", 8086, "admin", "admin", "Influxdb");
    cursor = db.cursor();
    data = cursor.execute("select Rls_date,it_pm,Project_id,Country,SIT_date,UAT_date,start_date, Project_Effort,"
                          " Story_ready,Rls,id,pod,project_name,projectOwner from ProjectG");
    info = cursor.fetchmany(data);
    for  Rls_date,it_pm,Project_id,Country,SIT_date,UAT_date,start_date,Story_ready,Rls,id,pod,project_name, Project_Effort,projectOwner in info:
         jiraUtil.insertTasks2Influxdb(Project_id, project_name, Project_Effort, projectOwner);
         metric =  {
            "measurement":"jira",
            "tags":{
               "project_ID": str(id)
            },
            "time": "2019-05-13T23:00:00Z",
            "fields":{
                "id": "",
             }
         }
    json2influxdb = [metric];
    influxClient.write_points(json2influxdb)
    influxClient.close();
    #call JiraUtil

db = createJiraConnection();
insertMysql2Influxdb(db,"Dashboard");

