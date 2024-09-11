import json
import unittest
from services import GlueJob


class TestGlueJob(unittest.TestCase):
    def setUp(self):
        self.glue_job = GlueJob()

    def test_start_job(self):
        # Test starting a Glue job
        task_id = "test-task-id"
        job_run_id = self.glue_job.start(self.glue_job.job_name, task_id)
        self.assertIsNotNone(job_run_id)

    def test_get_job_status(self):
        # Test retrieving Glue job status
        task_id = "test-task-id"
        status = self.glue_job.get_status(task_id)
        self.assertEqual(status, 'NOT_FOUND')

    def test_get_task_result(self):
        # Test retrieving task result from S3
        task_id = "test-task-id"
        result = self.glue_job.get_result(task_id)
        with open('sample-evidence.json', 'r') as evidence_file:
            evidence_data = json.load(evidence_file)
            self.assertEqual(result, evidence_data)
