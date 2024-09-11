import falcon.testing
import json
from app import api
from services import GlueJob


class TestTaskAPI(falcon.testing.TestCase):
    def setUp(self):
        # Set up the Falcon API for testing
        super().setUp()
        self.app = api
        self.glue_job = GlueJob()

    def test_create_task_unknown_job(self):
        # Test the POST /tasks endpoint to create a task
        request = {"job_name": "test-job"}
        response = self.simulate_post('/tasks', json=request)
        # Assert the response status
        self.assertEqual(response.status_code, 422)

    def test_create_task_known_job(self):
        # Test the POST /tasks endpoint to create a task
        request = {"job_name": "evidence"}
        response = self.simulate_post('/tasks', json=request)
        TestTaskAPI.known_task_id = response.json['task_id']
        # Assert the response status and response format
        self.assertEqual(response.status_code, 201)
        self.assertIn("task_id", response.json)
        self.assertIn("job_run_id", response.json)

    def test_get_task_status_unknown_id(self):
        task_id = "unknown-task-id"
        # Test the GET /tasks/{task_id}/status endpoint
        response = self.simulate_get(f"/tasks/{task_id}/status")
        # Assert the response status and response format
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], "NOT_FOUND")
        self.assertEqual(response.json['task_id'], task_id)

    def test_get_task_status_known_id(self):
        # Test the GET /tasks/{task_id}/status endpoint
        response = self.simulate_get(f"/tasks/{self.known_task_id}/status")
        # Assert the response status and response format
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], "RUNNING")
        self.assertEqual(response.json['task_id'], self.known_task_id)

    def test_get_task_result(self):
        task_id = "test-task-id"
        # Test the GET /tasks/{task_id}/result endpoint
        response = self.simulate_get(f"/tasks/{task_id}/result")
        # Assert the response status and response format
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['task_id'], task_id)
        with open('sample-evidence.json', 'r') as evidence_file:
            evidence_data = json.load(evidence_file)
            self.assertEqual(response.json['result'], evidence_data)
