JSON = require("JSON")

function load_json(filename)
	f = io.open(filename, "r")
	io.input(f)
	txt = io.read("*all")
	loaded_dict = JSON:decode(txt)
	return loaded_dict
end

function to_hex(input_str)
	return tonumber(input_str,16)
end

function DEC_HEX(IN)
    local B,K,OUT,I,D=16,"0123456789ABCDEF","",0
    while IN>0 do
        I=I+1
        IN,D=math.floor(IN/B),math.mod(IN,B)+1
        OUT=string.sub(K,D,D)..OUT
    end
    return OUT
end

function lpad_string(pad_number, pad_value, x)
	if pad_number > string.len(x) then
		local target = pad_number - string.len(x)
		local i = 0
		while i < target do
			x = pad_value .. x
			i = i + 1
		end
	end
	return x
end

function toBits(num,bits)
    -- returns a table of bits, most significant first.
    bits = bits or math.max(1, select(2, math.frexp(num)))
    local t = {} -- will contain the bits        
    for b = bits, 1, -1 do
        t[b] = math.fmod(num, 2)
        num = math.floor((num - t[b]) / 2)
    end
    return t
end

function get_length_table(x)
	cnt = 0
	for k,v in pairs(x) do
		cnt = cnt + 1
	end
	return cnt
end

function difference(a, b)
    local ai = {}
    local r = {}
    for k,v in pairs(a) do r[k] = v; ai[v]=true end
    for k,v in pairs(b) do 
        if ai[v]~=nil then   r[k] = nil   end
    end
    return r
end

function copy_table(source)
	local table_copy = {}
	for k,v in pairs(source) do
		table_copy[k] = v
	end
	return table_copy
end

function load_dictionaries()
	addresses = load_json("addresses.json")
	randomization = load_json("random.json")
	char_to_hex_map = load_json("char_to_hex_map.json")
	types = load_json("types.json")
	binary_to_hex = load_json("binary_to_hex.json")
	initializations = load_json("initializations.json")
end

function get_floor_number()
	local floor_number = memory.readbyte(to_hex(addresses["Floor Number"]["Address"])) + 1
	return floor_number
end

function set_floor_number(x)
	memory.writebyte(to_hex(addresses["Floor Number"]["Address"]),to_hex(x-1))
end

function get_highest_warp_floor_number()
	local highest_warp_floor_number = (memory.readbyte(to_hex(addresses["Highest Warp Floor"]["Address"])) / 2) + 1
	return highest_warp_floor_number
end

function set_highest_wrap_floor_number(x)
	x = x-1
	local highest_warp_floor_number = memory.writebyte(to_hex(addresses["Highest Warp Floor"]["Address"]), x*2)
end

function get_current_gold_card_qty(gold_card_type)
	local num_of_gold_cards = memory.readbyte(to_hex(addresses["Map Cards"]["Gold"][gold_card_type]["Address"]))
	return num_of_gold_cards
end

function set_current_gold_card_qty(gold_card_type, x)
	memory.writebyte(to_hex(addresses["Map Cards"]["Gold"][gold_card_type]["Address"]),to_hex(x))
end

function get_stored_gold_cards(gold_card_type, floor_number)
	local num_of_gold_cards = memory.readbyte(to_hex(addresses["Map Cards"]["Stored Gold Cards"][gold_card_type][floor_number]["Address"]))
	if floor_number >= 10 then
		if num_of_gold_cards == 2 or num_of_gold_cards == 3 then
			num_of_gold_cards = 1
		else
			num_of_gold_cards = 0
		end
	elseif floor_number <= 4 then
		if num_of_gold_cards == 1 or num_of_gold_cards == 3 then
			num_of_gold_cards = 1
		else
			num_of_gold_cards = 0
		end
	end
	return num_of_gold_cards
end

