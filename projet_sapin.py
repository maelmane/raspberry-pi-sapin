import RPi.GPIO as GPIO
import time
import i2c_lcd_driver
import dht11

r_pin = 18 	#pin GPIO pour la couleur rouge de la RGB LED
v_pin = 24 	#pin GPIO pour la couleur verte de la RGB LED
b_pin = 23 	#pin GPIO pour la couleur bleu de la RGB LED
buzzer = 12 #pin GPIO pour l'active buzzer
btn = 26 	#pin GPIO pour le bouton

humiture = dht11.DHT11(pin=17) 	#instance du humiture sensor 
mylcd = i2c_lcd_driver.lcd()	#instance de l'écran LCD

GPIO.setwarnings(False)	#enlever les avertissements 
GPIO.setmode(GPIO.BCM)	#mettre le mode de numérotation des pins en BROADCOM

#Mise en place de la RGB LED
GPIO.setup(r_pin, GPIO.OUT)
GPIO.setup(v_pin, GPIO.OUT)
GPIO.setup(b_pin, GPIO.OUT)

#Mise en place du buzzer
GPIO.setup(buzzer, GPIO.OUT)
GPIO.output(buzzer, GPIO.HIGH)

#Mise en place du bouton
GPIO.setup(btn, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


#Allumer la RGB LED rouge
def rouge():
    GPIO.output(r_pin, GPIO.LOW)
    GPIO.output(v_pin, GPIO.HIGH)
    GPIO.output(b_pin, GPIO.HIGH)

#Allumer la RGB LED blanc
def blanc():
    GPIO.output(r_pin, GPIO.LOW)
    GPIO.output(v_pin, GPIO.LOW)
    GPIO.output(b_pin, GPIO.LOW)

#Allumer la RGB LED vert
def vert():
    GPIO.output(r_pin, GPIO.HIGH)
    GPIO.output(v_pin, GPIO.LOW)
    GPIO.output(b_pin, GPIO.HIGH)
    
def led_off():
    GPIO.output(r_pin, GPIO.HIGH)
    GPIO.output(v_pin, GPIO.HIGH)
    GPIO.output(b_pin, GPIO.HIGH)

#Alterner la couleur de la RGB LED aux couleurs de Noël
def noel():
    mylcd.lcd_display_string("Joyeux Noel      ", 1)
    vert()
    time.sleep(1)
    blanc()
    time.sleep(1)
    rouge()
    time.sleep(1)
    vert()

#Activer le son du active buzzer
def buzzer_on():
    GPIO.output(buzzer, GPIO.LOW)

#Fermer le son du active buzzer
def buzzer_off():
    GPIO.output(buzzer, GPIO.HIGH)

#Faire que l'active buzzer beep (pernant en paramètre le nombre de secondes entre les beeps)
def beep(x):
    buzzer_on()
    time.sleep(x)
    buzzer_off()
    time.sleep(x)

#Faire flash la RGB LED rouge (pernant en paramètre le nombre de secondes entre les flashs de lumières)
def led_alerte(x):
    rouge()
    time.sleep(x)
    led_off()
    time.sleep(x)

#Afficher le message ALERTE à l'utilisateur et fait rententir l'active buzzer et la RGB LED rouge
def alarme():
    beep(0.5)
    led_alerte(0.5)
    mylcd.lcd_display_string("ALERTE! ALERTE!", 1)

#Fermer tout
def fermer():
    led_off()
    buzzer_off()
    mylcd.lcd_display_string("                        ", 1)
    mylcd.lcd_display_string("                        ", 2)
    

#Fonction appeler lorsque le bouton est pousser
def button_callback(channel):
    while True:
        result = humiture.read()
        if result.is_valid():
            mylcd.lcd_display_string(str(result.temperature)+ " C", 2)
            
            #si la température est plus petite ou égale à 25C la fonction noel() est appelée
            if ( 25 >= result.temperature ): 
                noel()
            #si la température est plus grande que 25C mais plus petite que 28C la fonction alarme() est appelée
            if ( result.temperature >  25 and result.temperature < 28):
                alarme()
            
            #si la température est plus grande ou égale à 28C la fonction fermer() est appelée
            if ( result.temperature >=  28):
                fermer()

#Ajouter une détection d'événement lorsque le bouton est pousser
GPIO.add_event_detect(26,GPIO.RISING,callback=button_callback)

