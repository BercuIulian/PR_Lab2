import json
import xml.etree.ElementTree as ET
from player import Player
from datetime import datetime
from .player_pb2 import player_pb2

class PlayerFactory:
    def to_json(self, players):
        '''
        This function should transform a list of Player objects into a list with dictionaries.
        '''
        return [{"nickname": player.nickname, "email": player.email,
                 "date_of_birth": player.date_of_birth.strftime("%Y-%m-%d"),
                 "xp": player.xp, "class": player.cls} for player in players]

    def from_json(self, list_of_dict):
        '''
        This function should transform a list of dictionaries into a list with Player objects.
        '''
        return [Player(player["nickname"], player["email"], player["date_of_birth"],
                       player["xp"], player["class"]) for player in list_of_dict]

    def from_xml(self, xml_string):
        '''
        This function should transform an XML string into a list with Player objects.
        '''
        root = ET.fromstring(xml_string)
        players = []
        for player_element in root.findall('player'):
            nickname = player_element.find('nickname').text
            email = player_element.find('email').text
            date_of_birth = player_element.find('date_of_birth').text
            xp = int(player_element.find('xp').text)
            cls = player_element.find('cls').text
            players.append(Player(nickname, email, date_of_birth, xp, cls))
        return players

    def to_xml(self, list_of_players):
        '''
        This function should transform a list with Player objects into an XML string.
        '''
        root = ET.Element("data")
        for player in list_of_players:
            player_element = ET.SubElement(root, "player")
            ET.SubElement(player_element, "nickname").text = player.nickname
            ET.SubElement(player_element, "email").text = player.email
            ET.SubElement(player_element, "date_of_birth").text = player.date_of_birth.strftime("%Y-%m-%d")
            ET.SubElement(player_element, "xp").text = str(player.xp)
            ET.SubElement(player_element, "cls").text = player.cls
        return ET.tostring(root, encoding='utf8').decode('utf8')

    def from_protobuf(self, binary):
        '''
        This function should transform a binary protobuf string into a list with Player objects.
        '''
        players = player_pb2.PlayersList()
        players.ParseFromString(binary)
        player_objects = []
        for player_msg in players.player:
            player = Player(
                player_msg.nickname,
                player_msg.email,
                player_msg.date_of_birth,
                player_msg.xp,
                player_pb2.Class.Name(player_msg.cls)
            )
            player_objects.append(player)
        return player_objects

    def to_protobuf(self, list_of_players):
        '''
        This function should transform a list with Player objects into a binary protobuf string.
        '''
        players = player_pb2.PlayersList()
        for player in list_of_players:
            player_msg = players.player.add()
            player_msg.nickname = player.nickname
            player_msg.email = player.email
            player_msg.date_of_birth = player.date_of_birth.strftime("%Y-%m-%d")
            player_msg.xp = player.xp
            player_msg.cls = player_pb2.Class.Value(player.cls)
        return players.SerializeToString()
