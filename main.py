from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item
import random

# Create Attack Spells
facts = Spell("Facts", 35, 600, "black")
doctors = Spell("Doctors", 35, 600, "black")
professors = Spell("Professors", 50, 1200, "black")
ok_boomer = Spell("Ok Boomer", 50, 1200, "black")
disrespect = Spell("Disrespect", 14, 340, "black")
little_karen = Spell("Little-Karen", 35, 600, "black")
facebook_post = Spell("Facebook-Post", 50, 1200, "black")
fake_news = Spell("Fake-News", 40, 800, "black")
your_attacking_me = Spell("You're aTtAckinG Me", 35, 600, "black")


# Create Healing Spells
medicine = Spell("Medicine", 25, 620, "white")
take_vaccine = Spell("Vaccine", 40, 1500, "white")
support_karens = Spell("Karen Support Group", 50, 6000, "white")

# Create Items
coke = Item("Coke", "potion", "Heals 50 HP", 50)
diet_coke = Item("Diet Coke", "potion", "Heals 100 HP", 100)
mountain_dew = Item("Mountain Dew", "potion", "Heals 1000 HP", 1000)
boba = Item("Boba", "elixir", "Fully restores HP/MP of one party member", 99)
tea = Item("Tea", "elixir", "Fully restores HP/MP of all parties", 99)
vaccine = Item("Vaccine", "attack", "Deals 500 dmg", 500)

player_spells = [facts, doctors, professors, ok_boomer, disrespect, medicine, take_vaccine]
enemy_spells = [little_karen, facebook_post, fake_news, your_attacking_me, support_karens]
player_items = [{"item": coke, "quantity": 15}, {"item": diet_coke, "quantity": 5},
                {"item": mountain_dew, "quantity": 2},
                {"item": boba, "quantity": 5}, {"item": tea, "quantity": 1}, {"item": vaccine, "quantity": 5}]
# People
player1 = Person("Salle:", 6260, 120, 500, 104, player_spells, player_items)
player2 = Person("Sally:", 5560, 180, 410, 94, player_spells, player_items)
player3 = Person("Sallo:", 4100, 165, 380, 114, player_spells, player_items)

enemy1 = Person("Karen1", 18200, 175, 545, 125, enemy_spells, [])
enemy2 = Person("Karen2", 5200, 130, 360, 75, enemy_spells, [])
enemy3 = Person("Karen3", 5200, 130, 360, 75, enemy_spells, [])

players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]

running = True
i = 0

print(bcolors.FAIL + bcolors.BOLD + "An Enemy Attacks" + bcolors.ENDC)