function set_stored_gold_cards(gold_card_type, floor_number, x)
	local num_of_gold_cards = memory.readbyte(to_hex(addresses["Map Cards"]["Stored Gold Cards"][gold_card_type][floor_number]["Address"]))
	if x > 0 then
		if floor_number >= 10 then
			if num_of_gold_cards == 0 then
				memory.writebyte(to_hex(addresses["Map Cards"]["Stored Gold Cards"][gold_card_type][floor_number]["Address"]), 2)
			elseif num_of_gold_cards == 1 then
				memory.writebyte(to_hex(addresses["Map Cards"]["Stored Gold Cards"][gold_card_type][floor_number]["Address"]), 3)
			elseif num_of_gold_cards == 2 then
				memory.writebyte(to_hex(addresses["Map Cards"]["Stored Gold Cards"][gold_card_type][floor_number]["Address"]), 2)
			elseif num_of_gold_cards == 3 then
				memory.writebyte(to_hex(addresses["Map Cards"]["Stored Gold Cards"][gold_card_type][floor_number]["Address"]), 3)
			end
		elseif floor_number <= 4 then
			if num_of_gold_cards == 0 then
				memory.writebyte(to_hex(addresses["Map Cards"]["Stored Gold Cards"][gold_card_type][floor_number]["Address"]), 1)
			elseif num_of_gold_cards == 1 then
				memory.writebyte(to_hex(addresses["Map Cards"]["Stored Gold Cards"][gold_card_type][floor_number]["Address"]), 1)
			elseif num_of_gold_cards == 2 then
				memory.writebyte(to_hex(addresses["Map Cards"]["Stored Gold Cards"][gold_card_type][floor_number]["Address"]), 3)
			elseif num_of_gold_cards == 3 then
				memory.writebyte(to_hex(addresses["Map Cards"]["Stored Gold Cards"][gold_card_type][floor_number]["Address"]), 3)
			end
		else
			memory.writebyte(to_hex(addresses["Map Cards"]["Stored Gold Cards"][gold_card_type][floor_number]["Address"]), 1)
		end
	elseif x == 0 then
		if floor_number >= 10 then
			if num_of_gold_cards == 0 then
				memory.writebyte(to_hex(addresses["Map Cards"]["Stored Gold Cards"][gold_card_type][floor_number]["Address"]), 0)
			elseif num_of_gold_cards == 1 then
				memory.writebyte(to_hex(addresses["Map Cards"]["Stored Gold Cards"][gold_card_type][floor_number]["Address"]), 1)
			elseif num_of_gold_cards == 2 then
				memory.writebyte(to_hex(addresses["Map Cards"]["Stored Gold Cards"][gold_card_type][floor_number]["Address"]), 0)
			elseif num_of_gold_cards == 3 then
				memory.writebyte(to_hex(addresses["Map Cards"]["Stored Gold Cards"][gold_card_type][floor_number]["Address"]), 1)
			end
		elseif floor_number <= 4 then
			if num_of_gold_cards == 0 then
				memory.writebyte(to_hex(addresses["Map Cards"]["Stored Gold Cards"][gold_card_type][floor_number]["Address"]), 0)
			elseif num_of_gold_cards == 1 then
				memory.writebyte(to_hex(addresses["Map Cards"]["Stored Gold Cards"][gold_card_type][floor_number]["Address"]), 0)
			elseif num_of_gold_cards == 2 then
				memory.writebyte(to_hex(addresses["Map Cards"]["Stored Gold Cards"][gold_card_type][floor_number]["Address"]), 2)
			elseif num_of_gold_cards == 3 then
				memory.writebyte(to_hex(addresses["Map Cards"]["Stored Gold Cards"][gold_card_type][floor_number]["Address"]), 2)
			end
		else
			memory.writebyte(to_hex(addresses["Map Cards"]["Stored Gold Cards"][gold_card_type][floor_number]["Address"]), 0)
		end
	end
end

