from models import InicializadorPubnub, ChamadaDeAssinatura, ChamadaTrataDisconexao, Publicador, Assinante
import time
import datetime




def iniciarMiddle(chave_sub, chave_pub):
    
    pubnub = InicializadorPubnub(chave_sub, chave_pub).inicializador()
    monitor = Assinante()
    publicador = Publicador()
    
    print("API Inicializada. Não conectado a nenhum canal no momento")
    time.sleep(2)
    while True:
        opcao = int(input("Para efetuar operacões, digite um dos comandos numericos: ", 
                          "1 - Monitorar fluxo de dados;", 
                          "2 - Publicar mensagem para dispositivos;", 
                          "3 - Obter log de comunicação", 
                          "4 - Desconectar"
                          "5 - Encerrar"))
        
        if opcao == 1:
            canal = input("Insira o canal que deseja monitorar: ")
            try:
                monitor.assina_canal(pubnub, canal)
                print("Monitorando canal de comunicacao:", canal)
            
            except:
                print("Erro ao conectar a canal: ", canal)
                
        elif opcao == 2:
            canal = input("Insira o canal em que deseja publicar: ")
            time.sleep(0.5)
            mensagem = input("Insira a mensagem a ser publicada aos dispositivos: ")
            try:
                publicador.publica_mensagem(canal, mensagem, pubnub)
                print("Mensagem publicada")
            except:
                print("Falha ao enviar mensagem a dispositivos")
        
        elif opcao == 3:
            pass
        
        elif opcao == 4:
            canal = input("Desconectar de que canal? ")
            try:
                monitor.remove_assinatura(pubnub, canal)
                print("Não mais monitorando canal ", canal)
            except:
                print("Falha ao desconectar")
                
        elif opcao == 5:
            del pubnub
            del monitor
            del publicador
            print("Sessão encerrada")
            time.sleep(0.5)
            break
        else:
            print("Opção inválida")