import falcon
import json
from resources import TaskResource, specs


class CORSMiddleware:
    def process_request(self, req, resp):
        resp.set_header('Access-Control-Allow-Origin', '*')
        resp.set_header('Access-Control-Allow-Methods', '*')
        resp.set_header('Access-Control-Allow-Headers', '*')
        resp.set_header('Access-Control-Max-Age', 1728000)  # 20 days
        if req.method == 'OPTIONS':
            raise falcon.http_status.HTTPStatus(falcon.HTTP_200, body='\n')


def app():
    # Initiate API
    out = falcon.App(middleware=[CORSMiddleware()])

    # Task resource
    task_resource = TaskResource()
    # Routes for RESTful API
    out.add_route('/tasks', task_resource)
    out.add_route('/tasks/{task_id}/result', task_resource, suffix="result")
    out.add_route('/tasks/{task_id}/status', task_resource, suffix="status")

    # Save Open API specifications
    specs.register(out)
    with open('openapi.json', 'w') as outfile:
        json.dump(specs.spec, outfile, indent=4)

    return out


# Initate API
api = app()