function get_battle_card(offset)
	local battle_card = {}
	
	local battle_card_data = memory.read_u16_le(to_hex(addresses["Battle Cards"]["Address"]) + (2 * offset))
	battle_card["Raw Value"] = lpad_string(4, "0", DEC_HEX(battle_card_data))
	battle_card["Value"] = string.sub(battle_card["Raw Value"], -3)
	battle_card["Offset"] = offset
	if toBits(battle_card_data, 16)[1] == 1 then
		battle_card["Is Premium"] = true
	else
		battle_card["Is Premium"] = false
	end
	if toBits(battle_card_data, 16)[2] == 1 or toBits(battle_card_data, 16)[3] == 1 or toBits(battle_card_data, 16)[4] == 1 then
		battle_card["Is Used"] = true
	else
		battle_card["Is Used"] = false
	end
	return battle_card
end

function get_battle_cards()
	i = 0
	j = 1
	local battle_cards = {}
	while i < addresses["Battle Cards"]["Bytes"]/2 do
		local battle_card = get_battle_card(i)
		if battle_card["Raw Value"] ~= "0FFF" then
			battle_cards[j] = battle_card
		end
		j = j + 1
		i = i + 1
	end
	return battle_cards
end

function remove_battle_card(card_value, premium)
	cards = get_battle_cards()
	finished = false
	--for k,v in pairs(cards) do
		--if v["Value"] == card_value and v["Is Used"] then
			--print("Removing this card might cause problems with memory.  For now we'll skip this card")
			--finished = true
		--end
	--end
	if not finished then
		for k,v in pairs(cards) do
			if v["Value"] == card_value and not v["Is Used"] and v["Is Premium"] == premium and not finished then
				memory.write_u16_le(to_hex(addresses["Battle Cards"]["Address"]) + (2 * v["Offset"]), 0x0FFF)
				finished = true
			end
		end
		if not finished then
			print("Error!  Card not found!")
		end
	end
end

function find_empty_battle_card_offset()
	local i = 0
	while i < addresses["Battle Cards"]["Bytes"]/2 do
		local battle_card = get_battle_card(i)
		if battle_card["Raw Value"] == "0FFF" then
			return battle_card["Offset"]
		end
		i = i + 1
	end
end

function add_battle_card(card_value, premium)
	local offset = find_empty_battle_card_offset()
	if premium then
		memory.write_u16_le(to_hex(addresses["Battle Cards"]["Address"]) + (2 * offset), to_hex("8"..card_value))
	else
		memory.write_u16_le(to_hex(addresses["Battle Cards"]["Address"]) + (2 * offset), to_hex("0"..card_value))
	end
end

function get_battle_unused_card_counts(battle_cards)
	local battle_card_counts = {}
	for k,v in pairs(battle_cards) do
		if not v["Is Used"] then
			local found = false
			for ik, iv in pairs(battle_card_counts) do
				if ik == v["Raw Value"] then
					battle_card_counts[ik] = battle_card_counts[ik] + 1
					found = true
				end
			end
			if not found then
				battle_card_counts[v["Raw Value"]] = 1
			end
		end
	end
	return battle_card_counts
end

function find_new_battle_cards(old_battle_cards, current_battle_cards)
	local new_battle_cards = {}
	local new_premium_battle_cards = {}
	regular_index = 1
	premium_index = 1
	for k,v in pairs(current_battle_cards) do
		local found = false
		for ik,iv in pairs(old_battle_cards) do
			if k == ik then
				found = true
			end
		end
		if not found then
			if v["Is Premium"] then
				new_premium_battle_cards[premium_index] = v["Value"]
				premium_index = premium_index + 1
			else
				new_battle_cards[regular_index] = v["Value"]
				regular_index = regular_index + 1
			end
		end
	end
	local new_cards = {}
	new_cards["Regular"] = new_battle_cards
	new_cards["Premium"] = new_premium_battle_cards
	return new_cards
end

function get_sleights()
	local sleights = {}
	i = 1
	for k,v in pairs(addresses["Sleights"]) do
		local sleight_byte = memory.readbyte(to_hex(v["Address"]["Address"]))
		local sleight_bits = toBits(sleight_byte, 8)
		for ik,iv in pairs(sleight_bits) do
			if iv == 1 then
				sleights[i] = v["Bits"][ik]
				i = i + 1
			end
		end
	end
	return sleights
