import time
import RPi.GPIO as GPIO
from .camera import SmartCamera
from .iot import Client
from .I2C_LCD_driver import lcd


class Manager:
    def __init__(self, left_channel, right_channel):
        # LCD setup
        self.lcd = lcd()
        self.lcd.lcd_clear()

        # make instances of utilities
        self.client = Client(get_device_id())
        status = self.client.hello()
        if status == -1:
            self.lcd.lcd_clear()
            self.lcd.lcd_display_string(f'device id:')
            self.lcd.lcd_display_string(self.client.device_id, line=2)
            return
        encodings, ids, in_count = self.client.fetch()
        self.camera = SmartCamera(encodings, ids)
        self.lcd.lcd_display_string(f'{in_count} ' + ('person' if in_count == 1 else 'people') + ' inside')
        # pinout setup
        self.left_channel = left_channel
        self.right_channel = right_channel

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.left_channel, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Set pins as GPIO in
        GPIO.setup(self.right_channel, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        print("Waiting for sensor to settle")
        time.sleep(2)  # Waiting 2 seconds for the sensor to initiate
        print("Detecting motion")

        # add event listener on left PIR
        GPIO.add_event_detect(self.left_channel, GPIO.RISING, callback=self.interrupt, bouncetime=10000)

    def hello_again(self):
        time.sleep(1)
        self.client.hello()
        encodings, ids, _ = self.client.fetch()
        self.camera.set_faces(encodings, ids)

    def interrupt(self, channel):
        enter = True
        if GPIO.input(self.right_channel):  # True = Rising, person coming from right
            enter = False

        for capture in self.camera.capture():
            if not capture['known']:
                req_result = self.client.introduce(capture['pic'], capture['embedding'])
                while not req_result['ok']:
                    self.hello_again()
                    req_result = self.client.introduce(capture['pic'], capture['embedding'])
                else:
                    self.camera.add_face(capture['embedding'], req_result['face_id'])
                    capture['face_id'] = req_result['face_id']

            req_result = self.client.log(capture['face_id'], enter)
            while not req_result['ok']:
                self.hello_again()
                req_result = self.client.log(capture['face_id'], enter)
            else:
                counter, name = req_result['response']['in_count'], req_result['response']['name']
                self.lcd.lcd_clear()
                self.lcd.lcd_display_string(f'{counter} ' + ('person' if counter == 1 else 'people') + ' inside')
                self.lcd.lcd_display_string(f'welcome {name}', line=2)

    def loop(self):
        try:
            while True:
                time.sleep(1)  # wait 1 second
        except KeyboardInterrupt:
            self.camera.close()  # run on exit
            GPIO.cleanup()  # clean up
            print("\nAll cleaned up.\n")


def get_device_id():
    cpu_serial = "0000000000000000"
    try:
        f = open('/proc/cpuinfo', 'r')
        for line in f:
            if line[0:6] == 'Serial':
                cpu_serial = line[10:26]
        f.close()
    except:
        cpu_serial = "ERROR000000000"
    return cpu_serial
