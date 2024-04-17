import random
#khoo jing xiang 10242713G
# Game variables

game_vars = {
    'turn': 0,                      # Current Turn
    'monster_kill_target': 20,      # Number of kills needed to win
    'monsters_killed': 0,           # Number of monsters killed so far
    'num_monsters': 0,              # Number of monsters in the field
    'gold': 10,                     # Gold for purchasing units
    'threat': 0,                    # Current threat metre level
    'max_threat': 10,               # Length of threat metre
    'danger_level': 1,              # Rate at which threat increases
    }
defenders = {'ARCHR': {'name': 'Archer',
                       'maxHP': 5,
                       'min_damage': 1,
                       'max_damage': 4,
                       'price': 5,
                       },
             
             'WALL': {'name': 'Wall',
                      'maxHP': 20,
                      'min_damage': 0,
                      'max_damage': 0,
                      'price': 3,
                      }
             }  
monsters = {'ZOMBI': {'name': 'Zombie',
                      'maxHP': 15,
                      'min_damage': 3,
                      'max_damage': 6,
                      'moves' : 1,
                      'reward': 2
                      },

            'WWOLF': {'name': 'Werewolf',
                      'maxHP': 10,
                      'min_damage': 1,
                      'max_damage': 4,
                      'moves' : 2,
                      'reward': 3
                      }
            }
 
defender_list = ['ARCHR', 'WALL']
monster_list = ['ZOMBI', 'WWOLF']

archer = {'shortform' : 'ARCHR',
          'name': 'Archer',
          'maxHP': 5,
          'min_damage': 1,
          'max_damage': 4,
          'price': 5
          }
             
wall = {'shortform': 'WALL',
        'name': 'Wall',
        'maxHP': 20,
        'min_damage': 0,
        'max_damage': 0,
        'price': 3
        }

zombie = {'shortform': 'ZOMBI',
          'name': 'Zombie',
          'maxHP': 15,
          'min_damage': 3,
          'max_damage': 6,
          'moves' : 1,
          'reward': 2
          }

field = [ [None, None, None, None, None, None, None],
          [None, None, None, None, None, None, None],
          [None, None, None, None, None, None, None],
          [None, None, None, None, None, None, None],
          [None, None, None, None, None, None, None] ]


#----------------------------------------------------------------------
# draw_field()
#
#    Draws the field of play
#    The column numbers only go to 3 since players can only place units
#      in the first 3 columns
#----------------------------------------------------------------------

def draw_field():
    num_rows=len(field)
    num_columns=len(field[0])
    print('{:^2}{:^6}{:^6}{:^6}'.format(' ','1','2','3'))
    print(end=' ')
#print the top line
    for column in range(num_columns):
        print('+-----',end='')
    print('+')
    for row in range(num_rows):
        print(chr(ord('A')+row),end='')  #using order of len(field) to print out abcde by adding row+1,+2,+3 to ord('A') and so on
        for column in field[row]:
            if column !=None:
                print('|{:5}'.format(str(column[0])),end='')
            else:
                print('|{:5}'.format(' '),end='')
        print('|')
        print(' ',end='')
        for column in field[row]:
            if column !=None:
                if column[0]=='ZOMBI':
                    maxHP=zombie['maxHP']
                elif column[0]=='ARCHR':
                    maxHP=archer['maxHP']
                elif column[0]=='WALL':
                    maxHP=wall['maxHP']
                else:
                    maxHP=0
                print('|{:>2}/{:<2}'.format(str(column[1]),str(maxHP)),end='')
            else:
                print('|{:5}'.format(' '),end='')
        print('|')
        print(' ',end='')
        for column in range(num_columns):
            print('+-----',end='')
        print('+')
    return

