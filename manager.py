from sys import path as syspath
from os import getenv, path

syspath.append(path.join(getenv("HOME"), "projects/dwh_crash_management"))

import requests
from pprint import pprint

from common import send_email

connectors = [("localhost:8083", "MySQLDebezium-test-1")]
connector_status_url = "/connectors/{}/status"
task_status_url = "/connectors/{}/tasks/{}/status"
task_restart_url = "/connectors/{}/tasks/{}/restart"

try:
    for host, connector in connectors:
        url = "http://" + host + connector_status_url.format(connector)
        req = requests.get(url)
        print(url)
        if req.status_code == 200:
            response = req.json()
            print(response)
            if response.get("connector"):
                print("{} is {}".format(connector, response["connector"].get("state")))
                if response["connector"].get("state") == "RUNNING":
                    tasks = response.get("tasks", [])
                    for task in tasks:
                        pprint(task)
                        if task.get("state") == "FAILED":
                            message = "{} is failed, Attempting to restart it..".format(connector)
                            send_email("Connector Failure", message)
                            restart_url = "http://" + host + task_restart_url.format(connector, task.get("id", -1))
                            requests.post(restart_url)
                            pprint(requests.get("http://" + host + task_status_url.format(connector,
                                                                                          task.get("id", -1))).json())
except KeyboardInterrupt:
    print("Received INT signal, Stopping manager.")
except Exception as e:
    print("Caught an Exception [Caused by: {}]".format(e))

print("Manager is stopped")
