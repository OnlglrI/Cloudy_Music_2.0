from celery import shared_task
import subprocess

@shared_task
def run_extract():
    subprocess.run(["python", "-m", "ETL.extract"], cwd="/app")

@shared_task
def run_analytics():
    subprocess.run(["python", "-m", "ETL.analytics"], cwd="/app")
