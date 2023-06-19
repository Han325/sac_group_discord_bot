import csv
import pytz
import datetime
from dateutil.parser import parse

from data import get_job_listings
from filter import get_relevant_listings

def parse_duration(time_str):
    parts = time_str.split(':')
    return datetime.timedelta(hours=int(parts[0]), minutes=int(parts[1]), seconds=int(parts[2]))


def write_to_csv(interests, current_time, duration, filename='interests.csv'):
    with open(filename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for interest in interests:
            writer.writerow([interest, current_time, duration])


def process_csv_and_get_jobs(filename='interests.csv'):
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            interest = row[0]
            
            # convert stored_time to a timezone aware datetime object
            local_tz = pytz.timezone('Asia/Kuala_Lumpur')
            stored_time_naive = datetime.datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S.%f')
            stored_time = local_tz.localize(stored_time_naive)
            
            duration = parse_duration(row[2])
            get_listings = get_job_listings()
            listings = get_relevant_listings(get_listings, interest)

            if listings:
                for listing in listings:
                    # date_offered is already timezone aware
                    date_offered = parse(listing['date_offered'])
                    
                    if date_offered >= stored_time and date_offered <= (stored_time + duration):
                        print(f"New job posting for {interest}: {listing}")
            else:
                return None

