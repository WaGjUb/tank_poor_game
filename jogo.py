import curses
import curses.textpad
import Pyro4
from threading import Thread
import time


jglobal = None
@Pyro4.expose
class teste(object):
    def t(self):
        return "Testado"

#se x for enter então retorna ctrl+g = terminate
def backspace(x):
    if x == 127:
        return 263
    return x

#Classe responsavel pelo servidor
class servidor(object):
    def __init__(self, janela):
        self.ip = "localhost"
        self.porta = "5388"
        self.executando = ""
        self.j = janela
        self.j.cursy += 2
        self.j.cursx = 0
    def imprime(self):
        self.j.positions = []
        self.j.screen.addstr(self.j.cy, 0, self.j.labels['l_ip'][0]+': '+self.ip)
        self.j.positions.append((self.set_ip, (0, self.j.x), (self.j.cy, self.j.cy)))
        self.j.screen.addstr(self.j.cy-1, 0, self.j.labels['l_port'][0]+": "+self.porta)
        self.j.positions.append((self.set_port, (0, self.j.x), (self.j.cy-1, self.j.cy-1)))
        self.j.screen.addstr(self.j.cy+2, 0, self.j.labels['l_client'][0])
        self.j.positions.append((cliente, (0, len(self.j.labels['l_client'][0])-1), (self.j.cy+2, self.j.cy+2)))
        self.j.screen.addstr(self.j.cy+2, len(self.j.labels['l_client'][0])+1, self.j.labels['l_start'][0]+' '+self.executando)
        inx = len(self.j.labels['l_client'][0])+1
        self.j.positions.append((self.start, (inx, inx +len(self.j.labels['l_start'][0])), (self.j.cy+2, self.j.cy+2)))
        self.j.screen.move(self.j.cursy, self.j.cursx)

    def start(self):

        Thread(target=self.create_server).start()
        self.executando = self.j.labels['l_ok'][0]
    
    def create_server(self):
        daemon = Pyro4.Daemon() 
        ns = Pyro4.locateNS()
        uri = daemon.register(jogo) #TODO mudar a função
        ns.register("example.greeting", uri)
        daemon.requestLoop()

    def set_ip(self):
        win = curses.newwin(1, 20, self.j.y-1, 0)
        tb = curses.textpad.Textbox(win, insert_mode=True)
        text = tb.edit(backspace)
        curses.flash()
        win.clear()
        win.addstr(0, 0, text.encode('utf-8'))
        win.refresh()
        self.ip = text

    def set_port(self, par=None):
        win = curses.newwin(1, 20, 0, 0)
        tb = curses.textpad.Textbox(win, insert_mode=True)
        text = tb.edit(self.backspace)
        curses.flash()
        win.clear()
        win.addstr(0, 0, text.encode('utf-8'))
        win.refresh()
        self.port = text

#classe responsavel pelo cliente
class cliente(object):
    def __init__(self, janela):
        self.ip = "localhost"
        self.porta = "5388"
        self.nickname = "default"
        self.j = janela
        self.j.cursx = 0
    def imprime(self):
        self.j.positions = []
        self.j.screen.addstr(self.j.cy, 0, self.j.labels['l_ip'][0]+': '+self.ip)
        self.j.positions.append((self.set_ip, (0, self.j.x), (self.j.cy, self.j.cy)))
        self.j.screen.addstr(self.j.cy-1, 0, self.j.labels['l_port'][0]+": "+self.porta)
        self.j.positions.append((self.set_port, (0, self.j.x), (self.j.cy-1, self.j.cy-1)))

        self.j.screen.addstr(self.j.cy-2, 0, self.j.labels['l_nickname'][0]+": "+self.nickname)
        self.j.positions.append((self.set_nickname, (0, self.j.x), (self.j.cy-2, self.j.cy-2)))
        self.j.screen.addstr(self.j.cy+2, 0, self.j.labels['l_connect'][0])
        self.j.positions.append((self.connect, (0, self.j.x), (self.j.cy+2, self.j.cy+2)))
        self.j.screen.move(self.j.cursy, self.j.cursx)

    def connect(self):
        jog = Pyro4.Proxy("PYRONAME:example.greeting") 
      #  my_p = player(self.nickname)
       # jog.__init__(self.j)

