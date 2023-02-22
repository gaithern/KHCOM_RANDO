# KHCOM_RANDO

This randomizer is only compatible with the Bizhawk emulator.
You can use this by running randomize.py, which will generate your random.json file.
In Bizhawk, run KHCOM, open Lua Console, and run khcom_rando_script.lua. This script will read from your random.json file in order to parse items you acquire and switch them with something else.

Randomizer logic works via "goal" floors.  The goal floors as of now are:

1,6,10,11,12,13.

This means that you must complete floor 1 as normal, then the Key of Beginnings, Key of Guidance, and Key to Truth (as well as other enemy cards) for floors 2-6 can be scattered anywhere on the assigned worlds from floors 2-6.
The goal is to find the Key of Beginnings, Key of Guidance, and Key of Truth for floor 6 and move onto the same situation for floors 7-10.
After that, complete 11,12,13 as normal.

Some additional details:

-Floor 1 is always Traverse Town

-Floor 11 is always 100 Acre Wood

-Floor 13 is always Castle Oblivion

-Text/Card Image injection is a WIP.  For now, you will pick up what appears to be a Kingdom Key 9 for example, but when you check your inventory you will see what that card is mapped to (Cure 3 as an example)

-You can check which keys you have for which floors by viewing the card descriptions for Key of Beginnings, Key of Guidance, and Key of Truth in your Map Cards inventory.

-You can edit the frequency that battle cards are chosen for remapping (or turn them off entirely) by editing the weights in battle_cards.json
  (For example you can do a no Cure card challenge or a no 0 value card challenge by setting each card types weight to 0)
