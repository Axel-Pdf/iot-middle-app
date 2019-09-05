# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 07:28:17 2019

@author: apdde / mb

Funções de Subscribe e Publish
"""


from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory, PNOperationType
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub, SubscribeListener
from pubnub.exceptions import PubNubException

class InicializadorPubnub(PubNub):
    chave_inscricao = "chave_para_incricao"
    chave_publicacao = "chave_para_publicacao"
    uuid = 'identificador_dispositivo'
    
    def __init__(self, chave_inscricao, chave_publicacao, uuid = ''):
        self.chave_inscricao = chave_inscricao
        self.chave_publicacao = chave_publicacao
        self.uuid = uuid
        
    def inicializador(self, ssl = False):
        pnconfig = PNConfiguration()
        pnconfig.subscribe_key = self.chave_inscricao
        pnconfig.publish_key = self.chave_publicacao
        pnconfig.ssl = ssl
        
        pubnub = PubNub(pnconfig)
        
        return pubnub
    
    def chamada_publicacao(envelope, status):
        #Confere se pedido foi completado
        
        if not status.is_error():
            pass 
            #Mensagem publicada
        else:
            pass
            #mensagem falhou publicacao
            #pedido falhou
            #pode ser repetida com [status retry]
            #tratar erros aqui
            
def subscribe_callback(envelope, status):
    if not status.is_error():
        pass
    else:
        pass
        
        
class ChamadaDeAssinatura(SubscribeCallback):
    
    def presenca(self, pubnub, presence):
        pass
        #tratar de dados de presenca de dispositivo
        
    def message(self, pubnub, message):
        pass #trata novas mensagens localizadas em message.message
        
    def sinal(self, pubnub, signal):
        pass
        #tratar sinais de entrada

        
    def status(self, pubnub, status):
        
        if status.operation == PNOperationType.PNSubscribeOperation \
            or status.operation == PNOperationType.PNUnsubscribeOperation:
            
             if status.category == PNStatusCategory.PNConnectedCategory:
                pass
                # inscrissão ao canal de comunicacao ocorreu normalmente
             elif status.category == PNStatusCategory.PNReconnectedCategory:
                 pass
                # Significa que ocorreu um erro de conexao mas que ja foi restabelecida
             elif status.category == PNStatusCategory.PNDisconnectedCategory:
                 pass
                # Ocorre quando se desfaz a inscricao a um canal de comunicacao
                # Dispositivo/interface para de receber mensagens
             elif status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
                 pass
                # Geralmente, erro com a internet. Tende a tentar reconectar automaticamente
             elif status.category == PNStatusCategory.PNAccessDeniedCategory:
                 pass
                # conexao nao permitida
             else:
                 pass
                # Erro com conexao de internet
        elif status.operation == PNOperationType.PNSubscribeOperation:
            # Heartbeat operations can in fact have errors, so it is important to check first for an error.
            # For more information on how to configure heartbeat notifications through the status
            # PNObjectEventListener callback, consult http://www.pubnub.com/docs/python/api-reference-configuration#configuration
            if status.is_error():
                pass
                # There was an error with the heartbeat operation, handle here
            else:
                pass
                # Heartbeat operation was successful
        else:
            pass
            # Encountered unknown status type
        
#Lidando com desconexoes
class ChamadaTrataDisconexao(SubscribeCallback):
    def status(self, pubnub, status):
        if status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
            #internet caiu / perdida. Tratar e reconectar
            pubnub.reconect()
        elif status.category == PNStatusCategory.PNTimeoutCategory:
            # timeout na tentativa de comunicacao. Tratar e reconectar
            
            pubnub.reconect()
        else:
            pubnub.logger.debug(status)
            
    def presence(self, pubnub, presence):
        pass
  
    def message(self, pubnub, message):
        pass
 
    def signal(self, pubnub, signal):
        pass

        
class Ouvinte(SubscribeCallback):
    
   def status(self, pubnub, status):
        if status.category == PNStatusCategory.PNConnectedCategory:
            pubnub.publish().channel("").message({}).sync()
 
   def message(self, pubnub, message):
       pass
 
   def presence(self, pubnub, presence):
       pass
   
     
class Publicador(SubscribeCallback):
    
   
    def publica_mensagem(self, pubnub, canal, mensagem):
        
        
        try:
            pubnub.publish().channel(canal).message(mensagem).pn_async(subscribe_callback)
            #print("Timetoken de publicação: %d", envelope.result.timetoken)
        except PubNubException as e:
            # Tratar falhas na publicacao
            #handle_exception(e)
            print(e.status)
            
    def resgata_registro(self, pubnub, canal, num_registros):
        
        resposta = []
        
        envelope = pubnub.history().channel(canal).count(num_registros).sync()
        dados = envelope.result.messages
        for item in dados:
            item = str(item)
            item = item[39:]
            
            resposta.append(item)
            
        return resposta
   
         
class Assinante(SubscribeCallback):
    
    assinante = None
    
    def __init__(self, canal):
        
        self.assinante = Ouvinte()
        
    def adiciona_ouvinte(self, pubnub):
        pubnub.add_listener(self.assinante)
        
    
    def assina_canal(self, pubnub, canal):
        
        pubnub.subscribe().channels(canal).execute()
        #self.assinante.wait_for_connect()
        print('Conectado')
        
    def remove_assinatura(self, pubnub, canal):
        pubnub.unsubscribe().channels(canal).execute()
        #self.assinante.wait_for_disconnect()
        print('Desconectado')
        
class Registrador():
    import firebase
#    import firebase_admin
#    from firebase_admin import credentials
#    from firebase_admin import firestore
    import datetime
    
   
  
          
    def registra_fluxo(self, canal, dados):
        
        base = self.firebase.firebase.FirebaseApplication('https://iot-middle-app.firebaseio.com/') 
        base_nome = 'iot-middle-app/' + canal
              
        for item in dados:          
            base.post(base_nome, item)
            


#
#pnconfig = PNConfiguration()
#pnconfig.subscribe_key = 'sub-c-c52c96a4-3f6c-11e9-978c-aae2bd4c3b77'
#pnconfig.publish_key = 'pub-c-3d596091-11f9-4424-9796-7a67018f578d'
#
#        
#pubnub = PubNub(pnconfig)            
##    
##
#envelope = pubnub.history().channel('canal_teste').count(5).sync()
#value = envelope.result.messages.__str__
#
#print(value)
#
#for item in value:
#    item = str(item)
#    item = item[39:]
#    print(item)
#    




#
##    
#publicador = Publicador()
#envelope = publicador.resgata_registro(pubnub, 'canal_teste', 3)    
#print(type(envelope))    