end

function add_sleight(sleight)
	for k,v in pairs(addresses["Sleights"]) do
		for ik, iv in pairs(v["Bits"]) do
			if sleight == iv then
				address = v["Address"]["Address"]
				bit_num = ik
			end
		end
	end
	local hex_byte = memory.readbyte(to_hex(address))
	local hex_bits = toBits(hex_byte, 8)
	hex_bits[bit_num] = 1
	local new_hex_char_1 = binary_to_hex[tostring(hex_bits[1])..tostring(hex_bits[2])..tostring(hex_bits[3])..tostring(hex_bits[4])]
	local new_hex_char_2 = binary_to_hex[tostring(hex_bits[5])..tostring(hex_bits[6])..tostring(hex_bits[7])..tostring(hex_bits[8])]
	local new_hex_char = new_hex_char_1..new_hex_char_2
	memory.writebyte(to_hex(address), to_hex(new_hex_char))
end

function remove_sleight(sleight)
	for k,v in pairs(addresses["Sleights"]) do
		for ik, iv in pairs(v["Bits"]) do
			if sleight == iv then
				address = v["Address"]["Address"]
				bit_num = ik
			end
		end
	end
	local hex_byte = memory.readbyte(to_hex(address))
	local hex_bits = toBits(hex_byte, 8)
	hex_bits[bit_num] = 0
	local new_hex_char_1 = binary_to_hex[tostring(hex_bits[1])..tostring(hex_bits[2])..tostring(hex_bits[3])..tostring(hex_bits[4])]
	local new_hex_char_2 = binary_to_hex[tostring(hex_bits[5])..tostring(hex_bits[6])..tostring(hex_bits[7])..tostring(hex_bits[8])]
	local new_hex_char = new_hex_char_1..new_hex_char_2
	memory.writebyte(to_hex(address), to_hex(new_hex_char))
end

function find_new_sleights(old_sleights, current_sleights)
	new_sleights = {}
	i = 1
	for k,v in pairs(current_sleights) do
		local found = false
		for ik, iv in pairs(old_sleights) do
			if v == iv then
				found = true
			end
		end
		if not found then
			new_sleights[i] = v
			i = i + 1
		end
	end
	return new_sleights
end

function set_floors()
	for k,v in pairs(randomization["Worlds"]) do
		memory.writebyte(to_hex(addresses["Floors"][k]["Assigned World"]["Address"]), to_hex(v))
	end
end

function handle_highest_warp()
	local floor_number = get_floor_number()
	for k,v in pairs(randomization["Goals"]) do
		if floor_number <= v then
			set_highest_wrap_floor_number(v)
			return
		end
	end
end

function find_new_keys(old_keys, current_keys, gold_card_type, floor_number)
	local new_keys = {}
	if current_keys > old_keys then
		new_keys[1] = gold_card_type .. tostring(floor_number)
	end
	return new_keys
end

function combine_new_keys(new_keys_1, new_keys_2, new_keys_3)
	local new_keys = {}
	i = 1
	for k,v in pairs(new_keys_1) do
		new_keys[i] = v
		i = i + 1
	end
	for k,v in pairs(new_keys_2) do
		new_keys[i] = v
		i = i + 1
	end
	for k,v in pairs(new_keys_3) do
		new_keys[i] = v
		i = i + 1
	end
	return new_keys
end

