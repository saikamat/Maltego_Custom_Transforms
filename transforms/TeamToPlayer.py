from extensions import registry
from maltego_trx.entities import IPAddress
from maltego_trx.maltego import UIM_TYPES, MaltegoMsg, MaltegoTransform
from maltego_trx.transform import DiscoverableTransform
import requests, os
from dotenv import load_dotenv


@registry.register_transform(display_name="Team to Player", input_entity="maltego.Organization",
                             description='Receive name of a football team, and shows current squad',
                             output_entities=["maltego.Person"])

def configure():
    load_dotenv()

configure()

class TeamToPlayer(DiscoverableTransform):
    # RETRIEVE SOURCE INFO
    @classmethod
    def get_team_id(cls, request: MaltegoMsg):
        team_name=request.Value
        # API call to get team ID from the name
        url = "https://api-football-v1.p.rapidapi.com/v3/teams"
        querystring = {"name":{team_name}}

        headers = {
            "X-RapidAPI-Key": os.getenv('api_key'),
            "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
        }
      
        api_response = requests.request("GET", url, headers=headers, params=querystring)
        data = api_response.json()
        
        if not (data['response']):
            raise Exception("INPUT ERROR: Incorrect Input Entity Name")
        else:
            team_id=data['response'][0]['team']['id']
            return team_id
        

    @classmethod
    def create_entities(cls, request: MaltegoMsg, response: MaltegoTransform):
        #""""
        url = "https://api-football-v1.p.rapidapi.com/v3/players/squads"

        querystring = {"team":{cls.get_team_id(request)}}

        headers = {
            "X-RapidAPI-Key": os.getenv('api_key'),
            "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
        }

        api_response = requests.request("GET", url, headers=headers, params=querystring)
        data = api_response.json()
                
        for player_id in data['response'][0]['players']:
        # Create Player Entity and add properties
            player_entity = response.addEntity("yourorganization.Player", player_id['name'])
            player_entity.addProperty(fieldName="position", displayName="Position", value=player_id['position'])
            player_entity.addProperty(fieldName="age", displayName="Age", value=player_id['age'])
            player_entity.addProperty(fieldName="PhotoURL", displayName="Image", value=player_id['photo'])
            player_entity.addProperty(fieldName="ID", displayName="ID", value=player_id['id'])

        