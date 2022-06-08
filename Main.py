
"""         FtpZabbixAgent        - Main File -        'Main.py'         """
"""     Este aplicativo realiza a monitoração de um storage Nexios e dispara um aviso no Zabbix em caso de pouco espaço em disco    """
# Storage nexio possui 11 discos de 146GB = 1606 GB


"""     INFORMAÇÕES DO DESENVOLVEDOR    """

__author__ = "Cristian Ritter"
__copyright__ = "EngNSC 2022"
__credits__ = ["",]
__license__ = "GPL"
__version__ = "v1.0.0"
__maintainer__ = "Cristian Ritter"
__email__ = "cristianritter@gmail.com"
__status__ = "Production" 


"""     REQUIREMENTS     """

import wx                                                       # Suporte a interface gráfica de usuário
import ftplib                                                   # Suporte à conexão FTP
from LibParseConfig import ConfPacket                           # Suporte ao import de configurações do arquivo ini
from LibZabbixSender import WRZabbixSender                      # Suporte ao envio de métricas para o Zabbix
from time import sleep                                          # Suporte ao atraso de programa
from LibTaskBar import TaskBarIcon                              # Suporte ao ícone de bandeja
from threading import Thread
from LibWXInitLlocaleFix import InitLocale as InitLocaleFix
wx.App.InitLocale = InitLocaleFix                               # Substituição do método padrao que gera um erro no idioma PT-BR no Windows 10


"""     PARSING DO ARQUIVO DE CONFIGURAÇÕES     """

configs = ConfPacket()
parsed_config = configs.load_config('storage, ftp, zabbix')


"""     INICIALIZAÇÃO DA THREAD DE ENVIO DAS MÉTRICAS PARA O ZABBIX     """

zabbix_data = [1]
zsender = WRZabbixSender(parsed_config['zabbix']['send_metrics_interval'], parsed_config['zabbix']['hostname'], 
                         parsed_config['zabbix']['key'], parsed_config['zabbix']['zabbix_server'], parsed_config['zabbix']['port'], 
                         0, zabbix_data )
zsender.start_zabbix_thread()


"""     DEFINIÇÃO DE FUNÇÕES    """

def get_files_size_sum():
    """ Acessa o servidor FTP, executa um comando dir, recebe os resultados, soma o tamanho dos arquivos e retorna seu tamanho total em GB """
    ftp = ftplib.FTP()                                              # Criando uma nova conexão
    ftp.connect(parsed_config['ftp']['server'], int(parsed_config['ftp']['port']))                               # Configurando IP e Porta do Server
    ftp.login(parsed_config['ftp']['user'], parsed_config['ftp']['pass'])                       # Executando login no servidor
    data = []
    ftp.dir(data.append)                                            # Recebendo dados do comando dir na pasta raiz do servidor
    ftp.quit()                                                      # Encerrando a conexão
    tamanho_total = 0.0
    for line in data:                                               # Trabalhando nos dados recebidos
        linha_separada = line.split()                               # Convertendo o texto em uma lista cujo indice 4 é o tamanho do arquivo
        tamanho_total += (float(linha_separada[4])/(1024*1024))     # Somando o tamanho de todos os arquivos presentes no servidor em MBs
    tamanho_total_gb = round(tamanho_total/1024, 2)
    return tamanho_total_gb

def LoopPrincipal():
    while(True):                                                                        # Loop infinito
        tamanhoGB = get_files_size_sum()                                                # Get soma do tamanho total de arquivos no storage
        zabbix_data[0] = tamanhoGB / float(parsed_config['storage']['size_gb'])         # Salva dados no ponteiro de envio para zabbix
        sleep(int(parsed_config['zabbix']['send_metrics_interval']))                    # Tempo de espera entre as métricas
    
t = Thread(target=LoopPrincipal, daemon=True)                       # Criação de thread de processo paraleo
t.start()                                                           # Start do processo paralelo

app = wx.App()   #criação da interface gráfica
TaskBarIcon(f"FTPZabbixAgent") 

app.MainLoop()