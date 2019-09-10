# -*- coding: utf-8 -*-

import models as md
import random, time





pubnub = md.InicializadorPubnub('sub-c-c52c96a4-3f6c-11e9-978c-aae2bd4c3b77', 'pub-c-3d596091-11f9-4424-9796-7a67018f578d').inicializador()
publicador = md.Publicador()

def publicaTemp(canal, num_leituras):
    
    for i in range(num_leituras):
        temperatura = round(random.uniform(0, 100), 2)
        
        publicador.publica_mensagem(pubnub, canal, str(temperatura))
        time.sleep(0.5)
    




num_reg = int(input("Entre o número de registros aleatórios a lançar: "))
cnl_name = input("Entre o nome do canal: ")
#time.sleep(3)
print("Registrando no canal...")
publicaTemp(cnl_name, num_reg)
