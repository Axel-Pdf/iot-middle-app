from models import InicializadorPubnub, ChamadaDeAssinatura, ChamadaTrataDisconexao,\
 Publicador, Assinante, Registrador
import shlex, time, sys


class Console:
    
    pubnub = None
    monitor = None
    publicador = None
    registra = None
    
    def __init__(self, chave_assinatura, chave_publicacao):
        self.pubnub = InicializadorPubnub(chave_assinatura, chave_publicacao).inicializador()
        

    def prefix(self):
        return '\ntask> '

    def waitCommand(self):
        comm = input(self.prefix())
        comm = comm.strip()
        return comm

    def start(self):
        print('== Controlador de Comunicações de Dispositivos IoT ==')
        print('.. Console de comando inicializado ..')
        print('.. Digite um comando, "help" para obter o painel de comando, ou "encerra" para encerrar')
        

    def parseCommand(self, comm):
        if comm.startswith(('help','?', '--help')):
            print('\n::.. Lista de comandos / Usando o app ..::')
            comandos = [
                '\thelp ou --help ou ?      - Esta tela de ajuda!',
                '\texit ou quit ou sair     - Finaliza o aplicativo',
                '\tconectar_canal           - Conecta a canal de comunicação (digitar: canal)',
                '\tpublica_mensagem         - Publica mensagem em canal conectada (digitar: canal mensagem [máximo: 5 palavras])',
                '\tobter_log                - Obtém log de comunicações de canal (digitar: canal num_registros)',
                '\tdesconectar              - Desconecta de canal de comunicação (digitar: canal)',
                '\tencerra                  - Encerra aplicativo'
            ]

            for item in comandos:
                print(item)

        elif comm.startswith('conectar_canal'):
            # verifica os demais argumentos, separados por espaço
            try:
                args = shlex.split(comm)
                if len(args) !=  2:
                    print('[Aviso] Verifique a sintaxe com comando: help')
                else:

                    canal = args[1]
                    
                    try:
                        self.monitor = Assinante(canal)
                        self.monitor.assina_canal(self.pubnub, canal)
                        print("Monitorando canal de comunicacao:", canal)
                    except:
                        print("Erro ao conectar a canal: ", canal)

            except ValueError as v:
                if str(v) == 'No closing quotation':
                    print('[Aviso] Verifique as aspas duplas')

        elif comm.startswith('publica_mensagem'):
            # verifica os demais argumentos, separados por espaço
            try:
                args = shlex.split(comm)
                if len(args) > 6 or len(args) < 3 :
                    print('[Aviso] Verifique a sintaxe com comando: help')
                else:
                    
                    canal = args[1]
                    mensagem = str(args[2:])
                    
                    try:
                        self.publicador = Publicador()
                        self.publicador.publica_mensagem(self.pubnub, canal, mensagem)
                        print("Mensagem", mensagem, " publicada no canal", canal)
                    except:
                        print("Falha ao enviar mensagem a dispositivos")               

            except ValueError as v:
                if str(v) == 'No closing quotation':
                    print('[Aviso] Verifique as aspas duplas')



        elif comm.startswith('obter_log'):
           
             # verifica os demais argumentos, separados por espaço
            try:
                args = shlex.split(comm)
                if len(args) < 3:
                    print('[Aviso] Verifique a sintaxe com comando: help')
                else:
                    
                    canal = args[1]
                    num_registros = int(args[2])
                    try:
                        if self.publicador == None:
                            self.publicador = Publicador()                            
                        registros_obtidos = self.publicador.resgata_registro(self.pubnub, canal, num_registros)
                        try:
                            self.registra = Registrador()
                            self.registra.registra_fluxo(canal, registros_obtidos)
                            print(registros_obtidos)
                        except:
                            print("Falha ao registrar dados em base")
                            print("Registros obtidos do canal", canal, "registrados em base de dados")
                            print(registros_obtidos) 
                    except:
                        print("Falha ao obter registros")               

            except ValueError as v:
                if str(v) == 'No closing quotation':
                    print('[Aviso] Verifique as aspas duplas')
            
            
        elif comm.startswith('desconectar'):
            try:
                args = shlex.split(comm)
                if len(args) != 2:
                    print('[Aviso] Verifique a sintaxe com comando: help')
                else:
                    canal = args[1]
                    
                    try:
                        self.monitor.remove_assinatura(self.pubnub, canal)
                        print("Não mais conectado ao canal", canal)
                    except:
                        print("Falha ao desconectar")

            except ValueError as v:
                if str(v) == 'No closing quotation':
                    print('[Aviso] Verifique as aspas duplas')

        elif comm.startswith('encerra'):
            try:
                args = shlex.split(comm)
                if len(args) < 1:
                    print('[Aviso] Verifique a sintaxe com comando: help')
                else:
                    
                    if self.pubnub != None:
                        del self.pubnub
                    if self.monitor != None:
                        del self.monitor
                    if self.publicador != None:
                        del self.publicador
                    if self.registra != None:
                        del self.registra
                    print("Sessão encerrada")
                    time.sleep(0.5)
                    sys.exit()


            except ValueError as v:
                if str(v) == 'No closing quotation':
                    print('[Aviso] Verifique as aspas duplas')

        elif comm.startswith('amigos_comuns'):
            try:
                args = shlex.split(comm)
                if len(args) < 3:
                    print('[Aviso] Verifique a sintaxe com comando: help')
                else:

                    pass

            except ValueError as v:
                if str(v) == 'No closing quotation':
                    print('[Aviso] Verifique as aspas duplas')



        elif comm.startswith('imprime'):
            try:
                args = shlex.split(comm)
                if len(args) >1:
                    print('[Aviso] Verifique a sintaxe com comando: help')
                else:
                     pass

            except ValueError as v:
                if str(v) == 'No closing quotation':
                    print('[Aviso] Verifique as aspas duplas')


        else:
            print('Não entendi... Melhor digitar: help')
          
            
    def startConsole(self):
        self.start()
        while True:
            comando = self.waitCommand()
            self.parseCommand(comando)
            
            