function handle_new_items(new_battle_cards, new_premium_battle_cards, new_keys, new_sleights)
	for k,v in pairs(new_battle_cards) do
		for ik,iv in pairs(randomization) do
			if v == ik then
				for iik, iiv in pairs(types) do
					if iv == iik then
						print("Replacing BC: " .. tostring(v))
						local new_item_type = iiv
						if new_item_type == "Key" then
							local key_type = string.sub(iv,1,3)
							local key_floor = tonumber(string.sub(iv,4))
							set_stored_gold_cards(key_type, key_floor, 1)
							remove_battle_card(v, false)
							print("Got GC: " .. tostring(iv))
						elseif new_item_type == "Sleight" then
							add_sleight(iv)
							remove_battle_card(v, false)
							print("Got SL: " .. tostring(iv))
						elseif new_item_type == "Battle Card" then
							remove_battle_card(v, false)
							add_battle_card(iv, false)
							print("Got BC: " .. tostring(iv))
						end
					end
				end
			end
		end
	end
	
	for k,v in pairs(new_premium_battle_cards) do
		for ik,iv in pairs(randomization) do
			if v == ik then
				for iik, iiv in pairs(types) do
					if iv == iik then
						print("Replacing PBC: " .. tostring(v))
						local new_item_type = iiv
						if new_item_type == "Key" then
							local key_type = string.sub(iv,1,3)
							local key_floor = tonumber(string.sub(iv,4))
							set_stored_gold_cards(key_type, key_floor, 1)
							remove_battle_card(v, true)
							print("Got GC: " .. tostring(iv))
						elseif new_item_type == "Sleight" then
							add_sleight(iv)
							remove_battle_card(v, true)
							print("Got SL: " .. tostring(iv))
						elseif new_item_type == "Battle Card" then
							remove_battle_card(v, true)
							add_battle_card(iv, true)
							print("Got PBC: " .. tostring(iv))
						end
					end
				end
			end
		end
	end
	
	for k,v in pairs(new_sleights) do
		for ik,iv in pairs(randomization) do
			if v == ik then
				for iik, iiv in pairs(types) do
					if iv == iik then
						print("Replacing SL: " .. tostring(v))
						local new_item_type = iiv
						if new_item_type == "Key" then
							local key_type = string.sub(iv,1,3)
							local key_floor = tonumber(string.sub(iv,4))
							set_stored_gold_cards(key_type, key_floor, 1)
							remove_sleight(v)
							print("Got GC: " .. tostring(iv))
						elseif new_item_type == "Sleight" then
							add_sleight(iv)
							remove_sleight(v)
							print("Got SL: " .. tostring(iv))
						elseif new_item_type == "Battle Card" then
							add_battle_card(iv, false)
							remove_sleight(v)
							print("Got BC: " .. tostring(iv))
						end
					end
				end
			end
		end
	end
	
	for k,v in pairs(new_keys) do
		local this_key_type = string.sub(v,1,3)
		local this_key_floor = string.sub(v,4)
		for ik,iv in pairs(randomization) do
			if v == ik then
				for iik, iiv in pairs(types) do
					if iv == iik then
						print("Replacing GC: " .. tostring(v))
						local new_item_type = iiv
						if new_item_type == "Key" then
							local key_type = string.sub(iv,1,3)
							local key_floor = tonumber(string.sub(iv,4))
							set_stored_gold_cards(key_type, key_floor, 1)
							set_current_gold_card_qty(key_type, get_current_gold_card_qty(key_type)-1)
							print("Got GC: " .. tostring(iv))
						elseif new_item_type == "Sleight" then
							add_sleight(iv)
							set_current_gold_card_qty(key_type, get_current_gold_card_qty(key_type)-1)
							print("Got SL: " .. tostring(iv))
						elseif new_item_type == "Battle Card" then
							add_battle_card(iv, false)
							set_current_gold_card_qty(key_type, get_current_gold_card_qty(key_type)-1)
							print("Got BC: " .. tostring(iv))
						end
					end
				end
			end
		end
	end
					
end

function get_playtime()
	local playtime = memory.read_u24_le(to_hex(addresses["Playtime"]["Address"]))
	return playtime
end

function save_or_savestate_loaded(saved_playtime, current_playtime)
	if current_playtime >= saved_playtime then
		if (current_playtime - saved_playtime) < 3 then
			return false
		end
	end
	print("Save or Savestate Loaded... Ignoring Changes")
	return true
end

function clean_garbage_cards()
	--Not sure what is adding these, but until I figure it out, I'll use this to clean them up
	local current_battle_cards = get_battle_cards()
	for k,v in pairs(current_battle_cards) do
		local found = false
		for ik,iv in pairs(types) do
			if v["Value"] == ik then
				found = true
			end
		end
		if not found then
			remove_battle_card(v["Value"], v["Is Premium"])
		end
	end
