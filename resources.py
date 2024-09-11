import falcon
import logging
import uuid
from services import GlueJob
from schemas import CreateTaskRequest, CreateTaskResponse, \
    TaskStatusResponse, TaskResultResponse
from spectree import Response, SpecTree

specs = SpecTree(
    "falcon",
    title="Atropos Task Manager API",
    annotations=True
)


class TaskResource:
    def __init__(self):
        self.glue_job = GlueJob()

    @specs.validate(
        json=CreateTaskRequest,
        resp=Response(HTTP_201=CreateTaskResponse),
        tags=['Task Management']
    )
    def on_post(self, req, resp):
        """
        Create a new task (i.e., start a Glue job).
        """
        body = req.media
        task_id = str(uuid.uuid4())
        job_name = body['job_name']

        # Start the AWS Glue job
        try:
            job_run_id = self.glue_job.start(job_name, task_id)
            result = CreateTaskResponse(task_id=task_id, job_run_id=job_run_id)
        except Exception as e:
            logging.error("TaskResource.on_post: %s", e)
            raise falcon.HTTPInternalServerError(
                description=str(e.args), code="E9001")

        resp.status = falcon.HTTP_201
        resp.media = result.dict()

    @specs.validate(
        resp=Response(HTTP_200=TaskResultResponse),
        tags=['Task Management']
    )
    def on_get_result(self, req, resp, task_id):
        """
        Get the task result.
        """
        # Retrieve the result from S3 (if completed)
        try:
            result_data = self.glue_job.get_result(task_id)
            result = TaskResultResponse(task_id=task_id, result=result_data)
        except Exception as e:
            if isinstance(e, falcon.HTTPNotFound):
                raise e
            logging.error("TaskResource.on_get_result: %s", e)
            raise falcon.HTTPInternalServerError(
                description=str(e.args), code="E9002")

        resp.status = falcon.HTTP_200
        resp.media = result.dict()

    @specs.validate(
        resp=Response(HTTP_200=TaskStatusResponse),
        tags=['Task Management']
    )
    def on_get_status(self, req, resp, task_id):
        """
        Get the task status.
        """
        # Check Glue job status
        try:
            status = self.glue_job.get_status(task_id)
            result = TaskStatusResponse(task_id=task_id, status=status)
        except Exception as e:
            logging.error("TaskResource.on_get_status: %s", e)
            raise falcon.HTTPInternalServerError(
                description=str(e.args), code="E9003")

        resp.status = falcon.HTTP_200
        resp.media = result.dict()
