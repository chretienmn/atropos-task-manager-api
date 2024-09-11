import boto3
import json
import logging
import threading
import time
from falcon import HTTPNotFound
from moto import mock_glue, mock_s3


# Use moto decorators to mock Glue and S3 globally for the class
# since we do not have access to a real AWS account
@mock_glue
@mock_s3
class GlueJob:
    def __init__(self):
        # Initialize clients for Glue and S3
        self.glue_client = boto3.client('glue')
        self.s3_client = boto3.client('s3')
        self.job_name = "evidence"
        self.bucket_name = "evidences"
        self.result_prefix = "results/"
        self.sample_task_id = "777c4f13-38ec-4d38-8036-06cb42b2e1a3"
        self.sample_evidence_file = "sample-evidence.json"
        # Track job runs locally since the `moto` library does not
        # support yet the `self.glue_client.get_job_runs` method yet
        self.job_runs = {}

        # Setup mock environment
        self.setup_mock_environment()

    def setup_mock_environment(self):
        """
        Setup mock AWS Glue jobs and S3 bucket using moto.
        This method will initialize mocked Glue jobs and a mock S3 bucket
        for local testing.
        """
        # Mocking Glue job
        self.glue_client.create_job(
            Name=self.job_name,
            Role="arn:aws:iam::123456789012:role/AWSGlueServiceRole",
            Command={
                "Name": "FHIR-evidence",
                "ScriptLocation": "s3://scripts/generate-evidence.py"
            }
        )

        # Mocking S3 bucket
        self.s3_client.create_bucket(Bucket=self.bucket_name)
        # Add a sample result file for a completed task
        with open(self.sample_evidence_file, 'r') as evidence_file:
            evidence_data = json.load(evidence_file)
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=f"{self.result_prefix}{self.sample_task_id}.json",
                Body=json.dumps(evidence_data)
            )

    def start(self, job_name, task_id):
        """
        Start a Glue job with the task_id passed as an argument.
        This method is mocked for local testing using moto.
        """
        response = self.glue_client.start_job_run(
            JobName=job_name,
            Arguments={'--task_id': task_id}
        )
        job_run_id = response['JobRunId']

        # Mock the job state as 'RUNNING' when starting
        self.job_runs[job_run_id] = {
            'JobRunState': 'RUNNING',
            'Arguments': {'--task_id': task_id}
        }
        # Simulate job finishing after a delay (mocked as thread here)
        thread = threading.Thread(target=self._change_jobs_state)
        thread.start()

        return job_run_id

    def _change_jobs_state(self, seconds=10):
        """
        Changes the 'JobRunState' of all jobs after specified seconds.
        """
        time.sleep(seconds)
        for job in self.job_runs.values():
            job['JobRunState'] = "SUCCEEDED"

    def get_status(self, task_id):
        """
        Get the status of the Glue job using the task_id.
        This method is mocked for local testing using moto.
        """
        # Retrieve mocked job runs locally since the `moto` library does not
        # support yet the `self.glue_client.get_job_runs` method yet.
        # A real-world scenario looks like:
        # response = self.glue_client.get_job_runs(JobName=self.job_name)
        # for job in response['JobRuns']:
        #     if job['Arguments'].get('--task_id') == task_id:
        #         return job['JobRunState']
        for job in self.job_runs.values():
            if job['Arguments'].get('--task_id') == task_id:
                return job['JobRunState']
        return 'NOT_FOUND'

    def get_result(self, task_id):
        """
        Retrieve the result from S3 for a completed Glue job.
        This method is mocked for local testing using moto.
        """
        # To mock a job result from S3, we're using the task ID of the
        # mock environment. In a real scenario, delete the line below
        task_id = self.sample_task_id
        result_key = f"{self.result_prefix}{task_id}.json"
        try:
            obj = self.s3_client.get_object(
                Bucket=self.bucket_name,
                Key=result_key
            )
            result_data = obj['Body'].read().decode('utf-8')
        except self.s3_client.exceptions.NoSuchKey:
            logging.info("GlueJob.get_result: Result not available yet")
            raise HTTPNotFound(
                description="Result not available yet", code="E9000")

        return json.loads(result_data)