end

function sleights_temporarily_removed()
	local sleights = get_sleights()
	if get_length_table(sleights) == 0 then
		return true
	end
	return false
end

function get_deck_pointer(deck_number, offset)
	local deck_pointer = DEC_HEX(memory.read_u16_le(to_hex(addresses["Deck Card Pointers"][deck_number]["Address"]) + 2*offset))
	if deck_pointer == "" then
		return "0"
	else
		return deck_pointer
	end
end

function get_deck_pointers()
	local deck_pointers = {}
	i = 1
	while i <= get_length_table(addresses["Deck Card Pointers"]) do
		deck_pointers[i] = {}
		j = 1
		k = 1
		finished = false
		while not finished and k < 100 do
			local deck_pointer = get_deck_pointer(i, j-1)
			if deck_pointer == "FFFF" then
				finished = true
			else
				deck_pointers[i][j] = deck_pointer
				j = j+1
			end
			k = k + 1
		end
		i = i+1
	end
	return deck_pointers
end

function set_deck_pointer(deck_number, offset, value)
	memory.write_u16_le(to_hex(addresses["Deck Card Pointers"][deck_number]["Address"]) + 2*offset, to_hex(value))
end

function reassign_deck_pointers(old_deck_pointers)
	for k,v in pairs(old_deck_pointers) do
		for ik,iv in pairs(v) do
			set_deck_pointer(k, ik-1, iv)
		end
	end
end

function set_starting_deck()
	for k,v in pairs(initializations["Starting Deck"]) do
		memory.write_u16_le(to_hex(addresses["Battle Cards"]["Address"]) + 2*(k-1), to_hex(v))
	end
end

function replace_text(address, bytes, new_text)
	local replacement_bytes = {}
	j = 1
	for i = 1, #new_text do
		local c = new_text:sub(i,i)
		replacement_bytes[j] = char_to_hex_map[c]
		replacement_bytes[j+1] = "00"
		j = j + 2
		i = i + 1
	end
	i = 0
	while i < bytes do
		memory.writebyte(to_hex(address) + i, to_hex("00"))
		i = i + 1
	end
	i = 0
	while i < get_length_table(replacement_bytes) do
		memory.writebyte(to_hex(address) + i, to_hex(replacement_bytes[i+1]))
		i = i + 1
	end
end

function set_key_description_text()
	i=1
	local new_string = ""
	while i <= 13 do
		if get_stored_gold_cards("KOB", i)  == 1 then
			new_string = new_string .. tostring(i) .. ","
		end
		i = i + 1
	end
	if new_string ~= "" then
		new_string = new_string:sub(1,-2)
	end
	replace_text(addresses["Text"]["Key Descriptions"]["KOB"]["Address"]["Address"], addresses["Text"]["Key Descriptions"]["KOB"]["Address"]["Bytes"], new_string)
	i=1
	new_string = ""
	while i <= 13 do
		if get_stored_gold_cards("KOG", i)  == 1 then
			new_string = new_string .. tostring(i) .. ","
		end
		i = i + 1
	end
	if new_string ~= "" then
		new_string = new_string:sub(1,-2)
	end
	replace_text(addresses["Text"]["Key Descriptions"]["KOG"]["Address"]["Address"], addresses["Text"]["Key Descriptions"]["KOG"]["Address"]["Bytes"], new_string)
	i=1
	new_string = ""
	while i <= 13 do
		if get_stored_gold_cards("KOT", i)  == 1 then
			new_string = new_string .. tostring(i) .. ","
		end
		i = i + 1
	end
	if new_string ~= "" then
		new_string = new_string:sub(1,-2)
	end
	replace_text(addresses["Text"]["Key Descriptions"]["KOT"]["Address"]["Address"], addresses["Text"]["Key Descriptions"]["KOT"]["Address"]["Bytes"], new_string)
end

