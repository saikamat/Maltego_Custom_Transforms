from extensions import registry
from maltego_trx.entities import IPAddress
from maltego_trx.maltego import UIM_TYPES, MaltegoMsg, MaltegoTransform
from maltego_trx.transform import DiscoverableTransform
import requests, os, json
from dotenv import load_dotenv

@registry.register_transform(display_name="Player to Performance", input_entity="maltego.Person",
                             description='Receive name of a player, and show if he scored more than 10 goals',
                             output_entities=["maltego.AS"])

def configure():
    load_dotenv()

configure()

class PlayerToPerformance(DiscoverableTransform):

    @classmethod
    def create_entities(cls, request: MaltegoMsg, response: MaltegoTransform):
        # RETRIEVE SOURCE INFO
        # def get_player_id():
        # get
        url = "https://api-football-v1.p.rapidapi.com/v3/players"

        querystring = {"id":"909","season":"2022"}

        headers = {
            "X-RapidAPI-Key": os.getenv('api_key'),
            "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
        }

        api_response = requests.request("GET", url, headers=headers, params=querystring)
        data = api_response.json()
        print(data['response'][0]['statistics'][0]['games']['rating'])

        performance_ratings_entity = response.addEntity("yourorganization.AS", data['response'][0]['statistics'][0]['games']['rating'])
        performance_ratings_entity.addProperty(fieldName="rating", displayName="Rating", value=data['response'][0]['statistics'][0]['games']['rating'])

        #****** DELETE THIS CODE LATER. IT'S HERE ONLY TO SAVE THE API CALLS ******
        
        #Open a file and write the dictionary to it in JSON format
        # with open('data/player_performance.json', 'w') as f:
        #     json.dump(data, f)
        
        # # # Close the file
        # f.close()

        # with open('data/2_PLAYER_PERFORMANCE_BKUP.json', 'r') as f:
            # data = json.load(f)
        #****** UNTIL HERE ******
        # print(data)
