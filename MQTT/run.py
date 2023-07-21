import paho.mqtt.client as mqtt
from AIRSensorDAO import add_air_data
from THSensorDAO import add_th_data
import json
from dateutil.parser import parse


# MQTT configurations
mqtt_broker = "47.190.103.180"
mqtt_port = 1883
mqtt_topic = "application/1/device/ff000000000013dc/event/up"
auth_username = "iobMQTT"
auth_password = "mqtt123456"

# MQTT callback function
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code: " + str(rc))
    client.subscribe(mqtt_topic)

def on_message(client, userdata, msg):
    # Decode and print the message payload based on its format
    # print("--------")
    # print(msg)
    # print("--------")
    decoded_data = decode_payload(msg.topic, msg.payload)
    print(decoded_data)
    obj = json.loads(decoded_data)
    
    try:
        if(len(obj["object"]["messages"])==2): #TH data
            sensor_values = {}
            for o in obj["object"]["messages"]:
                if(o["measurementId"]=="Humidity"):
                    sensor_values["humidity_value"]=o["measurementValue"]
                elif(o["measurementId"]=="Temperature"):
                    sensor_values["temperature_value"]=o["measurementValue"]
            
            datetime_object = parse(obj["rxInfo"][0]["time"])
            mysql_date_string = datetime_object.strftime("%Y-%m-%d %H:%M:%S")
            add_th_data(sensor_values["humidity_value"],sensor_values["temperature_value"],obj["devEUI"],mysql_date_string)
            
        else: #AIR data

            sensor_values = {}
            for o in obj["object"]["messages"]:
                if(o["measurementId"]=="NO2"):
                    sensor_values["NO2_value"]=o["measurementValue"]
                elif(o["measurementId"]=="SO2"):
                    sensor_values["SO2_value"]=o["measurementValue"]
                elif(o["measurementId"]=="O3"):
                    sensor_values["O3_value"]=o["measurementValue"]
            
            datetime_object = parse(obj["rxInfo"][0]["time"])
            mysql_date_string = datetime_object.strftime("%Y-%m-%d %H:%M:%S")
            add_air_data(sensor_values["SO2_value"],sensor_values["NO2_value"],sensor_values["O3_value"],obj["devEUI"],mysql_date_string)
    except Exception as e:
        print('Exception: ',e)


def decode_payload(topic, payload):
    # Decode the message payload based on its topic or payload format
    decoded_data = None

    # Check the topic or payload format to determine the decoding logic
    if topic.startswith("$SYS/broker/connection/"):
        # Example: Connection status message
        decoded_data = decode_connection_status(payload)
    elif topic.startswith("$SYS/broker/clients/"):
        # Example: Client registration message
        decoded_data = decode_client_registration(payload)
    elif topic.startswith("$SYS/broker/network/"):
        # Example: Network statistics message
        decoded_data = decode_network_statistics(payload)
    else:
        # Unknown or unhandled topic
        decoded_data = payload.decode("utf-8")  # Assume plain text payload

    return decoded_data

def decode_connection_status(payload):
    # Implement the decoding logic for connection status messages
    decoded_data = payload.decode("utf-8")  # Assume plain text payload

    return decoded_data

def decode_client_registration(payload):
    # Implement the decoding logic for client registration messages
    decoded_data = payload.decode("utf-8")  # Assume plain text payload

    return decoded_data

def decode_network_statistics(payload):
    # Implement the decoding logic for network statistics messages
    decoded_data = payload.decode("utf-8")  # Assume plain text payload

    return decoded_data

# Create MQTT client
client = mqtt.Client()

# Set MQTT callbacks
client.on_connect = on_connect
client.on_message = on_message

# authentication
client.username_pw_set(auth_username, auth_password)

# Connect to MQTT broker
client.connect(mqtt_broker, mqtt_port)

# Start MQTT loop (this function will block and handle MQTT events in the background)
client.loop_forever()