import json
import time
import requests
import math
import argparse
import logging
import os
import sys

CONFIG_FILE = 'config.json'

def is_running_in_terminal():
    return sys.stdout.isatty()

if is_running_in_terminal():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
else:
    logging.basicConfig(
        filename='main.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def wait_for_network(timeout=30):
    logging.info("Waiting for network connectivity...")
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            requests.get('https://www.google.com', timeout=5)
            logging.info("Network connectivity established.")
            return True
        except requests.ConnectionError:
            logging.warning("Network not available, retrying...")
            time.sleep(5)
    logging.error("Network not available after waiting for 30 seconds.")
    return False

def load_config():
    try:
        with open(CONFIG_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        logging.warning("Configuration file not found. Creating a new one.")
        return {}

def save_config(config):
    with open(CONFIG_FILE, 'w') as file:
        json.dump(config, file)
        logging.info("Configuration saved.")

def find_bridge():
    logging.info("Searching for Hue Bridge...")
    response = requests.get('https://discovery.meethue.com/')
    if response.status_code == 200 and len(response.json()) > 0:
        bridge_ip = response.json()[0]['internalipaddress']
        logging.info(f"Hue Bridge found at IP: {bridge_ip}")
        return bridge_ip
    else:
        logging.error("No Hue Bridge found.")
        exit(1)

def register_hue_user(bridge_ip):
    url = f"http://{bridge_ip}/api"
    data = {"devicetype": "my_hue_app#raspberrypi"}
    while True:
        logging.info("Press the button on the Hue Bridge to connect...")
        response = requests.post(url, json=data).json()
        if "success" in response[0]:
            username = response[0]["success"]["username"]
            logging.info("Connected to the Hue Bridge.")
            return username
        else:
            logging.warning("Waiting 5 seconds before retrying...")
            time.sleep(5)

def get_full_color_lights(bridge_ip, username):
    lights_url = f"http://{bridge_ip}/api/{username}/lights"
    response = requests.get(lights_url).json()

    logging.info("Retrieving full color lights...")
    full_color_lights = {}

    for light_id, light in response.items():
        if light['type'] in ['Extended color light', 'Color light']:
            logging.info(f"Found full color light: {light['name']} (ID: {light_id})")
            full_color_lights[light_id] = light

    return full_color_lights

def find_full_color_lights(bridge_ip, username, selected_lights=None):
    lights = get_full_color_lights(bridge_ip, username)

    if not selected_lights:
        full_color_lights = []
        logging.info("Automatically selecting the first two full color lights.")
        for light_id, light in lights.items():
            full_color_lights.append(light_id)
            logging.info(f"Selected light: {light['name']} (ID: {light_id})")
            if len(full_color_lights) == 2:
                break

        logging.info("To choose specific lights, run the script with '--lights' followed by the light IDs, e.g., 'python main.py --lights 5 6'.")
        return full_color_lights
    else:
        full_color_lights = []
        for light_id in selected_lights:
            if light_id in lights:
                full_color_lights.append(light_id)
                logging.info(f"Selected light: {lights[light_id]['name']} (ID: {light_id})")
            else:
                logging.error(f"Light ID {light_id} is invalid or not a full color light.")
                exit(1)
        return full_color_lights

def parse_arguments():
    parser = argparse.ArgumentParser(description='Select Philips Hue lights.')
    parser.add_argument('--lights', nargs=2, help='IDs of the full color lights to control')
    args = parser.parse_args()
    return args.lights

def get_unix_time():
    return time.time()

def get_rgb_color_from_decimal_number(number):
    r = 0
    g = 0
    b = number
    if b > 255:
        g = math.floor(number / 256)
        b = number - (g * 256)
    if g > 255:
        r = math.floor((number / 256) / 256)
        g = g - (r * 256)
    return f"{r},{g},{b}"

def get_gradient():
    timestamp = int(get_unix_time())
    gradient = ["0,0,0", "0,0,0"]

    if timestamp > 16777215:
        gradient[0] = get_rgb_color_from_decimal_number(timestamp // 16777215)
        gradient[1] = get_rgb_color_from_decimal_number(timestamp % 16777215)
    else:
        gradient[1] = get_rgb_color_from_decimal_number(timestamp)

    return gradient

def convert(red, green, blue):
    normalized = {
        'red': red / 255.0,
        'green': green / 255.0,
        'blue': blue / 255.0
    }

    colors = {color: ((normalized[color] + 0.055) / 1.055) ** 2.4 if normalized[color] > 0.04045 else normalized[color] / 12.92 for color in normalized}

    X = colors['red'] * 0.649926 + colors['green'] * 0.103455 + colors['blue'] * 0.197109
    Y = colors['red'] * 0.234327 + colors['green'] * 0.743075 + colors['blue'] * 0.022598
    Z = colors['red'] * 0.000000 + colors['green'] * 0.072310 + colors['blue'] * 0.986039
    total = X + Y + Z

    x = X / total if total != 0 else 0
    y = Y / total if total != 0 else 0
    bri = round(Y * 255)

    return {'x': x, 'y': y, 'bri': int(bri)}

def update_light(gradient, light_url):
    color = gradient.split(',')
    settings = convert(float(color[0]), float(color[1]), float(color[2]))
    data_light = '{"transitiontime": 0, "xy": [' + str(settings['x']) + ', ' + str(settings['y']) + ']}'
    requests.put(light_url, data_light)
    # logging.info(f"Updated light at {light_url} to color {color}")

def main_loop(bridge_ip, username, light_ids):
    previousTimestamp = 0
    previousColor1 = ''
    previousColor2 = ''
    updateAllIntervalInSeconds = (10 * 60)
    updateAllPreviousUpdate = 0

    while True:
        timestamp = int(get_unix_time())
        if timestamp != previousTimestamp:
            gradients = get_gradient()
            color1 = gradients[0]
            color2 = gradients[1]

            if color1 != previousColor1 or (timestamp - updateAllPreviousUpdate) >= updateAllIntervalInSeconds:
                update_light(color1, f"http://{bridge_ip}/api/{username}/lights/{light_ids[0]}/state")
                previousColor1 = color1

            if color2 != previousColor2 or (timestamp - updateAllPreviousUpdate) >= updateAllIntervalInSeconds:
                update_light(color2, f"http://{bridge_ip}/api/{username}/lights/{light_ids[1]}/state")
                previousColor2 = color2

            if (timestamp - updateAllPreviousUpdate) >= updateAllIntervalInSeconds:
                updateAllPreviousUpdate = timestamp

            previousTimestamp = timestamp

        time.sleep(0.1)

def main():
    if not wait_for_network():
        logging.error("Network initialization failed. Exiting.")
        return

    config = load_config()

    if 'bridge_ip' not in config or 'username' not in config:
        bridge_ip = find_bridge()
        username = register_hue_user(bridge_ip)
        config['bridge_ip'] = bridge_ip
        config['username'] = username
        save_config(config)
    else:
        bridge_ip = config['bridge_ip']
        username = config['username']

    selected_lights = parse_arguments()

    full_color_lights = find_full_color_lights(bridge_ip, username, selected_lights)

    if not full_color_lights:
        logging.error("No full color lights found.")
        return

    logging.info(f"Full color lights being used: {full_color_lights}")

    main_loop(bridge_ip, username, full_color_lights)

if __name__ == "__main__":
    main()
