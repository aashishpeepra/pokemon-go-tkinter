import pygame
import sys
import random
import time
from pygame import draw
#constants
HEIGHT = 600
WIDTH = 390
FPS = 60
CHARACTER_SIZE = (70,70)
SPEED = 10

#DECLARING COLORS
BLACK = (0,0,0)

#INITIALIZING GAME AND CREATING WINDOW
pygame.init() #STARTS THE PYGAME
pygame.mixer.init()
screen=pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Pokemon go!")
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()

#HELPDER FUNCTIONS

def random_coords():
    return [random.randint(10,290),random.randint(35,480)]

def generate_image_and_rect(src,currentSize):
    print("Loaded {} image from path {}".format(src,"./Assets/"+src))
    image = pygame.image.load(".//Assets//"+src)
    image = pygame.transform.scale(image,currentSize)
    return image , image.get_rect()

#IMAGES
background_image = pygame.image.load(".//Assets//6.png").convert()
background_rect = background_image.get_rect()
#generating and initializing images for pokemons and players
balbasour,balbasour_rect = generate_image_and_rect("bulbasour.png", CHARACTER_SIZE)
squirtel,squirtel_rect = generate_image_and_rect("squirtel.png",CHARACTER_SIZE)
pikachu, pikachu_rect = generate_image_and_rect("pikachu.png",(30,30))
player1, player_rect = generate_image_and_rect("player1.png",(30,30))
player2,player2_rect = generate_image_and_rect("player2.jpg",(30,30))
character,character_rect = generate_image_and_rect("character.jpg",(30,30))
charmender,charmender_react = generate_image_and_rect("charmender.jpg",(30,30))

# INITIAL POSITIONS FOR ALL CHARACTER

positions = {"balbasour":{"pos":random_coords(),"rect":balbasour_rect,"img":balbasour},"charmender":{"pos":random_coords(),"rect":character_rect,"img":charmender},"player1":{"pos":random_coords(),"rect":player_rect,"img":player1},"player2":{"pos":random_coords(),"rect":player2_rect,"img":player2},"pikachu":{"pos":random_coords(),"rect":pikachu_rect,"img":pikachu},"squirtel":{"pos":random_coords(),"rect":squirtel_rect,"img":squirtel}}


#BORDER CONDITIONS
def down_border_control(x,y):
    if ((x>=170 and x<=210) or (x>=80 and x<=120)) and y>=485:
        return True
    if ((x>=230 and x<=300) or (x>=0 and x<=70)) and (y>=425 and y<=435):
        return True
    return False
def right_border_control(x,y):
    if x>=150 and (y>=485):
        return True
    if x>=210 and (y>=435 and y<=485):
        return True
def lefT_border_control(x,y):
    if x<=120 and (y>=485):
        return True
    if (x<90) and (y>=435 and y<=485):
        return True

def draw_rect():
    pygame.draw.rect(screen,(230,230,230),pygame.Rect(5,HEIGHT-150,WIDTH-15,150))
def write_text(text,position,size=14,bold=False):
    font = pygame.font.SysFont('monospace',size,bold=bold)
    screen.blit(font.render(text,True,(50,50,50)),position)
def player_card(xp,charName,charImage,top=False):
    leftPad = 250
    topPad = 0
    if top:
        leftPad = 20
        topPad = 300
    write_text(charName,(leftPad,topPad),18,True)
    write_text("XP",(leftPad,topPad+20),16,False)
    pygame.draw.rect(screen,(230,230,230),pygame.Rect(leftPad,topPad+50,100,20))
    if xp<=0:
        xp = 0
    pygame.draw.rect(screen,(0,255,0),pygame.Rect(leftPad,topPad+50,xp,20))
    screen.blit(charImage,(leftPad,topPad+70))
def choose_pokemon(current,data):
    write_text("Choose Pokemon",(15,480),18,bold=True)
    write_text(data[0]["name"],(15,520),18,bold=current==1)
    write_text(data[1]["name"],(15,540),18,bold=current!=1)
def choose_attack(choice,name):
    write_text("Choose Attack",(15,480),18,bold=True)
    if name=="pikachu":
        write_text("Thunderbolt",(15,520),18,bold=choice==1)
        write_text("Tackel",(15,540),18,bold=choice!=1)
    elif name=="balbasour":
        write_text("Razor Leaf",(15,520),18,bold=choice==1)
        write_text("Poison Seed",(15,540),18,bold=choice!=1)
    elif name=="charmender":
        write_text("fire Ball",(15,520),18,bold=choice==1)
        write_text("Fire tornado",(15,540),18,bold=choice!=1)
    elif name=="squirtel":
        write_text("Water Splash",(15,520),18,bold=choice==1)
        write_text("Tackel",(15,540),18,bold=choice!=1)

def gen_pok():
    rnd = random.randint(0,3)
    pokiList = ["pikachu","squirtel","balbasour","charmender"]
    return {
        "name":pokiList[rnd],
        "pok":positions[pokiList[rnd]],
        "xp" : 100
    }
def player_loose(data):
    total = 0
    for each in data:
        total+=each["xp"]
    return total<=20
