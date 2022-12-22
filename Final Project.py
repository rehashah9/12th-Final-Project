import pygame
import random
#function definations and classes for 2048 game
class Main:
    def __init__(self):
        # SETUP pygame environment
        pygame.init()
        self.screen = pygame.display.set_mode((500,500))
        pygame.display.set_caption('2048')
        self.clock = pygame.time.Clock()
        # Create the Board
        self.board = Board()
        #self.board.add_tile()
        self.run()

    def paint(self):
        # Paint the background
        self.screen.fill((160,223,254))
        # Write that by pressing Enter can return to home screen
        global tse
        self.screen.blit(tse,(80,460))
        # Paint the board object to screen
        self.board.paint(self.screen)
        pygame.display.update()

    # Handling pygame.QUIT event, and
    # KEYDOWNS. Keydowns is parsed to board.move function, Return for exiting game and going to home page
    def eventhandler(self):
        global v
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                global k
                global z
                global rk
                self.running = False
                v=k=z=False
                rk=0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.board.move("LEFT")
                if event.key == pygame.K_RIGHT:
                    self.board.move("RIGTH")
                if event.key == pygame.K_UP:
                    self.board.move("UP")
                if event.key == pygame.K_DOWN:
                    self.board.move("DOWN")
                if event.key==pygame.K_RETURN:
                    self.running=False
                    v=False

    # Update function.
    def update(self):
        self.board.update_tiles()

    # Main loop. 60 FPS
    def run(self):

        self.running = True
        while self.running:
            self.clock.tick(60)
            self.eventhandler()
            self.update()
            self.paint()


class Tile:
    def __init__(self,x,y,stage):
        # SETUP tiles x,y and stage. Stage is the number it represents, 2,4,8 etc.
        self.x = x
        self.y = y
        self.stage = stage
        self.colorlist = [(245,240,255),(108,187,244),(177,200,241),(147,164,247),(151,157,232),(158,189,224),(123,183,227),(126,145,207),(126,157,190),(184,154,245),(129,203,193)]


    # Move the tile to new x,y coordinates. Returns False if it moves into a wall.
    def move_tile(self,x=0,y=0):
        self.x += x
        self.y += y
        if self.x<0 or self.x > 3 or self.y < 0 or self.y > 3:
            self.x -= x
            self.y -=y
            return False
        return True

    # Merge two tiles.
    def merge(self,Tile):
        global p
        if Tile.stage == self.stage:
            self.increasestage()
            p+=1 #increasing points of user if they add two tiles
            return True
        else:
            return False

    def increasestage(self):
        self.stage += 1

    # Draw the tile to Board.
    def draw(self,screen,x,y,font):
        pygame.draw.rect(screen,self.colorlist[self.stage-1],(x,y,87,87))
        # draw the numbers on tiles:
        if self.stage <= 2:
            color = (120,110,101)
        else:
            color = (250,248,239)
        text = font.render(str(2**self.stage),2,color)
        screen.blit(text,(x+(87/2 - text.get_width()/2), y + (87/2 -text.get_height()/2)))

