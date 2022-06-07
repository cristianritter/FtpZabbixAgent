"""         FitBox PRO        - TaskBar (Local Lib) -        'LibTaskBar.py'         """
"""     Criação de um icone de bandeja      """


"""     INFORMAÇÕES DO DESENVOLVEDOR    """

__author__ = "Cristian Ritter"
__license__ = "GPL"
__email__ = "cristianritter@gmail.com"


"""     REQUIREMENTS     """

import wx                                       # Interface do usuário
import os                                       # Suporte a rotinas e métodos do sistema operacional
import wx.adv

"""     DEFINIÇÕES DE CLASSES    """

class TaskBarIcon(wx.adv.TaskBarIcon):
    """
    Criacao de um icone na bandeja do systema para controle do aplicativo, e existencia no tray do sistema
    """

    def __init__(self, prog_name, ):
        """
        Funcao que inicializa o tray do sistema \n  
        """
        super(TaskBarIcon, self).__init__()
        
        self.TRAY_TOOLTIP = prog_name
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) # This is your Project Root
        task_icon = os.path.join(ROOT_DIR, 'zabbix-icon.png')          
        self.SetIcon(wx.Icon(task_icon), self.TRAY_TOOLTIP)

        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DOWN, self.on_left_down) #funcao que define o metodo de clique esquerdo no trayicon

    def create_menu_item(self, menu, label, func):
            item = wx.MenuItem(menu, -1, label)
            menu.Bind(wx.EVT_MENU, func, id=item.GetId())
            menu.Append(item)
            return item

    def CreatePopupMenu(self):
        menu = wx.Menu()
        #for name in self.CONFIGS.keys():
            # definindo metodos para cada submenu criado, funcao lambda permite enviar parametros especificos para cada submenu
        #    self.create_menu_item(menu, f'View {self.NAMES[name]}', lambda evt, temp=name: self.on_right_down(evt, temp)) 
        
        menu.AppendSeparator()
        self.create_menu_item(menu, 'Fechar a aplicação', self.on_exit) #on exit program clique
        menu.AppendSeparator()
        self.create_menu_item(menu, 'Sobre', self.on_get_info) #apresentacao de informacoes sobre o desenvolvedor
        return menu

    def on_left_down(self, event): 
        """
        Metodo executado ao clicar com o botao esquerdo
        """
        self.frame.Show()
        self.frame.Raise()
        self.frame.notebook.SetSelection(1)  #seleciona a tab selecionada
      
    def on_right_down(self, event, tab):
        """
        Metodo executado ao clicar com o botao direito em submenus\n
        button_label recebe a tab especifica de cada submenu 
        """
        self.frame.Show()
        for idx, name in enumerate(self.NAMES):
            if name == tab:
                self.frame.notebook.SetSelection(idx)  #seleciona a tab selecionada
      
    def on_exit(self, event):
        wx.CallAfter(self.Destroy)
     
    def on_get_info(self, event):
        wx.MessageBox("Zabbix Agent para monitoração do espaço utilizado no storage Nexios. Configurações podem ser feitas no arquivo config.ini. Feito por Cristian Ritter", 'Sobre o aplicativo')


"""     Se o arquivo for chamado diretamente roda este trecho    
        Permite testar a biblioteca individualmente e fornece também exemplos de uso.
"""
if __name__ == '__main__':
    pass