function main()
	load_dictionaries()
	set_floors()
	handle_highest_warp()
	local last_floor = get_floor_number()
	local last_kob = get_current_gold_card_qty("KOB")
	local last_kog = get_current_gold_card_qty("KOG")
	local last_kot = get_current_gold_card_qty("KOT")
	local last_sleights = get_sleights()
	local last_battle_cards = get_battle_cards()
	local last_playtime = get_playtime()
	while true do
		local frame = emu.framecount()
		if frame % 20 == 0 then
			local current_playtime = get_playtime()
			if current_playtime == 0 then
				set_starting_deck()
			end
			if not save_or_savestate_loaded(last_playtime, current_playtime) then
				local current_floor = get_floor_number()
				if current_floor ~= last_floor then
					handle_highest_warp()
					set_floors()
					set_current_gold_card_qty("KOB", get_stored_gold_cards("KOB", current_floor))
					set_current_gold_card_qty("KOG", get_stored_gold_cards("KOG", current_floor))
					set_current_gold_card_qty("KOT", get_stored_gold_cards("KOT", current_floor))
					last_kob = get_current_gold_card_qty("KOB")
					last_kog = get_current_gold_card_qty("KOG")
					last_kot = get_current_gold_card_qty("KOT")
				end
				local current_kob = get_current_gold_card_qty("KOB")
				local current_kog = get_current_gold_card_qty("KOG")
				local current_kot = get_current_gold_card_qty("KOT")
				local new_kob = find_new_keys(last_kob, current_kob, "KOB", current_floor)
				local new_kog = find_new_keys(last_kog, current_kog, "KOG", current_floor)
				local new_kot = find_new_keys(last_kot, current_kot, "KOT", current_floor)
				local new_keys = combine_new_keys(new_kob, new_kog, new_kot)
				local current_sleights = {}
				if sleights_temporarily_removed() then
					current_sleights = copy_table(last_sleights)
				else
					current_sleights = get_sleights()
				end
				local new_sleights = find_new_sleights(last_sleights, current_sleights)
				local current_battle_cards = get_battle_cards()
				local results = find_new_battle_cards(last_battle_cards, current_battle_cards)
				local new_battle_cards = results["Regular"]
				local new_premium_battle_cards = results["Premium"]
				last_deck_pointers = get_deck_pointers()
				handle_new_items(new_battle_cards, new_premium_battle_cards, new_keys, new_sleights)
				reassign_deck_pointers(last_deck_pointers)
				set_current_gold_card_qty("KOB", get_stored_gold_cards("KOB", current_floor))
				set_current_gold_card_qty("KOG", get_stored_gold_cards("KOG", current_floor))
				set_current_gold_card_qty("KOT", get_stored_gold_cards("KOT", current_floor))
			else
				handle_highest_warp()
				set_floors()
			end
			last_floor = get_floor_number()
			last_kob = get_current_gold_card_qty("KOB")
			last_kog = get_current_gold_card_qty("KOG")
			last_kot = get_current_gold_card_qty("KOT")
			if not sleights_temporarily_removed() then
				last_sleights = get_sleights()
			end
			last_battle_cards = get_battle_cards()
			last_playtime = current_playtime
			set_key_description_text()
		end
		emu.frameadvance()
	end
end

function test()
	load_dictionaries()
	local last_battle_cards = get_battle_cards()
	local last_playtime = get_playtime()
	while true do
		local frame = emu.framecount()
		if frame % 20 == 0 then
			local current_playtime = get_playtime()
			if current_playtime == 0 then
				set_starting_deck()
			end
			local current_battle_cards = get_battle_cards()
			local new_battle_cards = find_new_battle_cards(last_battle_cards, current_battle_cards)["Regular"]
			if get_length_table(new_battle_cards) > 1 then
				print("New Battle Cards")
				for k,v in pairs(new_battle_cards) do
					print(v)
				end
			end
			last_battle_cards = get_battle_cards()
		end
		emu.frameadvance()
	end
end

main()
--test()
--load_dictionaries()
--set_starting_deck()