class Board:
    def __init__(self):
        ## self.tiles keep track of the tiles GUI positions.
        self.tiles = [[0,0,0,0] for i in range(4)]
        self.board = pygame.Rect(50,50,400,400)
        self.color = (2,170,251)
        # tilearray stores the tiles as a list. When self.update_tiles is called
        # the tiles in tile_array gets updated in self.tiles (the tiles GUI position)
        self.tilearray = []
        self.add_tile()
        self.add_tile()
        self.font = pygame.font.SysFont('comicsans',61)


    #Draw the board background to screen.
    def paint(self,screen):
        pygame.draw.rect(screen,self.color,self.board)
        self.drawtiles(screen)

    # Draw tiles to screen. If no tile, draw empty square.
    def drawtiles(self,screen):
        for i,array in enumerate(self.tiles):
            for j,tile in enumerate(array):
                if tile == 0:
                    pygame.draw.rect(screen,(204,193,180),(60+i*87+10*i,60+j*87+10*j,87,87))
                else:
                    tile.draw(screen,60+i*87+10*i,60+j*87+10*j,self.font)

    # Returns an arraylist with positions in self.tiles which are empty
    def get_empty_spaces(self):
        empty = []
        for i,array in enumerate(self.tiles):
            for j,tile in enumerate(array):
                if tile==0:
                    empty.append([i,j])

        return empty

    # Add a new tile to the game. Coordinates chosen at random.
    def add_tile(self):
        empty = self.get_empty_spaces()
        chosen = random.choice(empty)

        if random.randrange(1,100) <10:
            stage = 2
        else:
            stage = 1

        t = Tile(chosen[0],chosen[1],stage)

        self.tilearray.append(t)
    # Move all tiles on the board.
    def move(self,key):

        stepstaken = 0

        if key=="LEFT":
            for i, array in enumerate(self.tiles):
                for j, _ in enumerate(array):
                    tile = self.tiles[j][i]
                    if tile!=0:
                        stepstaken += self.move_single_tile(tile,-1,0)
                    self.update_tiles()

        if key =="RIGTH":
            for i,array in enumerate(self.tiles):
                for j,_ in enumerate(array):
                    tile = self.tiles[3-j][3-i]
                    if tile!= 0:
                        stepstaken += self.move_single_tile(tile,1,0)
                    self.update_tiles()

        if key == "UP":
            for i,array in enumerate(self.tiles):
                for j,_ in enumerate(array):
                    tile = self.tiles[i][j]
                    if tile!=0:
                        stepstaken += self.move_single_tile(tile,0,-1)
                    self.update_tiles()

        if key == "DOWN":
            for i, array in enumerate(self.tiles):
                for j,_ in enumerate(array):
                    tile = self.tiles[3-i][3-j]
                    if tile!=0:
                        stepstaken += self.move_single_tile(tile,0,1)
                    self.update_tiles()
        if stepstaken>0:
            self.add_tile()


    # Tiles are stored in self.tilearray. When updating, the tiles from self.tilearray is 
    # stored in the 2d array.

    def move_single_tile(self,tile,vx=0,vy=0):
        steps = 0
        for i in range(0,3):
            if self.position_is_inside_grid(tile.x+vx,tile.y+vy) and self.tile_is_empty(tile.x+vx,tile.y+vy):
                tile.move_tile(vx,vy)
                steps+=1
            else:
                if self.position_is_inside_grid(tile.x+vx,tile.y+vy) and self.tiles[tile.x+vx][tile.y+vy].merge(tile):
                    self.tilearray.remove(tile)
                    steps += 1

        return steps 

    def position_is_inside_grid(self,x,y):
        if x>-1 and x<4 and y>-1 and y<4:
            return True
        else:
            return False

    def tile_is_empty(self,x,y):
        if self.tiles[x][y] == 0:
            return True
        else:
            return False

    def update_tiles(self):
        self.tiles = [[0,0,0,0] for i in range(4)]
        for tile in self.tilearray:
            self.tiles[tile.x][tile.y] = tile


