
from django.http import HttpResponse
from django.shortcuts import render
import requests
import json
from decouple import config

bearer = config('bearer')
workspace_gid = config('workspace_gid')
project_gid = config('project_gid')

due_at = "2019-09-15T02:06:58.147Z"
notes = "something"
start_on = "2019-09-14"


def todo(request):
    mytask = request.POST.get('task','')
  
    params = adhtml(request,mytask)    
    return render(request, 'todo.html', params)

def adhtml(request, mytask):
    url = f"https://app.asana.com/api/1.0/projects/{project_gid}/tasks"

    payload={}
    headers = {
    'Authorization': bearer,
    'Cookie': 'TooBusyRedirectCount=0; logged_out_uuid=355d1506d40d22897a60a73d8eace838; xsrf_token=dce4a512840171893ba48490296c63db%3A1645887792232'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    data = response.json()['data']
    tasklist = [x['name'] for x in data]

    if mytask != "":
        if mytask not in tasklist:
            url = "https://app.asana.com/api/1.0/tasks"

            payload = json.dumps({
            "data": {
                "completed": False,
                "due_at": due_at,
                "name": mytask,
                "notes": notes,
                "projects": [
                    project_gid
                ],
                "resource_subtype": "default_task",
                "start_on": start_on,
                "workspace": workspace_gid
            }
            })
            headers = {
            'Authorization': bearer,
            'Content-Type': 'application/json',
            'Cookie': 'TooBusyRedirectCount=0; logged_out_uuid=355d1506d40d22897a60a73d8eace838; xsrf_token=dce4a512840171893ba48490296c63db%3A1645887792232'
            }

            response = requests.request("POST", url, headers=headers, data=payload)
            print(response.text)
            tasklist.append(mytask)


    taskdict = {}
    for tindex, tasks in enumerate(tasklist):
            taskdict[tindex] = tasks
            
    params = {'taskdict': taskdict}
    return params