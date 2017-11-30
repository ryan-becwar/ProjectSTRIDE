from stravalib import Client
from tokens_file import *


client = Client(access_token=ACCESS_TOKEN)
athlete = client.get_athlete()

print(athlete)
