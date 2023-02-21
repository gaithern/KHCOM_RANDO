import json
import random
import time
import PySimpleGUI as sg

settings = {"F1TT": True, "F13CO": True, "FG": 6, "SG": 10, "BCTM": True}

def load_json_data(filename):
    with open(filename) as json_file:
        data = json.load(json_file)
    return data

def choose_worlds_for_each_floor(seed):
    goals = [1,settings["FG"],7,settings["SG"],11,12,13]
    random.seed(a=seed)
    worlds = [None,None,None,None,None,None,None,None,None,None,None,None,None]
    possible_worlds = load_json_data("worlds.json")["Worlds"]
    i = 1 #index for world assignment
    
    worlds[6] = possible_worlds.pop(-1) #100 Acre Wood
    worlds[12] = possible_worlds.pop(-1) #Castle Oblivion
    worlds[10] = possible_worlds.pop(-1) #Twilight Town
    worlds[0] = possible_worlds.pop(-1) #Traverse Town
    worlds[11] = possible_worlds.pop(-1) #Destiny Islands
    target_index = len(possible_worlds)+1
    while i <= target_index:
        if i != 6:
            choice = random.randint(0,len(possible_worlds)-1)
            worlds[i] = possible_worlds.pop(choice)
        i = i + 1
    return worlds

def reassign_battle_cards(seed, zeroes_allowed, cures_allowed):
    random.seed(a=seed)
    possible_battle_cards = load_json_data("battle_cards.json")["Battle Cards"]
    possible_battle_cards_values = []
    possible_battle_card_weights = []
    for card in possible_battle_cards:
        possible_battle_cards_values.append(card["Value"])
        if (card["Name"][:-1] == 0 and zeroes_allowed == "No") or (card["Name"][:4] == "Cure" and cures_allowed == "No"):
            possible_battle_card_weights.append(0)
        else:
            possible_battle_card_weights.append(card["Weight"])
    battle_card_reassignments = {}
    for card in possible_battle_cards_values:
        battle_card_reassignments[card] = random.choices(possible_battle_cards_values, possible_battle_card_weights)
    return battle_card_reassignments

def reassign_battle_cards_type_for_type(seed, zeroes_allowed, cures_allowed):
    random.seed(a=seed)
    possible_battle_cards = load_json_data("battle_cards.json")["Battle Cards"]
    possible_battle_cards_for_reassignment = []
    card_types_reassigned = []
    for card in possible_battle_cards:
        possible_battle_cards_for_reassignment.append({"Value": card["Value"], "Weight": card["Weight"], "Type": card["Name"][:-2], "Number": card["Name"][-1]})
    possible_types = []
    for card in possible_battle_cards_for_reassignment:
        if card["Type"] not in possible_types:
            possible_types.append(card["Type"])
    type_reassignments = {}
    for type in possible_types:
        type_reassignments[type] = random.choice(possible_types)
        while type_reassignments[type] == "Cure" and cures_allowed == "No":
            type_reassignments[type] = random.choice(possible_types)
    battle_card_reassignments = {}
    for card in possible_battle_cards_for_reassignment:
        for i_card in possible_battle_cards_for_reassignment:
            if type_reassignments[card["Type"]] == i_card["Type"] and card["Number"] == i_card["Number"]:
                if zeroes_allowed == "No" and card["Number"] == "0":
                    battle_card_reassignments[card["Value"]] = [possible_battle_cards_for_reassignment[possible_battle_cards_for_reassignment.index(i_card)+1]["Value"]]
                else:
                    battle_card_reassignments[card["Value"]] = [i_card["Value"]]
    return battle_card_reassignments

def reassign_one_time_rewards(seed):
    random.seed(a=seed)
    possible_rewards = load_json_data("one_time_rewards.json")["One Time Rewards"]
    one_time_rewards_reassignments = []
    possible_sleights = []
    possible_enemy_cards = []
    for reward in possible_rewards:
        if reward["Type"] == "Sleight":
            possible_sleights.append(reward)
        if reward["Type"] == "Enemy Card":
            possible_enemy_cards.append(reward)
    possible_sleight_reassignments = possible_sleights.copy()
    possible_enemy_cards_reassignments = possible_enemy_cards.copy() + load_json_data("critical_rewards.json")["Critical Rewards"]
    for sleight in possible_sleights:
        one_time_rewards_reassignments.append({"OG": sleight, "RE": possible_sleight_reassignments.pop(random.randrange(0,len(possible_sleight_reassignments)))})
    for enemy_card in possible_enemy_cards:
        one_time_rewards_reassignments.append({"OG": enemy_card, "RE": possible_enemy_cards_reassignments.pop(random.randrange(0,len(possible_enemy_cards_reassignments)))})
    return [one_time_rewards_reassignments]+[possible_sleight_reassignments + possible_enemy_cards_reassignments]