while running:
    print("=========================================")

    print("\n\n")
    print(bcolors.BOLD + "Name                    HP                                   MP" + bcolors.ENDC)
    for player in players:
        player.get_stats()

    print("\n")

    for enemy in enemies:
        enemy.get_enemy_stats()

    for player in players:

        player.choose_action()
        choice = input("Choose action: ")
        index = int(choice) - 1
        print("You chose", choice)

        if index == 0:
            enemy = player.choose_target(enemies)
            dmg = player.generate_damage() - enemies[enemy].df

            enemies[enemy].take_damage(dmg)
            print("You attacked " + enemies[enemy].name.replace(" ", "") + " for", dmg, "points of damage.")

            if enemies[enemy].get_hp() == 0:
                print(enemies[enemy].name.replace(" ", "") + " has been defeated!")
                del enemies[enemy]

        elif index == 1:
            player.choose_magic()
            magic_choice = int(input("Choose magic: ")) - 1

            if magic_choice == -1:
                continue

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()

            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(bcolors.FAIL + "\nNot enough mp\n" + bcolors.ENDC)
                continue
            player.reduce_mp(spell.cost)

            if spell.type == "white":
                player.heal(magic_dmg)
                print(bcolors.OKBLUE + "\n" + spell.name + " heals for " + str(magic_dmg), "HP. " + bcolors.ENDC)
            elif spell.type == "black":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(magic_dmg - enemies[enemy].df)
                print(bcolors.OKBLUE + "\n" + spell.name + " deals for " + str(magic_dmg),
                      "points of damage to " + enemies[enemy].name.replace(" ", "") + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace(" ", "") + " has been defeated!")
                    del enemies[enemy]

        elif index == 2:
            player.choose_item()
            item_choice = int(input("Choose item: ")) - 1

            if item_choice == -1:
                continue

            item = player.items[item_choice]["item"]

            if player.items[item_choice]["quantity"] == 0:
                print(bcolors.FAIL + "\n" + "None left" + bcolors.ENDC)

            player.items[item_choice]["quantity"] -= 1

            if item.type == "potion":
                player.heal(item.prop)
                print(bcolors.OKGREEN + "\n" + item.name + " heals for ", str(item.prop), "HP" + bcolors.ENDC)

            elif item.type == "elixir":
                if item.name == "Mega-Elixir":
                    for i in players:
                        i.hp = i.maxhp
                        i.mp = i.maxmp
                    print(bcolors.OKGREEN + "\n" + item.name + " fully restores full party's HP/MP " + bcolors.ENDC)
                else:
                    player.hp = player.maxhp
                    player.mp = player.maxmp
                    print(bcolors.OKGREEN + "\n" + item.name + " fully restores HP/MP " + bcolors.ENDC)

            elif item.type == "attack":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(item.prop - enemies[enemy].df)
                print(bcolors.FAIL + "\n" + item.name + " deals for ", str(item.prop), "points of dmg to " + enemies[enemy].name.replace(" ", "") + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(enemies[enemy].name.replace(" ", "") + " has been defeated!")
                    del enemies[enemy]

    # Check if battle is over
    defeated_enemies = 0
    defeated_players = 0

    print("\n")

    for enemy in enemies:
        if enemy.get_hp() == 0:
            defeated_enemies += 1

    for player in players:
        if player.get_hp() == 0:
            defeated_players += 1
    # Check if player won
    if defeated_enemies == 2:
        print(bcolors.OKGREEN + "You have defeated all the Karens...for now" + bcolors.ENDC)
        running = False
    # Check if enemy has won
    elif defeated_players == 2:
        print(bcolors.FAIL + "The Karens have defeated you...unfortunately" + bcolors.ENDC)
        running = False

    for enemy in enemies:
        pct = enemy.hp / enemy.maxhp * 100
        if pct < 30 < enemy.mp:
            enemy_choice = 1
        elif pct < 30 and enemy.mp <= 35:
            enemy_choice = 0
        else:
            enemy_choice = random.randrange(0, 2)

        if enemy_choice == 0:

            target = random.randrange(0, len(players))
            enemy_dmg = enemy.generate_damage() - players[target].df
            if len(players) == 0:
                print(bcolors.FAIL + "The Karens have defeated you...unfortunately" + bcolors.ENDC)
                running = False
            players[target].take_damage(enemy_dmg)
            print(bcolors.FAIL + enemy.name.replace(" ", "") + " slaps " + players[target].name.replace(":", "") + " for " + str(enemy_dmg) + " points of damage." + bcolors.ENDC)
            if players[target].get_hp() == 0:
                print(players[target].name.replace(":", " ") + "'s brain has died from " + enemy.name.replace(" ", "") + "'s karenness")
                del players[target]

        elif enemy_choice == 1:
            pct = enemy.hp / enemy.maxhp * 100

            if pct < 30:
                magic_choice = 4
                spell = enemy.magic[magic_choice]
                magic_dmg = spell.generate_damage()
                if enemy.mp < spell.cost:
                    continue
                else:
                    enemy.reduce_mp(spell.cost)
                    enemy.heal(magic_dmg)
                    print(bcolors.OKBLUE + spell.name + " heals " + enemy.name.replace(" ", "") + " for " + str(magic_dmg),
                          "HP. " + bcolors.ENDC)
            elif pct > 30:
                magic_choice = random.randrange(0, 3)
                spell = enemy.magic[magic_choice]
                magic_dmg = spell.generate_damage()
                if enemy.mp < spell.cost:
                    continue
                enemy.reduce_mp(spell.cost)
                target = random.randrange(0, len(players))
                if len(players) == 0:
                    print(bcolors.FAIL + "The Karens have defeated you...unfortunately" + bcolors.ENDC)
                    running = False
                players[target].take_damage(magic_dmg - players[target].df)
                print(bcolors.OKBLUE + enemy.name.replace(" ", "") + " slaps " + players[target].name.replace(":", "") + " with " + spell.name + " for " + str(magic_dmg),
                      "points of damage." + bcolors.ENDC)

                if players[target].get_hp() == 0:
                    print(players[target].name.replace(":", " ") + "'s brain has died from " + enemy.name.replace(" ", "") + "'s karenness")
                    del players[target]












