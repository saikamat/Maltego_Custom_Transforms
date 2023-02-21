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

    @classmethod
    def create_entities(cls, request: MaltegoMsg, response: MaltegoTransform):
        # url = "https://api-football-v1.p.rapidapi.com/v3/players/squads"

        # querystring = {"team":"33"}

        # headers = {
        #     "X-RapidAPI-Key": os.getenv('api_key'),
        #     "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
        # }

        # response = requests.request("GET", url, headers=headers, params=querystring)
        # data = response.json()
        # #****** DELETE THIS CODE LATER. IT'S HERE ONLY TO SAVE THE API CALLS ******
        # # Open a file and write the dictionary to it in JSON format
        # with open('data/team_squads.json', 'w') as f:
        #     json.dump(data, f)
        
        # # # Close the file
        # f.close()

        with open('data/1_PLAYER_SQ_BKUP.json', 'r') as f:
            data = json.load(f)
        #****** UNTIL HERE ******
        print(data['response'][0]['team']['name'])

        # Obtain information from source entity
        teamName=data['response'][0]['team']['name']
        player_name=data['response'][0]['players'][26]['name']
        player_position=data['response'][0]['players'][26]['position']
        player_age=data['response'][0]['players'][26]['age']
        player_image_url=data['response'][0]['players'][26]['photo']
        # print(type(player_name))

        # Create Player Entity
        player_entity = response.addEntity("yourorganization.Player", player_name)
        player_entity.addProperty(fieldName="position", displayName="Position", value=player_position)
        player_entity.addProperty(fieldName="age", displayName="Age", value=player_age)
        player_entity.addProperty(fieldName="PhotoURL", displayName="Image", value=player_image_url)
        # request_player_name = request.getProperty(player_name)
        # print(type(request_player_name))
        # player_entity.addProperty("Full Name", value=request_player_name) #28 is random player index