import machine
import network
import usocket as socket
import utime

# Wi-Fi connection settings
WIFI_SSID = "BH-10.2"

# Server settings
SERVER_PORT = 80

# Initialize Wi-Fi connection
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(WIFI_SSID)
while not wifi.isconnected():
    utime.sleep_ms(100)

# Print the IP address
ip_address = wifi.ifconfig()[0]
print("IP address:", ip_address)

# Initialize server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('', SERVER_PORT))
server_socket.listen(1)

# Initialize PWM object for the servo motor
servo_pin = machine.Pin(16)
servo_pwm = machine.PWM(servo_pin)

# Loop forever
while True:
    # Wait for a client to connect
    client_socket, client_address = server_socket.accept()
    print("Client connected:", client_address)

    # Receive the HTTP request
    request = client_socket.recv(1024).decode('utf-8')
    print("Request:", request)

    # Parse the servo status from the request URL
    servo_status = None
    parts = request.split(' ')
    for i, part in enumerate(parts):
        if part == '/?servo=on':
            servo_status = True
        elif part == '/?servo=off':
            servo_status = False

    # Control the servo motor based on the request
    if servo_status is not None:
        if servo_status:
            servo_pwm.duty_u16(6000)
        else:
            servo_pwm.duty_u16(1500)

    # Send the response
    response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\nServo status: {}\r\n".format(servo_status)
    client_socket.send(response.encode('utf-8'))

    # Close the client socket
    client_socket.close()