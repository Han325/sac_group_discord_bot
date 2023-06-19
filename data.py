import requests

def get_job_listings():
    response = requests.get('https://jobs.sunway.com.my/api/get_listings')

    data = response.json()

    return data

get_job_listings()