#----------------------------
# show_combat_menu()
#
#    Displays the combat menu
#----------------------------
def show_combat_menu(game_vars):
    print('Turn {}     Threat = [{}]     Danger Level {}'.format(game_vars['turn'],'-'*game_vars['threat'],game_vars['danger_level']))
    print('Gold= {}    Monster killed={}/{}'.format(game_vars['gold'],game_vars['monsters_killed'],game_vars['monster_kill_target']))
    print("1. Buy unit     2. End turn")
    print("3. Save game    4. Quit")

#----------------------------
# show_main_menu()
#
#    Displays the main menu
#----------------------------
def show_main_menu():
    print("1. Start new game")
    print("2. Load saved game")
    print("3. Quit")

#-----------------------------------------------------
# place_unit()
#
#    Places a unit at the given position
#    This function works for both defender and monster
#    Returns False if the position is invalid
#       - Position is not on the field of play
#       - Position is occupied
#       - Defender is placed past the first 3 columns
#    Returns True if placement is successful
#-----------------------------------------------------

def place_unit(field, position, unit_list):
    row=ord(position[0])- ord('A')   #ord of letter of input -ord('A') get the row[] list
    column= int(position[1]) -1      # position of input e.g 1-1=0 
     
    if field[row][column]==None:  #If the field is not occupied,place the unit
        field[row][column]=[unit_list['shortform'], unit_list['maxHP']]    #print out the zombioe name and hp
        
        return True
    else:
        return False

#-------------------------------------------------------------------
# buy_unit()
#
#    Allows player to buy a unit and place it using place_unit()
#-------------------------------------------------------------------
def buy_unit(field, game_vars):
    print('What unit do you wish to buy?')
    print('1. Archer (5 gold) \n'
          '2. Wall (3 gold) \n'
          '3. Dont buy')
    while True:
        #try:
        choices=int(input('Your choice? '))
        if choices==1:
            location=input('Place where? ') 
            game_vars['gold']-=5
            location=location.capitalize() 
   
            place_unit(field,location,archer) 
            return
        elif choices==2: 
            location=input('Place where? ')
            game_vars['gold']-=3
            location=location.capitalize() 
            place_unit(field,location,wall) 
            return
        elif choices==3:
            break
        #except
    
     


#-----------------------------------------------------------
# defender_attack()
#
#    Defender unit attacks.
#
#-----------------------------------------------------------
def defender_attack(defenders_list, field, row, column):

        if field[row][column][0] in defenders_list:
            for col_mon in range(column+1,len(field[row])):        #range of monster from defender
                if field[row][col_mon]!=None:        #check for monster
                        if field[row][col_mon][0] in monster_list:    #confirm monster
                            damage=random.randint(archer['min_damage'],archer['max_damage'])
                            field[row][col_mon][1]-=damage
                            #if field[row][column][0]!=wall['shortform']:
                            print('{} in lane {} shoots {} for {} damage!'.format(archer['name'],chr(65+row),monsters[field[row][col_mon][0]]['name'],damage))
         
                            if field[row][col_mon][1]<=0:  #when zombie hp is 0 and dies
                                print('{} dies! '.format(monsters[field[row][col_mon][0]]['name']))
                                print('You gain {} gold as a reward.'.format(monsters[field[row][col_mon][0]]['reward']))
                                game_vars['gold']+=monsters[field[row][col_mon][0]]['reward']
                                game_vars['monsters_killed']+=1
                                field[row][col_mon]=None
                                game_vars['num_monsters']-=1
                                game_vars['threat'] += zombie['reward']
                        break
            return

#-----------------------------------------------------------
# monster_advance()
#
#    Monster unit advances.
#       - If it lands on a defender, it deals damage
#       - If it lands on a monster, it does nothing
#       - If it goes out of the field, player loses
#-----------------------------------------------------------
def monster_advance(zombie, field, row, column):
    #Advance enemies and attack
    if field[row][column]!=None:
        if field[row][column][0]==zombie['shortform']:
            if field[row][column-1] != None:
                for name in defender_list:
                    if field[row][column-1][0] == name:    #archer being damage by zombie
                        damage = random.randint(zombie['min_damage'],zombie['max_damage'])
                        field[row][column-1][1] -= damage
                        print("{} in lane {} hits {} for {} damage!".format(zombie['name'], chr(row+65), defenders[name]['name'], damage))
                        if field[row][column-1][1] <= 0:
                            print("{} dies!".format(name['name']))
                            field[row][column-1] = None
                            break
            else:
                #replacing of zombie position
                field[row][column-1] = field[row][column]
                field[row][column] = None
                print("{} in lane {} advances!".format(zombie['name'], chr(row+65)))
                if column == 0: #if zombie makes it to city
                    print("A {} has reached the city! All is lost!".format(zombie['name']))
                    quit()

    return

