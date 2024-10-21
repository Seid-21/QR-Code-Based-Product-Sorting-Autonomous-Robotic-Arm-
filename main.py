import time
import serial
import RPi.GPIO as GPIO

# Setup for GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Servo pins
servo_pins = [3, 5, 6, 9, 10, 11]

# Initialize GPIO pins
for pin in servo_pins:
    GPIO.setup(pin, GPIO.OUT)

# Set initial servo angles (duty cycles for PWM)
servo_angles = [100, 90, 150, 60, 80, 117]

# Initialize PWM for each servo
servos = [GPIO.PWM(pin, 50) for pin in servo_pins]  # 50Hz frequency
for i, servo in enumerate(servos):
    servo.start(servo_angles[i])

# Initialize serial communication
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)  # Adjust serial port as necessary

def set_servo_angle(servo_index, angle):
    duty = angle / 18 + 2  # Convert angle to duty cycle
    servos[servo_index].ChangeDutyCycle(duty)
    time.sleep(1)  # Wait for the servo to reach the position

def process_item_a():
    set_servo_angle(1, 70)
    set_servo_angle(4, 130)
    set_servo_angle(2, 180)
    set_servo_angle(5, 67)  # Go down and hold
    set_servo_angle(1, 130)
    set_servo_angle(0, 60)
    set_servo_angle(0, 14)
    set_servo_angle(1, 95)
    set_servo_angle(4, 100)
    set_servo_angle(5, 117)  # Pick & sort
    reset_servos()

def process_item_b():
    set_servo_angle(1, 70)
    set_servo_angle(4, 130)
    set_servo_angle(2, 180)
    set_servo_angle(5, 67)  # Go down and hold
    set_servo_angle(1, 130)
    set_servo_angle(0, 140)
    set_servo_angle(0, 180)
    set_servo_angle(1, 95)
    set_servo_angle(4, 100)
    set_servo_angle(5, 117)  # Pick & sort
    reset_servos()

def reset_servos():
    set_servo_angle(2, 150)
    set_servo_angle(1, 90)
    set_servo_angle(4, 80)
    set_servo_angle(0, 60)
    set_servo_angle(0, 100)

# Main loop
try:
    while True:
        if ser.in_waiting > 0:
            read_string = ser.readline().decode('utf-8').strip()
            print(f"Received: {read_string}")

            if read_string == "ITEM_A":
                process_item_a()
            elif read_string == "ITEM_B":
                process_item_b()

except KeyboardInterrupt:
    print("Exiting program...")

finally:
    ser.close()
    for servo in servos:
        servo.stop()
    GPIO.cleanup()

