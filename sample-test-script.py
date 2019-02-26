import sys
import time
import Spanner
from Testboard import Testboard

import http.client, urllib.parse
import json

testboard = Testboard("Testboard1")

particle_token = "b4992ee32f43c39c8ea4fa0a178672c72f5dead8"
device_id = "370053000351353530373132"

# Our Product's Input will be connected the Testboard's Pin D3, making it our
# Output Pin
OUTPUT_PIN = "D3"

INPUT_PIN_RED = "A3"
INPUT_PIN_GREEN = "A2"
INPUT_PIN_BLUE = "A1"
INPUT_PIN_WHITE = "A0"

def toggle_digital_output():
    # set PIN state
    testboard.digitalWrite(OUTPUT_PIN, 'HIGH')
    time.sleep(1)
    testboard.digitalWrite(OUTPUT_PIN, 'LOW')
    time.sleep(1)
    testboard.digitalWrite(OUTPUT_PIN, 'HIGH')


def sendParticleCommand(auth_token, device, command, value):
    base_url = 'api.particle.io'
    api_path = '/v1/devices/'
    resource_uri =  api_path + device + '/' + command

    conn = http.client.HTTPSConnection(base_url)
    headers = {'Authorization': 'Bearer ' + auth_token, "Content-type": "application/x-www-form-urlencoded"}
    params = urllib.parse.urlencode({'@arg': value})

    print("=== Sending Particle Command ===")
    print("URL: https://" + base_url + resource_uri)
    print("Params: " + params)
    print("=== Headers ===")
    print(headers)

    conn.request('POST', resource_uri, params, headers)

    response = conn.getresponse()
    print("=== Raw Response ===")
    response = response.read().decode()
    print(response)
    print("====================")
    json_obj = json.loads(response)

    return json_obj["return_value"]

def setDeviceColor(color):
    return_code = sendParticleCommand(particle_token, device_id, "setColor", color)
    if(return_code != 1):
        sys.exit(1)

def setDeviceOn():
    return_code = sendParticleCommand(particle_token, device_id, "setOnOff", "1")
    if(return_code != 1):
        sys.exit(1)

def setDeviceOff():
    return_code = sendParticleCommand(particle_token, device_id, "setOnOff", "0")
    if(return_code != 0):
        sys.exit(1)

def testDeviceOffLEDs():
    setDeviceOff()
    time.sleep(2)
    value = testboard.analogRead(INPUT_PIN_RED)
    print("Read analog value: ","%d" % value, flush=True)
    Spanner.assertLessThan(100, value);

    value = testboard.analogRead(INPUT_PIN_GREEN)
    print("Read analog value: ","%d" % value, flush=True)
    Spanner.assertLessThan(100, value);

    value = testboard.analogRead(INPUT_PIN_BLUE)
    print("Read analog value: ","%d" % value, flush=True)
    Spanner.assertLessThan(100, value);

    value = testboard.analogRead(INPUT_PIN_WHITE)
    print("Read analog value: ","%d" % value, flush=True)
    Spanner.assertLessThan(100, value);

def testDeviceColorAllFullLEDs():
    setDeviceColor("ffffffff")
    time.sleep(2)
    value = testboard.analogRead(INPUT_PIN_RED)
    print("Read analog value: ","%d" % value, flush=True)
    Spanner.assertGreaterThan(4000, value);

    value = testboard.analogRead(INPUT_PIN_GREEN)
    print("Read analog value: ","%d" % value, flush=True)
    Spanner.assertGreaterThan(4000, value);

    value = testboard.analogRead(INPUT_PIN_BLUE)
    print("Read analog value: ","%d" % value, flush=True)
    Spanner.assertGreaterThan(4000, value);

    value = testboard.analogRead(INPUT_PIN_WHITE)
    print("Read analog value: ","%d" % value, flush=True)
    Spanner.assertGreaterThan(4000, value);

def testDeviceButtonToggleOnOffOn():
    value = testboard.analogRead(INPUT_PIN_RED)
    print("Read analog value: ","%d" % value, flush=True)
    Spanner.assertGreaterThan(4000, value);

    value = testboard.analogRead(INPUT_PIN_GREEN)
    print("Read analog value: ","%d" % value, flush=True)
    Spanner.assertGreaterThan(4000, value);

    value = testboard.analogRead(INPUT_PIN_BLUE)
    print("Read analog value: ","%d" % value, flush=True)
    Spanner.assertGreaterThan(4000, value);

    value = testboard.analogRead(INPUT_PIN_WHITE)
    print("Read analog value: ","%d" % value, flush=True)
    Spanner.assertGreaterThan(4000, value);

    toggle_digital_output()
    
    value = testboard.analogRead(INPUT_PIN_RED)
    print("Read analog value: ","%d" % value, flush=True)
    Spanner.assertLessThan(100, value);

    value = testboard.analogRead(INPUT_PIN_GREEN)
    print("Read analog value: ","%d" % value, flush=True)
    Spanner.assertLessThan(100, value);

    value = testboard.analogRead(INPUT_PIN_BLUE)
    print("Read analog value: ","%d" % value, flush=True)
    Spanner.assertLessThan(100, value);

    value = testboard.analogRead(INPUT_PIN_WHITE)
    print("Read analog value: ","%d" % value, flush=True)
    Spanner.assertLessThan(100, value);

    toggle_digital_output()

    value = testboard.analogRead(INPUT_PIN_RED)
    print("Read analog value: ","%d" % value, flush=True)
    Spanner.assertGreaterThan(4000, value);

    value = testboard.analogRead(INPUT_PIN_GREEN)
    print("Read analog value: ","%d" % value, flush=True)
    Spanner.assertGreaterThan(4000, value);

    value = testboard.analogRead(INPUT_PIN_BLUE)
    print("Read analog value: ","%d" % value, flush=True)
    Spanner.assertGreaterThan(4000, value);

    value = testboard.analogRead(INPUT_PIN_WHITE)
    print("Read analog value: ","%d" % value, flush=True)
    Spanner.assertGreaterThan(4000, value);


if __name__ == "__main__":
    Spanner.assertTrue(True)

    testDeviceOffLEDs()

    time.sleep(5)
    
    testDeviceColorAllFullLEDs()

    time.sleep(5)
    
    testDeviceButtonToggleOnOffOn()