#        jog = jogo()
 #       jog.player_enter(self.nickname)
  #      jog.player_enter("oalr")
        exec(jog, self.nickname)
        
    def set_nickname(self):
        win = curses.newwin(1, 20, self.j.y-1, 0)
        tb = curses.textpad.Textbox(win, insert_mode=True)
        text = tb.edit(backspace)
        curses.flash()
        win.clear()
        win.addstr(0, 0, text.encode('utf-8'))
        win.refresh()
        self.nickname = text

    def set_ip(self):
        win = curses.newwin(1, 20, self.j.y-1, 0)
        tb = curses.textpad.Textbox(win, insert_mode=True)
        text = tb.edit(backspace)
        curses.flash()
        win.clear()
        win.addstr(0, 0, text.encode('utf-8'))
        win.refresh()
        self.ip = text

    def set_port(self, par=None):
        win = curses.newwin(1, 20, 0, 0)
        tb = curses.textpad.Textbox(win, insert_mode=True)
        text = tb.edit(self.backspace)
        curses.flash()
        win.clear()
        win.addstr(0, 0, text.encode('utf-8'))
        win.refresh()
        self.port = text

#Classe responsavel pela renderização e manipulação dos elementos da tela
class janela(object):
    # Define janela, o tamanho da janela, posição do cursor
    def __init__(self, screen,x, y, cursx, cursy):
        self.barsize = 2 #tamanho dos menus
        self.screen = screen
        self.x = x
        self.y = y
        self.cursx = cursx
        self.cursy = cursy 
        self.cy = (self.y//2) - self.barsize
        self.labels = {}
        self.set_labels()
        self.positions = []
        self.gamepos = {}
        self.screen.nodelay(True)
    #Cria os labels do arquivo ("label", cx)
    def centerfy(self):
        self.cursx = self.x//2

        self.cursy =self.y//2
        return (self.cursx, self.cursy)

    def set_labels(self):
        f = open("./labels.lb").read().splitlines()
        for l in f:
            l = l.split()
            self.labels[l[0]] = (l[1], self.cx(l[1]))

    #retorna a posição para centralizar em x
    def cx(self,label):
        return (self.x//2) - (len(label)//2) - (len(label) % 2)

    #imprime menu
    def imprime(self):
        self.positions = []
        self.screen.addstr(self.cy, self.labels['l_client'][1], self.labels['l_client'][0])
        self.positions.append((cliente, (0, self.x), (self.cy, self.cy)))
        self.screen.addstr(self.cy-2,self.labels['l_server'][1],self.labels['l_server'][0])
        self.positions.append((servidor, (0, self.x), (self.cy-2, self.cy-2)))
        self.screen.move(self.cursy, self.cursx)
    def get_key(self):
        return(self.screen.getch())

    def move_cursx(self,d):
        if d > 0:
            self.cursx += 1
        if d < 0:
            self.cursx -= 1

        self.cursx = max(0,self.cursx)
        self.cursx = min(self.x-1, self.cursx)

    def move_cursy(self,d):
        if d > 0:
            self.cursy += 1
        if d < 0:
            self.cursy -= 1

        self.cursy = max(0,self.cursy)
        self.cursy = min(self.y-1, self.cursy)

    ##verifica se o cursor está em colisão
    ##x_int e y_int são tuplas (min, max)
    def colision(self):
        for i in self.positions:
        
            y_int = i[2]
            x_int = i[1]
            x = self.cursx 
            y = self.cursy 
            if ((x <= x_int[1]) and (x >= x_int[0]) and (y <= y_int[1]) and (y >= y_int[0])):
                return (True,i[0])
        return (False, '')



#Informações do jogador
@Pyro4.expose
class player(object):
    def __init__(self, nickname):
        self.nickname = nickname
        self.score = 0
        self.won = 0
        self.cursorx = None
        self.cursory = None
        self.lifes = 3

    def set_cursor(self, pos, numplay, y):
        self.cursorx = pos[0]
        if numplay == 1:
            self.cursory = (y-2)
        elif numplay == 2:
            self.cursory = 1

    def up_won(self):
        self.won += 1
        return self.won
    def up_score(self):
        self.score += 100

##Gerenciador do jogo no cliente
@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class jogo(object):
    def __init__(self):
        global jglobal
        self.players = {}
        self.bullets = []
        self.j = jglobal
        self.win = True
        self.round = 0
        self.velocidade = 0.04
        Thread(target=self.manager).start()
        '''
        while self.win:
            if self.players == 2:
                c = self.gamecolision()
                if c[0]:
                    self.players[c[1]].lifes -= 1
                    self.players[c[2]].up_score()
                    if self.playes[c[1]].lifes == 0:
                        if (self.players[c[2]].up_won() == 3):
                            break
        '''

    def ret(self, s):
        return eval("self."+s)

    def manager(self):
        while self.win:
            for i in self.bullets:
                if i[4] == 'p' and (time.time() - i[3]) > self.velocidade:
                    i[2] += 1
                    i[3] = time.time()
                elif i[4] == 'm' and (time.time() - i[3]) > self.velocidade:
                    i[2] -= 1
                    i[3] = time.time()
                if i[2] >= self.j.y-1 or i[2] <= 1:
                    #TODO setar os valores para y e verificar colisão aqui
                    g = self.gamecolision()
                    if (g[0]):
                        g[1].lifes -= 1
                        g[2].up_score()
                        if (g[1].lifes <= 0):
                            g[2].up_won()
                            self.inicializa()
                            self.round += 1  
                    self.bullets.remove(i)
            
    def inicializa(self):
        for p in self.players:
            self.players[p].cursorx = self.j.centerfy()[0]
            self.players[p].lifes = 3

    def player_enter(self,p):
        p = player(p)
        if len(self.players) < 2:
            if len(self.players) == 0:
                p.set_cursor(self.j.centerfy(),1, self.j.y)
            else:
                p.set_cursor(self.j.centerfy(),2, self.j.y)
            self.players[p.nickname] = p

    def imprime(self, nickname):
        self.j.screen.addstr(0, 0, self.j.labels['l_score'][0]+': '+str(self.players[nickname].score))
        self.j.screen.addstr(0, self.j.labels['l_won'][1], self.j.labels['l_won'][0]+': '+str(self.players[nickname].won))
        self.j.screen.addstr(self.j.y-1, 0, self.j.labels['l_round'][0]+": "+str(self.round))
        self.j.screen.addstr(self.j.y-1, self.j.labels['l_lifes'][1], self.j.labels['l_lifes'][0]+": "+str(self.players[nickname].lifes))
        for i in self.bullets:
            self.j.screen.addstr(i[2], i[1], 'O')
        self.j.gamepos[nickname] = (self.players[nickname].cursorx, self.players[nickname].cursory)


         #   self.j.gamepos[nickname] = (self.players[nickname].cursorx, self.players[nickname].cursory)
         #TODO fazer colisão de bullets e cursor
        
        for i in self.players:
            symb = None
            i = self.players[i]
            if i.cursory  > self.j.cy:
                symb = "▲"
            else:
                symb = '▼'
            self.j.screen.addstr(i.cursory, i.cursorx, symb)

        self.j.screen.move(self.players[nickname].cursory, self.players[nickname].cursorx)

    def gamecolision(self):
        for i in self.bullets:
            x = i[1]
            y = i[2]
            for n in self.players:
                j = self.players[n]
                x_player = j.cursorx
                y_player = j.cursory
                if ((x == x_player) and y == y_player):
                    return (True, self.players[n], self.players[i[0]])
        return(False,'')

    def shot(self, nickname):
        if self.players[nickname].cursory < self.j.cy:
            self.bullets.append([nickname, self.players[nickname].cursorx, self.players[nickname].cursory+1, time.time(), 'p'])
        else:
            self.bullets.append([nickname, self.players[nickname].cursorx, self.players[nickname].cursory-1, time.time(), 'm'])

    def move_cursx(self, d, nickname):
        if (d > 0):
            self.players[nickname].cursorx += 1
        if (d < 0):
            self.players[nickname].cursorx -= 1

        #limita x
        self.players[nickname].cursorx = max(0,self.players[nickname].cursorx)
        self.players[nickname].cursorx = min(self.j.x-1, self.players[nickname].cursorx)

def exec(jogo, nickname):
    k = 0
    jogo.player_enter(nickname)
    while jogo.ret('win'):
        jogo.ret('j.screen.clear()')
        jogo.imprime(nickname)
        jogo.ret('j.screen.refresh()')
        k = jogo.ret('j.screen.getch()')
        if k == curses.KEY_DOWN or k == curses.KEY_UP or k == 32:
            jogo.shot(nickname)
        elif k == curses.KEY_RIGHT:
            jogo.move_cursx(1, nickname)
        elif k == curses.KEY_LEFT:
            jogo.move_cursx(-1, nickname)
       # ret = jogo.j.colision()
        
##desenha o menu inicial na janela
def inicio(stdscr):
    global jglobal
    ret = None
    k = None
    height, width = stdscr.getmaxyx()
    cursor_x = width//2
    cursor_y = height//2
    stdscr.clear()
    stdscr.refresh()    
    j = janela(stdscr,width, height, cursor_x, cursor_y-2)
    jglobal = j
    f = j
    while(k != ord('q')):
        stdscr.clear()
        f.imprime()
        stdscr.refresh()
        k = stdscr.getch()
        if k == curses.KEY_DOWN:
            j.move_cursy(1)
        elif k == curses.KEY_UP:
            j.move_cursy(-1)
        elif k == curses.KEY_RIGHT:
            j.move_cursx(1)
        elif k == curses.KEY_LEFT:
            j.move_cursx(-1)
        elif k == 10:
            ret = j.colision()
            if (ret[0]):

                if (type(ret[1]) is type(cliente)) or (type(ret[1]) is type(servidor)):
                    f = ret[1](j)
                else:
                    ret[1]()

curses.wrapper(inicio)
    
