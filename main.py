#!/usr/bin/env pybricks-micropython
from pybricks.tools import wait, StopWatch, DataLog

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Button
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import ImageFile

import time
#import ev3_dc as ev3speaker


# Initialize the EV3 Brick.
ev3 = EV3Brick()

# Initialize the motors.
left_motor = Motor(Port.B)
right_motor = Motor(Port.C)

# Array av animasjoner
Glad = [ImageFile.AWAKE,
        ImageFile.WINKING,
        ImageFile.AWAKE,
        ImageFile.THUMBS_UP,
        ]

Sint = [ImageFile.AWAKE,
        ImageFile.ANGRY,
        ImageFile.EVIL,
        ImageFile.PINCHED_LEFT,
        ImageFile.PINCHED_MDDLE,
        ImageFile.UP,
        ImageFile.THUMS_DOWN]



robot = DriveBase(left_motor, right_motor, wheel_diameter=55.5, axle_track=104)

#####
ev3.speaker.set_speech_options(language='no', voice='f1', speed=None, pitch=None) ##voice settings
ev3.speaker.set_volume(100, which='_all_') #volum settings tts



###nykode
knapp= TouchSensor(Port.S2)
sensorv=UltrasonicSensor(Port.S1)
sensorh=UltrasonicSensor(Port.S4)

knappStatus=True


def stopp():
    robot.stop()
    

def hindring(): ###definisjon for hvis roboten møter på hindring
    robot.stop()
    robot.turn(-96)


def kjøra():
    robot.straight(1000)
    robot.turn

meny = [
    ["Er du et menneske?", "Ja", "Nei"],
    ["Vil du donere?", "Ja", "Nei"],
    ["Velg mottaker", "Røde Kors", "Barnekreft", "TV-Aksjonen", "Fattige studenter"],
    ["Velg student", "Petter", "Torkil", "Amund", "Are"],
    ["Donasjons metode", "Vipps", "Kontant"]
]

vipps_numre = {
    "Røde Kors": "2272",
    "Barnekreft": "02099",
    "TV-Aksjonen": "3366",
    "Frelsesarmeen": "2309",
    "Petter": "40433005",
    "Torkil": "41365950",
    "Amund": "46809142",
    "Are": "41766895"
}

def tegn_meny(pos, valg):
    ev3.screen.clear()
    ev3.screen.print(valg[0])
    ev3.screen.print("")
    for i in range(1, len(valg)):
        prefix = ">" if i == pos else " "
        ev3.screen.print(prefix + " " + valg[i])

nivå = 0
pos = 1
aktiv = meny[nivå]
valgt_mottaker = None
tegn_meny(pos, aktiv)



while (True):

    while knappStatus == True:              #https://pybricks.com/ev3-micropython/examples/robot_educator_ultrasonic.html
        nivå = 0
        aktiv = meny[nivå]
        ev3.screen.print("Vil du donere?")
        wait(20)
        ev3.screen.clear()

        #if knapp.pressed() == True:
         #   knappStatus = False
        if sensorv.distance() <80 or sensorh.distance() <80:
            start_timer = time.time()
            robot.stop()
            ev3.screen.clear()
            tegn_meny(pos, aktiv)
            while True:
                if nivå == 0 and time.time() - start_timer >= 10:
                    hindring()
                    break
                if Button.UP in ev3.buttons.pressed():
                    pos = (pos - 1) if pos > 1 else len(aktiv) - 1
                    tegn_meny(pos, aktiv)
                    wait(300)

                elif Button.DOWN in ev3.buttons.pressed():
                    pos = (pos + 1) if pos < len(aktiv) - 1 else 1
                    tegn_meny(pos, aktiv)
                    wait(300)

                elif Button.CENTER in ev3.buttons.pressed():
                    valg = aktiv[pos]

                    if nivå == 0:
                        if valg == "Nei":
                            ev3.screen.clear()
                            ev3.screen.print("Avslutter...")
                            hindring()
                            break
                        else:
                            nivå = 1
                            pos = 1
                            aktiv = meny[nivå]
                            tegn_meny(pos, aktiv)

                    elif nivå == 1:
                        if valg == "Nei":
                            ev3.screen.clear()
                            ev3.screen.print("Ingen donasjon.")
                            ev3.speaker.play_file('fornermelse.wav')
                            for f in Sint:
                                ev3.screen.load_image(f)
                                wait(140)
                            wait(2000)
                            hindring()
                            break
                        else:
                            nivå = 2
                            pos = 1
                            aktiv = meny[nivå]
                            tegn_meny(pos, aktiv)

                    elif nivå == 2:
                        if valg == "Fattige studenter":
                            nivå = 3
                            pos = 1
                            aktiv = meny[nivå]
                            tegn_meny(pos, aktiv)
                        else:
                            valgt_mottaker = valg
                            nivå = 4
                            pos = 1
                            aktiv = meny[nivå]
                            tegn_meny(pos, aktiv)

                    elif nivå == 3:
                        valgt_mottaker = valg
                        nivå = 4
                        pos = 1
                        aktiv = meny[nivå]
                        tegn_meny(pos, aktiv)

                    elif nivå == 4:
                        ev3.screen.clear()
                        if valg == "Vipps":
                            nummer = vipps_numre.get(valgt_mottaker, "Ukjent")
                            ev3.screen.print(nummer)
                            wait(2000)
                            ev3.screen.print("Klikk på rød knapp")
                            wait(1000)
                            ev3.screen.print("når du er ferdig.")
                            wait(2000)
                            vent = True
                            while vent == True:
                                if knapp.pressed():
                                    ev3.screen.clear()
                                    ev3.screen.print("Takk for bidraget!")
                                    wait(2000)
                                    for f in Glad:
                                        ev3.screen.load_image(f)
                                        wait(140)
                                        wait(2000)
                                    vent = False
                                    hindring()
                                    break
                                else: 
                                    wait(20)
                            
                        else:
                            
                            ev3.screen.print("Legg kontanter")
                            ev3.screen.print("i boksen.")
                            wait(5000)
                            ev3.screen.clear()
                            ev3.screen.print("Trykk den røde")
                            ev3.screen.print("knappen for å")
                            ev3.screen.print("bekrefte.")
                            vent = True
                            while vent:
                                if knapp.pressed():
                                    ev3.screen.clear()
                                    ev3.screen.print("Takk for bidraget!")
                                    wait(2000)
                                    for f in Glad:
                                        ev3.screen.load_image(f)
                                        wait(140)
                                        wait(2000)
                                    vent = False
                                    hindring()
                                    break
                        break  

                    wait(500)
            #knappStatus = False
            #ev3.screen.print("Vil du donere?")
            #wait(200)
        
        else:

            robot.drive(100,0)
               