pygame.init()
dis=pygame.display.set_mode((600,600)) #display
t=pygame.time.Clock() #clock
fo=pygame.font.SysFont('Agency FB',25) #font
#loading and resizing image of tic tac toe, user profile, leaderboard, login again and point system for home page
TTTim=pygame.image.load("C:/Users/Admin/Pictures/Project/2048 tic tac toe.jpg")
TTTim=pygame.transform.scale(TTTim,(375,300))
Upim=pygame.image.load("C:/Users/Admin/Pictures/Project/user profile.jpeg")
Upim=pygame.transform.scale(Upim,(250,125))
Lbim=pygame.image.load("C:/Users/Admin/Pictures/Project/leaderboard.jpeg")
Lbim=pygame.transform.scale(Lbim,(250,125))
Ptim=pygame.image.load("C:/Users/Admin/Pictures/Project/point system.jpeg")
Ptim=pygame.transform.scale(Ptim,(550,125))
Luim=pygame.image.load("C:/Users/Admin/Pictures/Project/different login.jpg")
Luim=pygame.transform.scale(Luim,(187,300))
#loading and resizing images of 'X' and 'O' for tic tac toe
Xim=pygame.image.load("C:/Users/Admin/Pictures/Project/PicsArt_10-27-08.37.30.jpg")
Oim=pygame.image.load("C:/Users/Admin/Pictures/Project/PicsArt_10-27-08.38.04.jpg")
Xim=pygame.transform.scale(Xim,(175,175))
Oim=pygame.transform.scale(Oim,(175,175))
#loading and resizing images to declare the winner or draw for tic tac toe
Pxim=pygame.image.load("C:/Users/Admin/Pictures/Project/PicsArt_10-27-08.42.09.jpg")
Poim=pygame.image.load("C:/Users/Admin/Pictures/Project/PicsArt_10-27-08.44.10.jpg")
Pdim=pygame.image.load("C:/Users/Admin/Pictures/Project/PicsArt_10-27-08.45.24.jpg")
Pxim=pygame.transform.scale(Pxim,(500,500))
Poim=pygame.transform.scale(Poim,(500,500))
Pdim=pygame.transform.scale(Pdim,(500,500))
#loading and resizing images of the numbers of the boxes for tic tac toe
im1=pygame.image.load("C:/Users/Admin/Pictures/Project/PicsArt_10-27-07.42.49.jpg")
im2=pygame.image.load("C:/Users/Admin/Pictures/Project/PicsArt_10-27-07.43.15.jpg")
im3=pygame.image.load("C:/Users/Admin/Pictures/Project/PicsArt_10-27-07.43.55.jpg")
im4=pygame.image.load("C:/Users/Admin/Pictures/Project/PicsArt_10-27-08.34.30.jpg")
im5=pygame.image.load("C:/Users/Admin/Pictures/Project/PicsArt_10-27-08.34.57.jpg")
im6=pygame.image.load("C:/Users/Admin/Pictures/Project/PicsArt_10-27-09.33.07.jpg")
im7=pygame.image.load("C:/Users/Admin/Pictures/Project/PicsArt_10-27-08.35.25.jpg")
im8=pygame.image.load("C:/Users/Admin/Pictures/Project/PicsArt_10-27-08.35.46.jpg")
im9=pygame.image.load("C:/Users/Admin/Pictures/Project/PicsArt_10-27-08.36.04.jpg")
im1=pygame.transform.scale(im1,(175,175))
im2=pygame.transform.scale(im2,(175,175))
im3=pygame.transform.scale(im3,(175,175))
im4=pygame.transform.scale(im4,(175,175))
im5=pygame.transform.scale(im5,(175,175))
im6=pygame.transform.scale(im6,(175,175))
im7=pygame.transform.scale(im7,(175,175))
im8=pygame.transform.scale(im8,(175,175))
im9=pygame.transform.scale(im9,(175,175))
#loading and resizing image to display GAME OVER in 2048 game
Goim=pygame.image.load("C:/Users/Admin/Pictures/Project/PicsArt_11-03-10.19.26.jpg")
Goim=pygame.transform.scale(Goim,(400,300))
#connecting to mysql and obtaining all data stored
import mysql.connector as m
mo=m.connect(host='localhost',user='root',password='reha',database='user')
co=mo.cursor()
co.execute('use user')
#co.execute('create table user_data(p_no integer primary key,username char(40) not null,points integer,password char(40) not null)')
k=True
# loop to allow different users to use one after other without closing whole application
while k:
    co.execute('select * from user_data')
    data=co.fetchall()
    rec=[] #list containing data of user
    tk=1 #variable used to record if quit pressed in password or username window and then not go through any other process
    #displaying page for entering username
    a=True
    s=''
    while a:
        pygame.display.set_caption('Username') #caption/title
        event=pygame.event.poll()
        keys=pygame.key.get_pressed()
        if event.type==pygame.QUIT:
            k=False
            a=False
            tk=0
        if event.type==pygame.KEYDOWN:
            key=pygame.key.name(event.key)
            if len(key)==1:
                if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                    s+=key.upper()
                else:
                    s+=key
            elif key=='backspace':
                s=s[:len(s)-1]
            elif event.key==pygame.K_RETURN:
                a=False
        st='enter user_name (of player 1 for X-O game) in black rectangle'
        sp="don't use Space,Underscore."
        sm='press Enter to move to page to enter password'
        tp=fo.render(sp,1,(225,225,225))
        tm=fo.render(sm,1,(225,225,225))
        tx=fo.render(st,1,(225,225,225))
        tn=fo.render(s,1,(225,225,225))
        dis.fill((26,159,174))
        pygame.draw.rect(dis,(0,0,0),pygame.Rect(45,290,500,45))
        dis.blit(tx,(25,50))
        dis.blit(tn,(50,300))
        dis.blit(tp,(25,125))
        dis.blit(tm,(25,200))
        pygame.display.update()
    re=0 #variable used to record if username already exists or not
    #recording data of user in list rec
    for i in data:
        if i[1]==s:
            for j in i:
                rec.append(j)
            re+=1
    # displaying page for entering password
    b=True
    u=''
    while b and tk:
        pygame.display.set_caption('Password') #caption/title
        event=pygame.event.poll()
        keys=pygame.key.get_pressed()
        if event.type==pygame.QUIT:
            b=k=False
            tk=0
        if event.type==pygame.KEYDOWN:
            key=pygame.key.name(event.key)
            if len(key)==1:
                if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                    u+=key.upper()
                else:
                    u+=key
            elif key=='backspace':
                u=u[:len(u)-1]
            elif event.key==pygame.K_RETURN:
                if re!=0:
                    if u==rec[3]:
                        b=False
                    else:
                        u=''
                else:
                    b=False
        st='enter password (of player 1 for X-O game) in black rectangle'
        sp="don't use Space,Underscore,if page appears again: enter different"
        sp1='password as that is not the correct one.'
        sm='press Enter to move to go to home page'
        tp1=fo.render(sp1,1,(225,225,225))
        tm=fo.render(sm,1,(225,225,225))
        tx=fo.render(st,1,(225,225,225))
        tu=fo.render(u,1,(225,225,225))
        tp=fo.render(sp,1,(225,225,225))
        dis.fill((26,159,174))
        pygame.draw.rect(dis,(0,0,0),pygame.Rect(45,290,500,45))
        dis.blit(tx,(25,50))
        dis.blit(tu,(50,300))
        dis.blit(tp,(25,105))
        dis.blit(tp1,(25,130))
        dis.blit(tm,(25,180))
        pygame.display.update()
    #adding record of user if it doesn't exist
    if re==0 and tk==1:
        co.execute('select max(p_no) from user_data')
        lpno=co.fetchone()
        mpno=lpno[0]
        ins='insert into user_data values(%s,%s,%s,%s)'
        if mpno==None:
            rectu=(1,s,0,u)
            co.execute(ins,rectu)
            rec=[1,s,0,u]
        else:
            rectu=(mpno+1,s,0,u)
            co.execute(ins,rectu)
            rec=[mpno+1,s,0,u]
        mo.commit()
    if tk==1:
        p=rec[2] #points of user
    #loop for home page, includes both games, user profile and leaderboard
    z=True
    while z and tk:
        dis=pygame.display.set_mode((600,600)) #display
        pygame.display.set_caption('Home Page') #caption/title
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                z=False
                k=False
            elif event.type==pygame.KEYDOWN:
                #to enter different username
                if event.key==pygame.K_4:
                    z=False
                # playing tic tac toe if 1 pressed
                elif event.key==pygame.K_1:
                    pygame.display.set_caption('Tic Tac Toe Game') #caption/title
                    l=[[1,2,3],[4,5,6],[7,8,9],[1,4,7],[2,5,8],[3,6,9],[1,5,9],[3,5,7]] #list of all possible combination to win
                    a=[] #list to record all boxes already used
                    xl=[] #list to record boxes used by player 1 - X
                    ol=[] #list to record boxes used by player 2 - O
                    c=1  #integer value of the number of the next turn
                    e=1  #integer value of the total number of turns already done
                    n=0  #number of box chosen by the player
                    r=True
                    d=0
                    zk=1 #variable used to not display conclusion pages or add points if quit pressed in middle of game
                    while c<=9:
                        #coloring the background and drawing the 4 lines that will split the display into 9 boxes
                        dis.fill((225,225,225))
                        pygame.draw.line(dis,(0,0,0),(200,0),(200,600),5)
                        pygame.draw.line(dis,(0,0,0),(400,0),(400,600),5)
                        pygame.draw.line(dis,(0,0,0),(0,200),(600,200),5)
                        pygame.draw.line(dis,(0,0,0),(0,400),(600,400),5)
                        #bliting images of the numbers of the squares
                        dis.blit(im1,(10,10))
                        dis.blit(im2,(210,10))
                        dis.blit(im3,(410,10))
                        dis.blit(im4,(10,210))
                        dis.blit(im5,(210,210))
                        dis.blit(im6,(410,210))
                        dis.blit(im7,(10,410))
                        dis.blit(im8,(210,410))
                        dis.blit(im9,(410,410))
                        pygame.display.update()
                        while r:
                            for event in pygame.event.get():
                                #closing game if user quits
                                if event.type==pygame.QUIT:
                                    r=False
                                    z=False
                                    k=False
                                    zk=0
                                    c=10
                                # recording number of box chosen by the player and the cordinates where the image of X/O will be blitted
                                elif event.type==pygame.KEYDOWN:
                                    if event.key==pygame.K_1:
                                        n,x,y=1,10,10
                                    elif event.key==pygame.K_2:
                                        n,x,y=2,210,10
                                    elif event.key==pygame.K_3:
                                        n,x,y=3,410,10
                                    elif event.key==pygame.K_4:
                                        n,x,y=4,10,210
                                    elif event.key==pygame.K_5:
                                        n,x,y=5,210,210
                                    elif event.key==pygame.K_6:
                                        n,x,y=6,410,210
                                    elif event.key==pygame.K_7:
                                        n,x,y=7,10,410
                                    elif event.key==pygame.K_8:
                                        n,x,y=8,210,410
                                    elif event.key==pygame.K_9:
                                        n,x,y=9,410,410
                            #bliting the image of X/O at required positions
                            if c%2!=0:
                                if n not in a:
                                    if n!=0:
                                        dis.blit(Xim,(x,y))
                                        pygame.display.update()
                                        xl.append(n)
                                        a.append(n)
                                        e=c
                                        c+=1
                            else:
                                if n not in a:
                                    if n!=0:
                                        dis.blit(Oim,(x,y))
                                        pygame.display.update()
                                        ol.append(n)
                                        a.append(n)
                                        e=c
                                        c+=1
                            #checking if either player won by comaring xl/ol with l and closing game if they did
                            for i in l:
                                if e%2!=0 and zk:
                                    if i[0] in xl:
                                        if i[1] in xl:
                                            if i[2] in xl:
                                                r=False
                                                xl=[]
                                                d=1
                                                p+=10
                                else:
                                    if i[0] in ol and zk:
                                        if i[1] in ol:
                                            if i[2] in ol:
                                                r=False
                                                ol=[]
                                                d=1
                            t.tick(60)
                            #closing game if all 9 turns are done and nobody has won yet
                            if e==9 and zk:
                                if d==0:
                                    r=False
                                    print("It's a draw, nobody lost !!!")
                                    p+=5
                        #displaying winner of game of draw
                        while c<=10 and zk:
                            for event in pygame.event.get():
                                if event.type==pygame.QUIT:
                                    c=11
                                    r=k=z=False
                                if event.type==pygame.KEYDOWN:
                                    if event.key==pygame.K_RETURN:
                                        c=11 #to come out of while c<=9 and c<=10 loop
                            # displaying who won or draw
                            if d==1:
                                if e%2!=0:
                                    dis.fill((0,0,0))
                                    dis.blit(Pxim,(50,50))
                                    pygame.display.update()
                                else:
                                    dis.fill((0,0,0))
                                    dis.blit(Poim,(50,50))
                                    pygame.display.update()
                            elif d==0:
                                dis.fill((0,0,0))
                                dis.blit(Pdim,(50,50))
                                pygame.display.update()
                            t.tick(60)
                # displaying leaderboard
                elif event.key==pygame.K_3:
                    g=True
                    while g:
                        pygame.display.set_caption('Leaderboard') #caption/title
                        cr=50
                        for event in pygame.event.get():
                            if event.type==pygame.QUIT:
                                g=z=k=False
                            if event.type==pygame.KEYDOWN:
                                if event.key==pygame.K_RETURN:
                                    g=False
                        dis.fill((26,159,174))
                        co.execute('select * from user_data order by points desc,p_no')
                        ld=co.fetchall()
                        sl='LEADERBOARD (Top 10)'
                        sr='No.    Username- Points'
                        se='Press Enter to return to home page'
                        tx=fo.render(se,1,(225,225,225))
                        tr=fo.render(sr,1,(225,225,225))
                        tl=fo.render(sl,1,(225,225,225))
                        dis.blit(tl,(50,15))
                        dis.blit(tr,(50,60))
                        dis.blit(tx,(50,550))
                        q=1
                        for i in ld[:10]:
                            cr+=45
                            sld=str(q)+'.'+'      '+i[1]+'- '+str(i[2])
                            tld=fo.render(sld,1,(225,225,225))
                            dis.blit(tld,(50,cr))
                            q+=1
                        pygame.display.update()
                # displaying user profile
                elif event.key==pygame.K_SPACE:
                    y=True
                    while y:
                        pygame.display.set_caption('User Profile') #caption/title
                        for event in pygame.event.get():
                            if event.type==pygame.QUIT:
                                y=z=k=False
                            if event.type==pygame.KEYDOWN:
                                if event.key==pygame.K_RETURN:
                                    y=False
                                # to delete user record
                                elif event.key==pygame.K_1:
                                    tpl=(rec[0],)
                                    ex='delete from user_data where p_no=%s'
                                    co.execute(ex,tpl)
                                    mo.commit()
                                    y=False
                                    z=False
                        su='password : '+u
                        sn='username : '+s
                        spno='Player number : '+str(rec[0])
                        sp='Points : '+str(p)
                        se='Press Enter to return to home page'
                        sd='Press 1 to delete your profile'
                        tx=fo.render(se,1,(225,225,225))
                        tp=fo.render(sp,1,(225,225,225))
                        tpno=fo.render(spno,1,(225,225,225))
                        td=fo.render(sd,1,(225,225,225))
                        tsu=fo.render(su,1,(225,225,225))
                        tsn=fo.render(sn,1,(225,225,225))
                        dis.fill((26,159,174))
                        dis.blit(tsu,(50,250))
                        dis.blit(tx,(50,500))
                        dis.blit(tsn,(50,150))
                        dis.blit(tp,(50,350))
                        dis.blit(tpno,(50,50))
                        dis.blit(td,(50,550))
                        pygame.display.update()
                #playing 2048 game if 2 is pressed
                elif event.key==pygame.K_2:
                    rk=1 #used so that game over page not displayed if quit pressed in middle of game
                    v=True
                    while v:
                        ste='Press Enter to return to home screen'
                        tse=fo.render(ste,1,(0,0,0))
                        m = Main()
                        # TO DO
                        # Refactor move() to loop functions
                    h=True
                    while h and rk:
                        for event in pygame.event.get():
                            if event.type==pygame.QUIT:
                                h=z=k=False
                            if event.type==pygame.KEYDOWN:
                                if event.key==pygame.K_RETURN:
                                    h=False
                        dis.fill((0,0,0))
                        dis.blit(Goim,(50,100))
                        pygame.display.update()
        #updating points of user
        rec[2]=p
        tup=(rec[2],rec[0])
        exc='update user_data set points=%s where p_no=%s'
        co.execute(exc,tup)
        mo.commit()
        # home page display
        dis.fill((225,225,225))
        dis.blit(TTTim,(12,150))
        dis.blit(Upim,(300,12))
        dis.blit(Lbim,(25,12))
        dis.blit(Ptim,(25,463))
        dis.blit(Luim,(400,150))
        pygame.display.update()
        t.tick(60)
co.close()
mo.close()
pygame.quit()