def reassign_key_rewards(seed, worlds, leftover_one_time_rewards, bottom_floor, top_floor):
    random.seed(a=seed)
    key_rewards = load_json_data("key_rewards.json")
    battle_cards = load_json_data("battle_cards.json")
    reward_pool = []
    locations = []
    i = bottom_floor - 1
    solvable = False
    while i < top_floor:
        locations = locations + get_locations(key_rewards, worlds, i)
        i = i + 1
    while not solvable:
        reassignments = {}
        reward_pool = []
        key_pool = []
        for reward in leftover_one_time_rewards:
            reward_pool.append(reward["Value"])
        for location in locations:  
            if location["Value"].startswith("KO") and location["Value"] not in reward_pool:
                key_pool.append(location["Value"])
        #print(key_pool)
        goal_rewards = len(locations)
        for location in locations:
            if len(key_pool) != 0:
                reward = random.choice(key_pool)
                key_pool.remove(reward)
            elif len(reward_pool) != 0:
                reward = random.choice(reward_pool)
                reward_pool.remove(reward)
            else:
                reward = "001"
            reassignments[location["Value"]] = reward
        #print(reassignments)
        rewards_received = []
        attempts = 0
        while len(rewards_received) != goal_rewards and attempts < 50:
            for location in locations:
                can_receive_item = True
                for requirement in location["Requirements"]:
                    if requirement not in rewards_received:
                        can_receive_item = False
                if can_receive_item and reassignments[location["Value"]] not in rewards_received:
                    rewards_received.append(reassignments[location["Value"]])
            attempts = attempts + 1
        if len(rewards_received) == goal_rewards:
            solvable = True
        #else:
         #   print("Attempt not solvable, retrying")
    return reassignments

def get_locations(key_rewards, worlds, i):
    locations = []
    for reward in key_rewards[worlds[i]["Name"]]:
            reward["Reward"]["Floor Number"] = i+1
            if reward["Reward"]["Type"] == "Gold Map Card":
                match reward["Reward"]["Value"]["Type"]:
                    case "Key of Beginnings":
                        reward["Reward"]["Value"] = "KOB" + str(reward["Reward"]["Floor Number"])
                    case "Key of Guidance":
                        reward["Reward"]["Value"] = "KOG" + str(reward["Reward"]["Floor Number"])
                    case "Key to Truth":
                        reward["Reward"]["Value"] = "KOT" + str(reward["Reward"]["Floor Number"])
            else:
                reward["Reward"]["Value"] = reward["Reward"]["Value"]["Value"]
            for requirement in reward["Requirements"]:
                requirement["Floor Number"] = i+1
                if requirement["Type"] == "Gold Map Card":
                    match requirement["Value"]["Type"]:
                        case "Key of Beginnings":
                            requirement["Value"] = "KOB" + str(reward["Reward"]["Floor Number"])
                        case "Key of Guidance":
                            requirement["Value"] = "KOG" + str(reward["Reward"]["Floor Number"])
                        case "Key to Truth":
                            requirement["Value"] = "KOT" + str(reward["Reward"]["Floor Number"])
                else:
                    requirement["Value"] = requirement["Value"]["Value"]
            to_append = {"Value": reward["Reward"]["Value"], "Requirements": []}
            for requirement in reward["Requirements"]:
                to_append["Requirements"].append(requirement["Value"])
            locations.append(to_append)
    return locations

def get_reassignments(worlds, battle_card_reassignments, one_time_rewards_reassignments, reassigned_key_rewards):
    world_output = []
    item_reassignment_output = {}
    for world in worlds:
        world_output.append(world["Value"])
    for key in battle_card_reassignments.keys():
        item_reassignment_output[key] = battle_card_reassignments[key][0]
    for one_time_rewards_reassignment in one_time_rewards_reassignments:
        item_reassignment_output[one_time_rewards_reassignment["OG"]["Value"]] = one_time_rewards_reassignment["RE"]["Value"]
    for key in reassigned_key_rewards.keys():
        item_reassignment_output[key] = reassigned_key_rewards[key]
    item_reassignment_output["Worlds"] = world_output
    item_reassignment_output["Goals"] = [1,settings["FG"],7,settings["SG"],11,12,13]
    return item_reassignment_output

def output_reassignments(item_reassignments):
    json_object = json.dumps(item_reassignments, indent=4)
    with open('random.json', 'w') as f:
        f.write(json_object)

def remove_items_from_leftover_one_time_rewards(reassigned_key_rewards, leftover_one_time_rewards):
    for key in reassigned_key_rewards.keys():
        for reward in leftover_one_time_rewards:
            if reassigned_key_rewards[key] == reward["Value"]:
                leftover_one_time_rewards.remove(reward)

