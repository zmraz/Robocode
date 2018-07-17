import bluetooth as bt
import RPi.GPIO as GPIO 
import time 

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

lf = 7
rb = 9
rf = 10
lb = 8

frequency = float(20)
duty_cycle = float(30)
stop = float(0)

GPIO.setup(lb, GPIO.OUT) # left backwards
GPIO.setup(lf, GPIO.OUT) # left forward
GPIO.setup(rb, GPIO.OUT) # right backwards
GPIO.setup(rf, GPIO.OUT) # right forward

left_back = GPIO.PWM(lb, frequency) # left backwards
left_forward = GPIO.PWM(lf, frequency) # left forward
right_back = GPIO.PWM(rb, frequency) # right backwards
right_forward = GPIO.PWM(rf, frequency) # right forward


# Turn all motors off
left_back.start(stop)
left_forward.start(stop)
right_back.start(stop)
right_forward.start(stop)

def stop():
    global stop
    left_back.ChangeDutyCycle(0) 
    left_forward.ChangeDutyCycle(0) 
    right_back.ChangeDutyCycle(0) 
    right_forward.ChangeDutyCycle(0)  

def left():
    global duty_cycle
    left_back.ChangeDutyCycle(0) 
    left_forward.ChangeDutyCycle(float(duty_cycle)) 
    right_back.ChangeDutyCycle(0) 
    right_forward.ChangeDutyCycle(0) 
    time.sleep(0.2)
    stop()

def forward():
    global duty_cycle
    left_back.ChangeDutyCycle(0) 
    left_forward.ChangeDutyCycle(float(duty_cycle)) 
    right_back.ChangeDutyCycle(0) 
    right_forward.ChangeDutyCycle(float(duty_cycle)) 
    time.sleep(1)
    stop()
    
def step():
    global duty_cycle
    left_back.ChangeDutyCycle(0) 
    left_forward.ChangeDutyCycle(float(duty_cycle)) 
    right_back.ChangeDutyCycle(0) 
    right_forward.ChangeDutyCycle(float(duty_cycle)) 
    time.sleep(0.5)
    stop()

def right():
    global duty_cycle
    left_back.ChangeDutyCycle(0) 
    left_forward.ChangeDutyCycle(0) 
    right_back.ChangeDutyCycle(0) 
    right_forward.ChangeDutyCycle(float(duty_cycle)) 
    time.sleep(0.5)
    stop()
    
def back():
    global duty_cycle
    left_back.ChangeDutyCycle(float(duty_cycle)) 
    left_forward.ChangeDutyCycle(0) 
    right_back.ChangeDutyCycle(float(duty_cycle)) 
    right_forward.ChangeDutyCycle(0) 
    time.sleep(0.5)
    stop()

def circle():
    for i in range(1,10):
        left()
        step()
    

def zigzag():
    right()
    forward()
    left()
    forward()
    right()
    forward()
    left()
    forward()
    right()
    forward()
    left()
    forward()
    
def dance():
    for i in range(1,3):
        left()
        right()
        left()
        left()
        right()
        right()
        step()
        right()
        back()
        right()
        step()
        right()
        back()
        right()

def robot():
    step()
    step()
    step()
    step()
    right()
    right()
    right()
    right()
    right()
    right()
    


commands = ('go,step,back,left,right,circle,zigzag,robot')
#sudo python server.py
server_sock=bt.BluetoothSocket( bt.RFCOMM )
server_sock.bind(("",bt.PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = '85d86026-b42f-4415-b3d1-9aad2647ea53'

bt.advertise_service( server_sock, "SampleServer",
                   service_id = uuid,
                   service_classes = [ uuid, bt.SERIAL_PORT_CLASS ],
                   profiles = [ bt.SERIAL_PORT_PROFILE ], 
#                   protocols = [ OBEX_UUID ] 
                    )
                   
print("Waiting for connection on RFCOMM channel %d" % port)

client_sock, client_info = server_sock.accept()
print("Accepted connection from ", client_info)
client_sock.send(commands)

try:
    while True:
        data = client_sock.recv(1024)
        if len(data) == 0: break
        print("received [%s]" % data)
        if data == 'circle':
            circle()
        elif data == 'zigzag':
            zigzag()
        elif data == 'left':
            left()
        elif data == 'right':
            right()
        elif data == 'go':
            forward()
        elif data == 'step':
            step()
        elif data == 'dance':
            dance()
        elif data == 'back':
            back()
        elif data == 'robot':
            robot()
        elif data == "Robert":
            robot()
        
except IOError:
    pass

print("disconnected")

client_sock.close()
server_sock.close()
print("all done")
