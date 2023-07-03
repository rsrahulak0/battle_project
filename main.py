from classes.game import Person, bcolors
from classes.magic import spell
from classes.inventory import items
import random

# creating black magic
fire = spell("Fire", 25, 600, "Black")
thunder = spell("Thunder", 25, 600, "Black")
blizzard = spell("Blizzard", 25, 600, "Black")
meteor = spell("Meteor", 40, 1200, "Black")
quake = spell("Quake", 30, 1040, "Black")

# creating white magic
cure = spell("Cure", 25, 620, "White")
cura = spell("Cura", 32, 1500, "White")
curaga = spell("Curaga", 50, 6000, "White")

#creating some item:
potion = items("Potion", "potion", "heals 50 HP", 50)
hipotion = items("Hi-Potion", "Potion", "heals 100 HP", 100)
superpotion = items("Super Potion", "potion", "heals 500 HP", 1000)
elixer = items("Elixer", "elixer", "Fully restores HP/MP of one party member", 9999)
hielixer = items("MegaElixer", "elixer", "Fully restores party's HP/MP", 9999)

granade = items("Granade", "attack", "deals 500 damage", 500)

player_spells = [fire, thunder, blizzard, meteor, quake, cure, cura]
enemy_spell = [fire, meteor, curaga]
player_items = [{"item": potion, "quantity": 15}, {"item":hipotion, "quantity": 5},
                {"item": superpotion, "quantity": 5}, {"item":elixer, "quantity": 5},
                {"item": hielixer, "quantity": 2}, {"item":granade, "quantity": 5}]


# Instantiate People
player1 = Person("Gobu: ", 3200, 132, 300, 34, player_spells, player_items)
player2 = Person("Puggu:", 4000, 188, 311, 34, player_spells, player_items)
player3 = Person("Yogi: ", 3120, 174, 288, 34, player_spells, player_items)
# instantiate Enemy
enemy1 = Person("Batli:     ", 1250, 130, 500, 250, enemy_spell, [])
enemy2 = Person("Supernova: ", 11200, 701, 525, 300, enemy_spell, [])
enemy3 = Person("Sakura:    ", 1200, 130, 500, 250, enemy_spell, [])


players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]

running = True
i = 0

print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS!" + bcolors.ENDC)

while running:
    print("=====================")

    print("\n\n")
    print("NAME                 HP                                MP")
    for player in players:
        player.get_stats()
    print("\n")

    for enemy in enemies:
        enemy.get_enemy_stats()

    for player in players:

        player.choose_action()
        choice = input("     Choose Action")
        index = int(choice) - 1

        if index == 0:
            dmg = player.generate_damege()
            enemy = player.choose_target(enemies)

            enemies[enemy].take_damage(dmg)
            print("You Attack " + enemies[enemy].name.replace(" ", "") + "for", dmg, "points of damage.")

            if enemies[enemy].get_hp() == 0:
                print(enemies[enemy].name.replace(" ", "") + " has died")
                del enemies[enemy]

        elif index == 1:
            player.choose_magic()
            magic_choice = int(input("     Choose Magic:")) - 1

            if magic_choice == -1:
                continue

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()

            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(bcolors.FAIL + "\nNot enough MP\n" + bcolors.ENDC)
                continue

            player.reduce_mp(spell.cost)

            if spell.type == "White":
                players.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + "heals for", str(magic_dmg), "HP." + bcolors.ENDC)
            elif spell.type == "Black":

                enemy = player.choose_target(enemies)

                enemies[enemy].take_damage(magic_dmg)

                print(bcolors.OKBLUE + "\n" + spell.name + "deals", str(magic_dmg), "points of damage to " + enemies[enemy].name.replace(" ", "") + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace(" ", "") + " has died")
                    del enemies[enemy]

        elif index == 2:
            player.choose_item()
            item_choice = int(input("     Choose items: ")) -1

            if item_choice == -1:
                continue

            items = player.items[item_choice]["item"]

            if player.items[item_choice]["quantity"] == 0:
                print(bcolors.FAIL + "\n" + "None Left..." + bcolors.ENDC)
                continue

            player.items[item_choice]["quantity"] -= 1

            if items.type == "potion":
                player.heal(items.prop)
                print(bcolors.OKGREEN + "\n" + items.name + "heals for ", str(items.prop), "HP" + bcolors.ENDC)
            elif items.type == "elixer":

                if items.name == "MegaElixer":
                    for i in players:
                        i.hp = i.maxhp
                        i.mp = i.maxmp
                else:
                    player.hp = player.maxhp
                    player.mp = player.maxmp
                    print(bcolors.OKGREEN + "\n" + items.name + "fully restores HP/MP" + bcolors.ENDC)
            elif items.type == "attack":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(items.prop)

                print(bcolors.FAIL + "\n" + items.name + "deals", str(items.prop), "points of damage to   " + enemies[enemy].name.replace(" ", "") + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace(" ", "") + " has died")
                    del enemies[enemy]
    #check if battle is over
    defeated_enemies = 0
    defeated_players = 0
    for enemy in enemies:
        if enemy.get_hp() == 0:
            defeated_enemies += 1

    for player in players:
        if player.get_hp() == 0:
            defeated_players += 1

    #check if player won
    if defeated_enemies == 2:
        print(bcolors.OKGREEN + "You Win!" + bcolors.ENDC)
        running = False

    #check if enemy won
    elif defeated_players == 2:
        print(bcolors.FAIL + "You loose idiot now go home" + bcolors.ENDC)
        running = False

    print("\n")
    #Enemy attack phase
    for enemy in enemies:
        enemy_choice = random.randrange(0, 2)

        #Enemy Choose attack
        if enemy_choice ==0:
            target = random.randrange(0, 3)
            enemy_dmg = enemies[0].generate_damege()

            players[target].take_damage(enemy_dmg)
            print(enemy.name.replace(" ", "") + "attacks " + players[target].name.replace(" ", "") + "for",  enemy_dmg)
        elif enemy_choice == 1:

            spell = enemy.magic[magic_dmg]
            magic_dmg = spell.generate_damage()
            enemy.reduce_mp()
            if spell.type == "White":
                enemy.heal(magic_dmg)
            print(bcolors.OKBLUE + spell.name + "heals" + enemy.name + "for", str(magic_dmg), "HP" + bcolors.ENDC)

            if players[target].get_hp() == 0:
                print(players[target].name.replace(" ", "") + "has died")
                del players[player]


            #print("Enemy chose", spell, "damage is", magic_dmg)