#The ultimate game loop
gameRunning = True
x = 170
y = 550
yesOrNo = True
startBattle = False
choosen = False
choosePokemon = 1
chosenPok = False
chooseAttack = 1
choosenAttack = False
battle = {
    "comp":{"data":[gen_pok() for i in range(2)],"attack":1,"current":1},
    "user":{"data":[gen_pok() for i in range(2)],"attack":1,"current":1}
}
attackData = {
    "pikachu":[40,50],
    "balbasour":[33,70],
    "charmender":[40,45],
    "squirtel":[30,20]
}
turn = 1
everStarted = False
neverAttacked = True
counter = 0
inContact = False
while gameRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameRunning = False
        if event.type == pygame.KEYDOWN:
            print("Pressed")
            if event.key == pygame.K_LEFT:
                # if lefT_border_control(x,y):
                #     continue
                if x <5 :
                    x = x
                else:
                    x = x-SPEED
                print(x)
            if event.key == pygame.K_RIGHT:
                # if right_border_control(x,y):
                #     continue
                if x>292:
                    x = x
                else:
                    x = x+SPEED
                print(x)
            if event.key == pygame.K_UP:
                if not choosen:
                    yesOrNo = not yesOrNo
                choosePokemon = 2 if choosePokemon == 1 else 1
                chooseAttack = 1 if chooseAttack == 2 else 2
                if y<=35:
                    y = y
                else:
                    y = y-SPEED
                print(y)
            if event.key == pygame.K_DOWN:
                # if down_border_control(x,y):
                #     continue
                if not choosen:
                    yesOrNo = not yesOrNo
                choosePokemon = 2 if choosePokemon == 1 else 1
                chooseAttack = 1 if chooseAttack == 2 else 2
                if y+SPEED>535:
                    y = 540
                else:
                    y = y+SPEED
                print(y)
            if event.key == pygame.K_RETURN:
                if choosen:
                    chosenPok = True
                    everStarted = True
                    if chosenPok and (counter==2 or counter%2==1):
                        choosenAttack = False
                    if counter%2==0:
                        choosenAttack = True
                choosen = True
                counter+=1
                print("Battle Started!") if yesOrNo else print("Battle Denied!")
                startBattle = yesOrNo
                
    all_sprites.update()

    #perform motions
    screen.fill((255,255,255))
    if not startBattle :
        screen.blit(background_image,background_rect)
        for each in positions: #rendering all imagges
            print(each,WIDTH - positions[each]["pos"][0],HEIGHT-positions[each]["pos"][1],positions[each]["pos"])
            positions[each]["rect"] = positions[each]["pos"]
            screen.blit(positions[each]["img"],positions[each]["rect"])
        oppX = WIDTH- positions["player1"]["pos"][0]
        oppY = HEIGHT- positions["player1"]["pos"][1]
        if oppX > x:
            oppX = positions["player1"]["pos"][0]
        if oppY > y:
            oppY= positions["player1"]["pos"][1]
        if (oppX-100) <= x <= (oppX+100) or (oppY-100)<=y<=(oppY+100):
            print("Attack",positions["player1"]["pos"][1]-y)
            inContact = True
            
        screen.blit(character,[x,y])
        character_rect.move([x,y])
        print(x,y)
        
        if inContact:
            draw_rect()
            if not choosen :
                write_text("Trainer wants to fight with you.",(15,460),18,bold=True)
                write_text("Are you ready?",(15,480),18,bold=True)
                write_text("Yes",(15,520),18,bold=yesOrNo)
                write_text("No",(15,540),18,bold=(not yesOrNo))
            elif not everStarted:
                write_text("You denied the challenge",(15,460),18,bold=True)

    else:
        # If the user accepts the challenge
        draw_rect()
        userCurrent = battle["user"]["current"]
        compCurrent = battle["comp"]["current"]
        userPok = battle["user"]["data"][userCurrent]["name"]
        compPok= battle["comp"]["data"][compCurrent]["name"]
        player_card(battle["comp"]["data"][compCurrent]["xp"],compPok,positions[compPok]["img"])
        player_card(battle["user"]["data"][userCurrent]["xp"],userPok,positions[userPok]["img"],True)
        if turn==1:
            if not chosenPok :
                choose_pokemon(choosePokemon,battle["user"]["data"])
                battle["user"]["current"] = choosePokemon-1
            elif chosenPok:
                if not choosenAttack :
                    choose_attack(chooseAttack,battle["user"]["data"][battle["user"]["current"]]["name"])

                elif choosenAttack :
                    user_pk = battle["user"]["data"][battle["user"]["current"]]["name"]
                    reducedXp = attackData[user_pk][battle["user"]["attack"]]
                    write_text("Reduced {} XP".format(reducedXp),(10,500),18,True)
                    battle["comp"]["data"][battle["comp"]["current"]]["xp"]-=reducedXp
                    
                    print(battle["comp"]["data"][battle["comp"]["current"]]["xp"])
                    #gameRunning = False
                    neverAttacked = True
                    chosenPok = False
                    turn = 2
        if turn==2:
            
            battle["comp"]["current"] = random.randint(0,1)
            battle["comp"]["attack"] = random.randint(0,1)
            user_pk = battle["comp"]["data"][battle["comp"]["current"]]["name"]
            reducedXp = attackData[user_pk][battle["comp"]["attack"]]
            write_text("Reduced {} XP".format(reducedXp),(10,500),18,True)
            battle["user"]["data"][battle["user"]["current"]]["xp"]-=reducedXp
            
            print(battle["comp"]["data"][battle["comp"]["current"]]["xp"])
            #gameRunning = False
            choosenAttack = False
            turn = 1
            chosenPok = False
    #check for battle conditions
    if player_loose(battle["user"]["data"]) and player_loose(battle["comp"]["data"]):
        write_text("Game Tied. Nice Fight",(10,500),18,True)
    if player_loose(battle["user"]["data"]):
        write_text("You Loose! Better Luck Next Time.",(10,500),18,True)
        startBattle = False
    if player_loose(battle["comp"]["data"]):
        write_text("You Win! Amazing Job.",(10,500),18,True)
        startBattle = False
        print("Pressed yes")
        print("oh")
    all_sprites.update()
    pygame.display.flip()

