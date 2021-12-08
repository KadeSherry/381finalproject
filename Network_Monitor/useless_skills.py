### teams Bot ###
from webexteamsbot import TeamsBot
from webexteamsbot.models import Response
import json
import requests
import paramiko_kade as K

teams_token = 'NzQwNmE0MGMtNDI5Yy00ODhkLTliMDQtM2ViY2E2MDdiZTA5NzZhYTEwZTMtMGU3_P0A1_529b5ae9-ae34-46f8-9993-5c34c3d90856' #Fill in your Teams Bot Token#

def do_something(incoming_msg):
    """
    Function to do some action.
    :param incoming_msg: The incoming message object from Teams
    :return: A text or markdown based reply
    """
    return "i did what you said - {}".format(incoming_msg.text)

def get_routing_protocol(incoming_msg):
    HOST = '192.168.56.105'
    PORT = '443'
    USER = 'cisco'
    PASS = 'cisco123!'

    url_base = "https://{h}/restconf".format(h=HOST)
    headers = {'Content-Type': 'application/yang-data+json',
     'Accept':'application/yang-data+json'}

    url = url_base + "/data/ietf-routing:routing-state"
    response = requests.get(url,
                            auth=(USER, PASS),
                            headers=headers,
                            verify=False
                            )

    data = response.json()["ietf-routing:routing-state"]["routing-instance"][0]
    route1 = response.json()["ietf-routing:routing-state"]["routing-instance"][0]["routing-protocols"]["routing-protocol"][0]
    route2 = response.json()["ietf-routing:routing-state"]["routing-instance"][0]["routing-protocols"]["routing-protocol"][1]
    route3 = response.json()["ietf-routing:routing-state"]["routing-instance"][0]["routing-protocols"]["routing-protocol"][2]
    route4 = response.json()["ietf-routing:routing-state"]["routing-instance"][0]["routing-protocols"]["routing-protocol"][3]

    print("Routing Protocols:")
    try:
        routingProtocol1 = route1["type"]
        routingProtocol2 = route2["type"]
        routingProtocol3 = route3["type"]
        routingProtocol4 = route4["type"]
        routerId = data["router-id"]
    except KeyError:
        print("Json Error")

    #print("Router ID: "+routerId)
    #print("Routing Protocol 1: "+routingProtocol1)
    #print("Routing Protocol 2: "+routingProtocol2)
    #print("Routing Protocol 3: "+routingProtocol3)
    #print("Routing Protocol 4: "+routingProtocol4)

    Test = "Router ID: "+routerId+"\nRouting Protocol 1: "+routingProtocol1+"\nRouting Protocol 2: "+routingProtocol2+"\nRouting Protocol 3: "+routingProtocol3+"\nRouting Protocol 4: "+routingProtocol4

    return Test

def show_card(incoming_msg):
    attachment = open("cardpayload.json").read()
    backupmessage = "You have an assignment!!!"

    c = create_message_with_attachment(
        incoming_msg.roomId, msgtxt=backupmessage, attachment=json.loads(attachment)
    )
    print(c)
    return ""

# An example of how to process card actions
def handle_cards(api, incoming_msg):
    """
    Function to handle card actions.
    :param api: webexteamssdk object
    :param incoming_msg: The incoming message object from Teams
    :return: A text or markdown based reply
    """
    m = get_attachment_actions(incoming_msg["data"]["id"])
    meeting = open("cardpayload.json").read()
    meeting = json.loads(meeting)
    # #print(meeting['content']['body'][0]['text'])
    return "New Due Date is- {}".format(m["inputs"])

def create_message(rid, msgtxt):
    headers = {
        "content-type": "application/json; charset=utf-8",
        "authorization": "Bearer " + teams_token,
    }

    url = "https://api.ciscospark.com/v1/messages"
    data = {"roomId": rid,"attachments":[], "markdown": msgtxt}
    response = requests.post(url, json=data, headers=headers)
    return response.json()

def create_message_with_attachment(rid, msgtxt, attachment):
    headers = {
        "content-type": "application/json; charset=utf-8",
        "authorization": "Bearer " + teams_token,
    }

    url = "https://api.ciscospark.com/v1/messages"
    data = {"roomId": rid, "attachments": [attachment], "markdown": msgtxt}
    response = requests.post(url, json=data, headers=headers)
    return response.json()


def get_attachment_actions(attachmentid):
    headers = {
        "content-type": "application/json; charset=utf-8",
        "authorization": "Bearer " + teams_token,
    }

    url = "https://api.ciscospark.com/v1/attachment/actions/" + attachmentid
    response = requests.get(url, headers=headers)
    return response.json()


# An example using a Response object.  Response objects allow more complex
# replies including sending files, html, markdown, or text. Rsponse objects
# can also set a roomId to send response to a different room from where
# incoming message was recieved.
def ret_message(incoming_msg):
    """
    Sample function that uses a Response object for more options.
    :param incoming_msg: The incoming message object from Teams
    :return: A Response object based reply
    """
    # Create a object to create a reply.
    response = Response()

    # Set the text of the reply.
    response.text = "Here's a fun little meme."

    # Craft a URL for a file to attach to message
    u = "https://giphy.com/gifs/justin-doge-3Owa0TWYqHi5RZYGql"
    response.link= u
    return response



#run the paramiko_kade file which will run show ip int br and output to Webex.

def get_interface_output(incoming_msg):
    ssh_client = K.connect("192.168.56.105", "22", "cisco", "cisco123!")
    shell = K.get_shell(ssh_client)
    TEST = K.show(shell,"show ip interface brief", n=10000, timeout = 1)
    K.close(ssh_client)
    """ssh_client = K.connect("192.168.56.107", "22", "cisco", "cisco123!")
    shell = K.get_shell(ssh_client)
    TEST2 = K.show(shell,"show ip interface brief", n=10000, timeout = 1)
    K.close(ssh_client)"""
    # this statement performs a GET on the specified url
    return TEST
    """return TEST2"""

def get_interface_output2(incoming_msg):
    ssh_client = K.connect("192.168.56.107", "22", "cisco", "cisco123!")
    shell = K.get_shell(ssh_client)
    TEST2 = K.show(shell,"show ip interface brief", n=10000, timeout = 1)
    K.close(ssh_client)
    # this statement performs a GET on the specified url
    return TEST2

# An example command the illustrates using details from incoming message within
# the command processing.
def current_time(incoming_msg):
    """
    Sample function that returns the current time for a provided timezone
    :param incoming_msg: The incoming message object from Teams
    :return: A Response object based reply
    """

    # Craft REST API URL to retrieve current time
    #   Using API from http://worldclockapi.com
    u = "http://worldclockapi.com/api/json/cst/now"
    r = requests.get(u).json()

    # If an invalid timezone is provided, the serviceResponse will include
    # error message
    if r["serviceResponse"]:
        return "Error: " + r["serviceResponse"]

    # Format of returned data is "YYYY-MM-DDTHH:MM<OFFSET>"
    #   Example "2018-11-11T22:09-05:00"
    returned_data = r["currentDateTime"].split("T")
    cur_date = returned_data[0]
    cur_time = returned_data[1][:5]
    timezone_name = r["timeZoneName"]

    # Craft a reply string.
    reply = "In {TZ} it is currently {TIME} on {DATE}.".format(
        TZ=timezone_name, TIME=cur_time, DATE=cur_date
    )
    return reply
