# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text="Hello World!")

        return []
    
class ActionFetchPet(Action):
    
    def name(self) -> Text:
        return "action_fetch_pet"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Uzima vrstu ljubimca od korisnika
        pet_type = tracker.get_slot("pet_type")  # pet_type je slot koji chatbot koristi za odredjivanje vrste ljubimca
        
        # Definisanje URL-a na osnovu vrste ljubimca
        if pet_type == "dog":
            url = "http://localhost:3000/api/pet?type=pas&size=&availabe="
            response_text = "Here are the available dogs:"
        elif pet_type == "cat":
            url = "http://localhost:3000/api/pet?type=macka&size=&availabe="
            response_text = "Here are the available cats:"
        elif pet_type == "fish":
            url = "http://localhost:3000/api/pet?type=ribica&size=&availabe="
            response_text = "Here are the available fish:"
        elif pet_type == "hamster":
            url = "http://localhost:3000/api/pet?type=hrcak&size=&availabe="
            response_text = "Here are the available hamsters:"
        elif pet_type == "bird":
            url = "http://localhost:3000/api/pet?type=papagaj&size=&availabe="
            response_text = "Here are the available birds:"
        else:
            url = ""
            response_text = "Sorry, I couldn't find any pets for that type."

        # Slanje poruke korisniku sa odgovarajućim linkom za filtriranje
        dispatcher.utter_message(text=f"{response_text} You can see the details here: {url}")
        
        return []
# from rasa_sdk import Action
# from rasa_sdk.events import SlotSet

# class ActionProvidePetLink(Action):

#     def name(self) -> str:
#         return "action_provide_pet_link"

#     def run(self, dispatcher, tracker, domain):
#         pet_type = tracker.latest_message['text'].lower()

#         # Mappings for pet types to their respective API links
#         pet_links = {
#             'dog': 'http://localhost:5173/api/pet?type=pas&size=&availabe=',
#             'cat': 'http://localhost:3000/api/pet?type=macka&size=&availabe=',
#             'fish': 'http://localhost:3000/api/pet?type=ribica&size=&availabe=',
#             'hamster': 'http://localhost:3000/api/pet?type=hrcak&size=&availabe=',
#             'bird': 'http://localhost:3000/api/pet?type=papagaj&size=&availabe=',
#         }

#         # Check if the pet type is in the message and respond with the corresponding link
#         for pet, link in pet_links.items():
#             if pet in pet_type:
#                 dispatcher.utter_message(text=f"Here is the link to find {pet}s: {link}")
#                 return [SlotSet("requested_pet", pet)]

#         dispatcher.utter_message(text="Sorry, I couldn't find that pet type.")
#         return []