#---------------------------------------------------------------------
# spawn_monster()
#
#    Spawns a monster in a random lane on the right side of the field.
#    Assumes you will never place more than 5 monsters in one turn.
#---------------------------------------------------------------------
def spawn_monster(field, monster_list):
    while True:
      row=random.randint(0,len(field)-1)#largest num=4
      position=chr(ord('A')+row)+'7'
      result=place_unit(field,position,monster_list)
      if result==True:
        game_vars['num_monsters']+=1
        break
    return 

#-----------------------------------------
# save_game()
#
#    Saves the game in the file 'save.txt'
#-----------------------------------------
def save_game():
    path='C://Users//jingx//OneDrive//Documents//PRG 1 ASG game//'
    field_file=open(path+'game.txt','w')
    field_file.write(str(field))
            #save field only
    #save game_vars
    vars_file=open(path+'game_vars.txt','w')
    vars_file.write(str(game_vars))   
    vars_file.close()
    print("Game saved.")
    
#-----------------------------------------
# load_game()
#
#    Loads the game from 'save.txt'
#-----------------------------------------
def load_game(game_vars):
    config_file=open('game.txt','r')
    info=config_file.readline()
    save=info[0].strip('{').strip(']').strip(',')
    save=info[0].strip('\n')
    save.strip(']')
    field=info[1:]
  #attempt to load the game
    

    
    
    
    return

#-----------------------------------------------------
# initialize_game()
#
#    Initializes all the game variables for a new game
#-----------------------------------------------------
def initialize_game():
    game_vars['turn'] = 0
    game_vars['monster_kill_target'] = 20
    game_vars['monsters_killed'] = 0
    game_vars['num_monsters'] = 0
    game_vars['gold'] = 10
    

#-----------------------------------------
#               MAIN GAME
#-----------------------------------------

print("Desperate Defenders")
print("-------------------")
print("Defend the city from undead monsters!")
print()

# TO DO: ADD YOUR CODE FOR THE MAIN GAME HERE!
show_main_menu()
choice=int(input('Your Choice? '))
if choice==1:
    play_game=True
elif choice==2:
    play_game=True
    load_game(game_vars)
    
else:
    play_game=False
    
#In the process of playing the game
while play_game==True:
    #game_vars['gold']
    if game_vars['num_monsters']==0:
       spawn_monster(field,zombie)
    draw_field()
    show_combat_menu(game_vars)
    choice=int(input('Your Choice? '))
    if choice==1:
        buy_unit(field, game_vars)
    elif choice==2:
        for row in range(len(field)):
            for column in range(len(field[0])):
                if field[row][column]!=None: 
                    defender_attack(defender_list, field, row, column)
                    monster_advance(zombie, field, row, column) 
                    
    elif choice==3:
        save_game()
    elif choice==4:
        print('See you next time!')
        play_game=False
    else:
        continue
        
    game_vars['gold']+=1
    game_vars['turn']+=1
    game_vars['threat'] += random.randint(1,game_vars['danger_level'])
    if game_vars['turn'] %2==0:
            game_vars['danger_level'] += 1
            zombie['maxHP']+=1
    if game_vars['threat'] > 10:
            game_vars['threat'] = 0
            spawn_monster(field,zombie)

    if game_vars['monsters_killed']==20:
            print('You have protected the city! You win!')
            quit()
        
