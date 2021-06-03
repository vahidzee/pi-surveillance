from src.manager import Manager

pir_r = 23  # Associate pin 23 to right sensor
pir_l = 24  # Associate pin 24 to left sensor

if __name__ == '__main__':
    manager = Manager(pir_l, pir_r)
    manager.loop()
