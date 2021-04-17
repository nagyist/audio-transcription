from worker import app
import os
from io import BytesIO
from celery.utils.log import get_task_logger
import hashlib
from minio import Minio
from minio.error import NoSuchKey, BucketAlreadyExists, \
    BucketAlreadyOwnedByYou


logger = get_task_logger(__name__)


@app.task(bind=True, name='save_interim')
def save_interim(self, interim_transcript):
    write_interim(interim_transcript)


@app.task(bind=True, name='save_final')
def save_final(self, final_transcript):
    write_final(final_transcript)


def write_final(final_transcript):
    write_transcript(
        bucket=os.environ['FINAL_BUCKET'],
        transcript=final_transcript
    )
    logger.info('Wrote final transcript')


def write_interim(interim_transcript):
    write_transcript(
        bucket=os.environ['INTERIM_BUCKET'],
        transcript=interim_transcript
    )
    logger.info('Wrote interim transcript')


def write_transcript(bucket, transcript):
    minio_client = Minio(os.environ['MINIO_HOST'],
                         access_key=os.environ['MINIO_ACCESS_KEY'],
                         secret_key=os.environ['MINIO_SECRET_KEY'],
                         secure=False)
    try:
        minio_client.make_bucket(
            bucket_name=bucket,
            location='us-east-1')
    except BucketAlreadyExists:
        pass
    except BucketAlreadyOwnedByYou:
        pass

    key = hashlib.md5(transcript.encode()).hexdigest()
    try:
        st = minio_client.stat_object(bucket, key)
        update = (st.etag != key)
    except NoSuchKey as err:
        update = True
    if update:
        logger.info(f'Writing transcript as {bucket}/{key} to minio')
        stream = BytesIO(transcript.encode())
        minio_client.put_object(bucket, key, stream,
                                stream.getbuffer().nbytes)
