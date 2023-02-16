import json
import argparse
import random
import time

settings = {"F1TT": True, "F13CO": True, "FG": 6, "SG": 10, "BCTM": True}
parser = argparse.ArgumentParser()
parser.add_argument("--F1TT", required = False) #Defines if the first floor should be Traverse Town
parser.add_argument("--F13CO", required = False) #Defines if the last floor should be Castle Oblivion
parser.add_argument("--FG", required = False) #Defines the first goal floor
parser.add_argument("--SG", required = False) #Defines the second goal floor
parser.add_argument("--seed", required = False) #Defines the seed if you wish to use a specific seed
args = parser.parse_args()
if args.F1TT is not None:
    if args.F1TT == "False":
        settings["F1TT"] = False
if args.F13CO is not None:
    if args.F13CO == "False":
        settings["F13CO"] = False
if args.seed is not None:
    seed = args.seed
else:
    seed = time.time()
if args.FG is not None:
    settings["FG"] = args.FG
if args.SG is not None:
    settings["SG"] = args.SG

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

def reassign_battle_cards(seed):
    random.seed(a=seed)
    possible_battle_cards = load_json_data("battle_cards.json")["Battle Cards"]
    possible_battle_cards_values = []
    possible_battle_card_weights = []
    for card in possible_battle_cards:
        possible_battle_cards_values.append(card["Value"])
        possible_battle_card_weights.append(card["Weight"])
    battle_card_reassignments = {}
    for card in possible_battle_cards_values:
        battle_card_reassignments[card] = random.choices(possible_battle_cards_values, possible_battle_card_weights)
    return battle_card_reassignments

def reassign_battle_cards_type_for_type(seed):
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
    battle_card_reassignments = {}
    for card in possible_battle_cards_for_reassignment:
        for i_card in possible_battle_cards_for_reassignment:
            if type_reassignments[card["Type"]] == i_card["Type"] and card["Number"] == i_card["Number"]:
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

def reassign_key_rewards(seed, worlds, leftover_one_time_rewards):
    random.seed(a=seed)
    key_rewards = load_json_data("key_rewards.json")
    reward_pool = []
    locations = []
    rewards_to_be_placed = []
    rewards_placed = []
    reassignments = {}
    rewards_to_be_removed_from_rewards_to_be_placed = []
    for reward in leftover_one_time_rewards:
        reward_pool.append(reward["Value"])
    i = 0
    goals = [1, settings["FG"], settings["SG"], 12, 13]
    for goal in goals:
        print("Goal: " + str(goal))
        while i < goal:
            print(i)
            locations = locations + get_locations(key_rewards, worlds, i)
            for location in locations:  
                print("Location: " + str(location))
                if location["Value"].startswith("KO") and location["Value"] not in reward_pool and location["Value"] not in rewards_placed:
                    reward_pool.append(location["Value"])
                    #print("Added " + str(location["Value"]) + " to the reward pool")
            i = i + 1
        rewards_to_be_placed =[]
        rewards_to_be_placed = rewards_to_be_placed + ["KOB" + str(goal), "KOG" + str(goal), "KOT" + str(goal)]
        print(rewards_to_be_placed)
        reward_pool.remove("KOB" + str(goal))
        reward_pool.remove("KOG" + str(goal))
        reward_pool.remove("KOT" + str(goal))
        for reward in rewards_to_be_placed:
            print(reward)
            while reward not in rewards_placed:
                possible_location = random.choices(locations)[0]
                if reward not in possible_location["Requirements"]:
                    reassignments[possible_location["Value"]] = reward
                    rewards_placed.append(reward)
                    for requirement in possible_location["Requirements"]: 
                        if requirement not in rewards_placed and requirement not in rewards_to_be_placed and requirement in reward_pool:
                            rewards_to_be_placed.append(requirement)
                    for location in locations:
                        if reward == location and location != possible_location:
                            location["Requirements"] = location["Requirements"] + possible_location["Requirements"]
                    locations.remove(possible_location)
                    print("Removed location: " + str(possible_location))
                    if reward in reward_pool:
                        reward_pool.remove(reward)
        rewards_to_be_placed =[]
        for location in locations:
            print("This location: " + str(location))
            if len(reward_pool) > 0:
                while location["Value"] not in reassignments.keys():
                    reward = random.choices(reward_pool)[0]
                    print("Leftover: " + str(reward))
                    if reward not in location["Requirements"]:
                        reassignments[location["Value"]] = reward
                        rewards_placed.append(reward)
                        #locations.remove(location)
                        print("Removed location: " + str(location))
                        for requirement in location["Requirements"]: 
                            if requirement not in rewards_placed and requirement not in rewards_to_be_placed and requirement in reward_pool:
                                rewards_to_be_placed.append(requirement)
                        reward_pool.remove(reward)
        locations = []
    return reassignments

def reassign_key_rewards_2(seed, worlds, leftover_one_time_rewards, bottom_floor, top_floor):
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

def main():
    worlds = choose_worlds_for_each_floor(seed)
    if settings["BCTM"]:
        battle_card_reassignments = reassign_battle_cards_type_for_type(seed)
    else:
        battle_card_reassignments = reassign_battle_cards(seed)
    results = reassign_one_time_rewards(seed)
    one_time_rewards_reassignments = results[0]
    leftover_one_time_rewards = results[1]
    reassigned_key_rewards = reassign_key_rewards_2(seed, worlds, leftover_one_time_rewards, 1,1)
    remove_items_from_leftover_one_time_rewards(reassigned_key_rewards, leftover_one_time_rewards)
    reassigned_key_rewards.update(reassign_key_rewards_2(seed, worlds, leftover_one_time_rewards, 2,6))
    remove_items_from_leftover_one_time_rewards(reassigned_key_rewards, leftover_one_time_rewards)
    reassigned_key_rewards.update(reassign_key_rewards_2(seed, worlds, leftover_one_time_rewards, 7,10))
    remove_items_from_leftover_one_time_rewards(reassigned_key_rewards, leftover_one_time_rewards)
    reassigned_key_rewards.update(reassign_key_rewards_2(seed, worlds, leftover_one_time_rewards, 11,11))
    remove_items_from_leftover_one_time_rewards(reassigned_key_rewards, leftover_one_time_rewards)
    reassigned_key_rewards.update(reassign_key_rewards_2(seed, worlds, leftover_one_time_rewards, 12,12))
    remove_items_from_leftover_one_time_rewards(reassigned_key_rewards, leftover_one_time_rewards)
    reassigned_key_rewards.update(reassign_key_rewards_2(seed, worlds, leftover_one_time_rewards, 13,13))
    remove_items_from_leftover_one_time_rewards(reassigned_key_rewards, leftover_one_time_rewards)
    #reassigned_key_rewards = reassign_key_rewards(seed, worlds, leftover_one_time_rewards)
    item_reassignment_output = get_reassignments(worlds, battle_card_reassignments, one_time_rewards_reassignments, reassigned_key_rewards)
    output_reassignments(item_reassignment_output)
main()