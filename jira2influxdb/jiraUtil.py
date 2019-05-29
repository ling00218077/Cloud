from jira import JIRA
import requests
import random
import time

from influxdb import InfluxDBClient

def createJiraConnection(url,user,password):
        jira = JIRA(
            {
                'server':url,
                'verify':False
            },
            basic_auth = (user,password)
        )
        return jira

def insertIssues2Influxdb2(jira, projectId, project_name, Project_Effort, projectOwner):

    influxClient = InfluxDBClient("39.104.48.57", 8086, "admin", "admin", "Influxdb")
    jiraIssues = jira.search_issues('project={0} and created  <= endOfYear()  and createdDate >= startOfYear() '.format(projectId),
                                    startAt=0, maxResults=None);
    times = time.time();
    for issue in jiraIssues:
        if issue.fields.issuetype == "TestCase" :
             metric =  {
                "measurement":"jira",
                "tags":{
                    "project_ID": str(projectId),
                    "story_id": str(issue.fields.id),
                    "status": str(issue.fields.status),
                    "testcase_name": str(issue.fields.id),
                    "Owner":str(issue.fields.assignee),
                    "effort" : Project_Effort
                 },
                "time": times,
                "fields":{
                    "project": str("TestCaseF")
                }
               }
        elif  type == "Task":
            metric =  {
                "measurement":"jira",
                "tags":{
                "status": str(issue.fields.status),
                "project_ID": str(projectId),
                "it_pm" : str(projectOwner),
                "Task_Name": str(issue.fields["category "]),
                "Task_Owner":str(issue.fields.assignee),
                "effort": random.random() * 10,
                "Project_Effort" : Project_Effort,
                "Task_ID": str(issue.fields.id),
                "pod" : "POD Libra"
            },
                "time": times,
                "fields":{
                    "project": str("Task6")
                }
            }
        elif type == "Bug":
            metric =  {
                "measurement":"jira",
                "tags":{
                "project_ID": str(projectId),
                "classification" : "SIT",
                "status1": "1",
                "defect_name": str(issue.fields["category "]),
                "owner":str(issue.fields.assignee),
                "status": str(issue.fields.status),
                "pod" : "POD Libra"
                },
                "time": times,
                "fields":{
                    "project": str("IssueB")
                }
            }

    json2influxdb = [metric];
    influxClient.write_points(json2influxdb);
    influxClient.close();

def insertTasks2Influxdb(projectId, project_name, Project_Effort, projectOwner ):
    jira = createJiraConnection("http://39.104.48.57:8080","lingji",'Ling00218077')
    insertIssues2Influxdb2(jira, projectId, project_name, Project_Effort, projectOwner);
    jira.close();
