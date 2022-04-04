from airflow.hooks.S3_hook import S3Hook

def upload_to_s3(s3_conn_id, s3_key, s3_bucket, file_path, replace=False):
    s3_hook = S3Hook(s3_conn_id)
    s3_hook.load_file(
        filename=file_path,
        key=s3_key,
        bucket_name=s3_bucket,
        replace=replace)

def download_from_s3(s3_conn_id, s3_key, s3_bucket, local_path=None):
    hook = S3Hook(s3_conn_id)
    file_name = hook.download_file(
        key=s3_key, 
        bucket_name=s3_bucket, 
        local_path=local_path)
    return file_name