def initializations(seed, starting_deck, one_of_each_map_card, zeroes_allowed, cures_allowed):
    random.seed(a=seed)
    initializations = load_json_data("initializations.json")
    battle_cards = load_json_data("battle_cards.json")
    if starting_deck == "Randomize":
        valid = False
        while not valid:
            selected_cards = random.choices(battle_cards["Battle Cards"], k=10)
            cp_cost = 0
            for card in selected_cards:
                cp_cost = cp_cost + card["CP Cost"]
            if cp_cost <= 275:
                valid = True
                if zeroes_allowed == "No":
                    for card in selected_cards:
                        if card["Name"][-1] == "0":
                            valid = False
                if cures_allowed == "No":
                    for card in selected_cards:
                        if card["Name"][:4] == "Cure":
                            valid = False
            else:
                valid = False
        i = 0
        while i < len(selected_cards):
            selected_cards[i] = "1" + selected_cards[i]["Value"]
            i = i + 1
    else:
        selected_cards = [
            "1007"
            ,"1006"
            ,"1005"
            ,"1005"
            ,"1004"
            ,"1003"
            ,"1004"
            ,"1003"
            ,"1002"
            ,"1002"
            ,"1001"
            ,"1000"
            ,"10B9"
            ,"1182"
            ,"10CD"
        ]
    initializations["Starting Deck"] = selected_cards
    for color in initializations["Starting Map Cards"]:
        for card_type in initializations["Starting Map Cards"][color]:
            for card in card_type:
                if one_of_each_map_card == "Yes":
                    card["Quantity"] = 1
                else:
                    card["Quantity"] = 0
    json_object = json.dumps(initializations, indent=4)
    with open('initializations.json', 'w') as f:
        f.write(json_object)

def randomize(battle_cards, starting_deck, goal_floor_1, goal_floor_2, one_of_each_map_card, zeroes_allowed, cures_allowed, seed):
    seed = seed
    settings["FG"] = int(goal_floor_1)
    settings["SG"] = int(goal_floor_2)
    worlds = choose_worlds_for_each_floor(seed)
    battle_card_reassignments = {}
    if battle_cards == "Match Type for Type":
        battle_card_reassignments = reassign_battle_cards_type_for_type(seed, zeroes_allowed, cures_allowed)
    elif battle_cards == "Random":
        battle_card_reassignments = reassign_battle_cards(seed, zeroes_allowed, cures_allowed)
    results = reassign_one_time_rewards(seed)
    one_time_rewards_reassignments = results[0]
    leftover_one_time_rewards = results[1]
    reassigned_key_rewards = reassign_key_rewards(seed, worlds, leftover_one_time_rewards, 1,1)
    remove_items_from_leftover_one_time_rewards(reassigned_key_rewards, leftover_one_time_rewards)
    reassigned_key_rewards.update(reassign_key_rewards(seed, worlds, leftover_one_time_rewards, 2,6))
    remove_items_from_leftover_one_time_rewards(reassigned_key_rewards, leftover_one_time_rewards)
    reassigned_key_rewards.update(reassign_key_rewards(seed, worlds, leftover_one_time_rewards, 7,10))
    remove_items_from_leftover_one_time_rewards(reassigned_key_rewards, leftover_one_time_rewards)
    reassigned_key_rewards.update(reassign_key_rewards(seed, worlds, leftover_one_time_rewards, 11,11))
    remove_items_from_leftover_one_time_rewards(reassigned_key_rewards, leftover_one_time_rewards)
    reassigned_key_rewards.update(reassign_key_rewards(seed, worlds, leftover_one_time_rewards, 12,12))
    remove_items_from_leftover_one_time_rewards(reassigned_key_rewards, leftover_one_time_rewards)
    reassigned_key_rewards.update(reassign_key_rewards(seed, worlds, leftover_one_time_rewards, 13,13))
    remove_items_from_leftover_one_time_rewards(reassigned_key_rewards, leftover_one_time_rewards)
    item_reassignment_output = get_reassignments(worlds, battle_card_reassignments, one_time_rewards_reassignments, reassigned_key_rewards)
    output_reassignments(item_reassignment_output)
    initializations(seed, starting_deck, one_of_each_map_card, zeroes_allowed, cures_allowed)
#randomize()


sg.theme('DarkAmber')

layout = [  [sg.Text("Battle Cards", size = (20,1)), sg.Combo(["Vanilla", "Random", "Match Type for Type"], default_value = "Vanilla")],
            [sg.Text("Starting Deck", size = (20,1)), sg.Combo(["Vanilla", "Randomize"], default_value = "Vanilla")],
            [sg.Text("Goal Floor 1", size = (20,1)), sg.Combo(["6"], default_value = "6")],
            [sg.Text("Goal Floor 2", size = (20,1)), sg.Combo(["10"], default_value = "10")],
            [sg.Text("One of Each Map Card", size = (20,1)), sg.Combo(["Yes", "No"], default_value = "Yes")],
            [sg.Text("0s Allowed", size = (20,1)), sg.Combo(["Yes", "No"], default_value = "Yes")],
            [sg.Text("Cure Allowed", size = (20,1)), sg.Combo(["Yes", "No"], default_value = "Yes")],
            [sg.Text("Seed", size = (20,1)), sg.InputText(str(time.time()))],
            [sg.Button("Generate json", key="Randomize")]
         ]

window = sg.Window("KHCOM_RANDO", layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == "Cancel":
        break
    elif event == "Randomize":
        randomize(values[0], values[1], values[2], values[3], values[4], values[5], values[6], values[7])