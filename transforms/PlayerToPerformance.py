from extensions import registry
from maltego_trx.entities import IPAddress
from maltego_trx.maltego import UIM_TYPES, MaltegoMsg, MaltegoTransform
from maltego_trx.transform import DiscoverableTransform
import requests, os
from dotenv import load_dotenv

@registry.register_transform(display_name="Player to Rating", input_entity="maltego.Person",
                             description='Receive name of a player, and show if he scored more than 10 goals',
                             output_entities=["maltego.AS"])

def configure():
    load_dotenv()

configure()
HIGH_SCORE_CRITERION = 6.5
class PlayerToPerformance(DiscoverableTransform):
    # RETRIEVE SOURCE INFO
    @classmethod
    def get_player_id(cls, request: MaltegoMsg):
        player_id=request.getProperty("ID")
        return player_id

    @classmethod
    def create_entities(cls, request: MaltegoMsg, response: MaltegoTransform): 
        # print(cls.get_player_id(request))
        #"""""
        url = "https://api-football-v1.p.rapidapi.com/v3/players"
        
        querystring = {"id":{cls.get_player_id(request)},"season":"2022"}

        headers = {
            "X-RapidAPI-Key": os.getenv('api_key'),
            "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
        }

        api_response = requests.request("GET", url, headers=headers, params=querystring)
        data = api_response.json()

        rating = data['response'][0]['statistics'][0]['games']['rating']

        if float(rating) > HIGH_SCORE_CRITERION:
            performance_ratings_entity = response.addEntity("yourorganization.AS", rating)
            performance_ratings_entity.addProperty(fieldName="rating", displayName="Rating", value=rating)