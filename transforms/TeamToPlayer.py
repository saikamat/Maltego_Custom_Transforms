from extensions import registry
from maltego_trx.entities import IPAddress
from maltego_trx.maltego import UIM_TYPES, MaltegoMsg, MaltegoTransform
from maltego_trx.transform import DiscoverableTransform
import requests, os, json
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
        # print(team_name) #DEBUG
        # API call to get team ID from the name
        url = "https://api-football-v1.p.rapidapi.com/v3/teams"
        querystring = {"name":{team_name}}

        headers = {
            "X-RapidAPI-Key": os.getenv('api_key'),
            "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
        }
      
        api_response = requests.request("GET", url, headers=headers, params=querystring)
        data = api_response.json()
        # print(data) #DEBUG
        try:
            if not (data['response']):
                print("ERROR: Incorrect Input Entity Name")
            else:
                team_id=data['response'][0]['team']['id']
                return team_id
        except Exception:
            raise Exception("Sorry!!") 

    @classmethod
    def create_entities(cls, request: MaltegoMsg, response: MaltegoTransform):
        print(cls.get_team_id(request)) # DEBUG
        #""""
        url = "https://api-football-v1.p.rapidapi.com/v3/players/squads"

        querystring = {"team":{cls.get_team_id(request)}}

        headers = {
            "X-RapidAPI-Key": os.getenv('api_key'),
            "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
        }

        api_response = requests.request("GET", url, headers=headers, params=querystring)
        data = api_response.json()
        #"""""

        """""
        # #****** DELETE THIS CODE LATER. IT'S HERE ONLY TO SAVE THE API CALLS ******
        # # Open a file and write the dictionary to it in JSON format
        # with open('data/team_squads.json', 'w') as f:
        #     json.dump(data, f)
        
        # # # # Close the file
        # f.close()
        print(data)

        
        with open('data/team_squads.json', 'r') as f:
            data = json.load(f)
        #****** UNTIL HERE ******
        # print(data['response'][0]['team']['name'])

        # Obtain information from source entity
        # teamName=data['response'][0]['team']['name']
        # print(teamName)
        # print(data['response'][0]['players'])
        
        # print('*****RESPONSE.JSON')
        # print(response1.json())
        """""
        #"""""
        for player_id in data['response'][0]['players']:
        # Create Player Entity and add properties
            player_entity = response.addEntity("yourorganization.Player", player_id['name'])
            player_entity.addProperty(fieldName="position", displayName="Position", value=player_id['position'])
            player_entity.addProperty(fieldName="age", displayName="Age", value=player_id['age'])
            player_entity.addProperty(fieldName="PhotoURL", displayName="Image", value=player_id['photo'])
            player_entity.addProperty(fieldName="ID", displayName="ID", value=player_id['id'])
        #"""""
        