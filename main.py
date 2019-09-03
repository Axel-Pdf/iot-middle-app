from models import InicializadorPubnub, ChamadaDeAssinatura, ChamadaTrataDisconexao,\
 Publicador, Assinante, Registrador
import time
import datetime




def iniciarMiddle(chave_sub, chave_pub):
    
    pubnub = InicializadorPubnub(chave_sub, chave_pub).inicializador()
    monitor = None
    publicador = None
    registra = None
    
    print("API Inicializada. Não conectado a nenhum canal no momento")
    time.sleep(2)
    while True:
        opcao = int(input("""Para efetuar operacões, digite um dos comandos numericos:  
                          1 - Monitorar fluxo de dados; 
                          2 - Publicar mensagem para dispositivos; 
                          3 - Obter log de comunicação 
                          4 - Desconectar
                          5 - Encerrar
                          : """))
        
        if opcao == 1:
            canal = input("Insira o canal que deseja monitorar: ")
            try:
                monitor = Assinante(canal)
                monitor.assina_canal(pubnub, canal)
                print("Monitorando canal de comunicacao:", canal)
            
            except:
                print("Erro ao conectar a canal: ", canal)
                
        elif opcao == 2:
            canal = input("Insira o canal em que deseja publicar: ")
            time.sleep(0.5)
            mensagem = str(input("Insira a mensagem a ser publicada aos dispositivos: "))
         
            try:
                publicador = Publicador()
                publicador.publica_mensagem(pubnub, canal, mensagem)
                print("Mensagem", mensagem, " publicada no canal", canal)
            except:
                print("Falha ao enviar mensagem a dispositivos")
        
        elif opcao == 3:
            
            canal_ref = str(input("Insira o canal de que quer obter registros: "))
            num_registros = int(input("Insira o número de registros que deseja obter: "))
            
            try:
                publicador = Publicador()
                registros_obtidos = publicador.resgata_registro(pubnub, canal_ref, num_registros)
                registros_obtidos = registros_obtidos[1]
                try:
                    registra = Registrador()
                    registra.registra_dados(canal_ref, registros_obtidos)
                except:
                    print("Falha ao registrar dados em base")
                    print("Registros obtidos do canal", canal, "registrados em base de dados")
                    print(registros_obtidos)
            except:
                print("Falha ao obter registros")
        
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
            del registra
            print("Sessão encerrada")
            time.sleep(0.5)
            break
        else:
            print("Opção inválida")
            
        