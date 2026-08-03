import re
import secrets

import pprint



def process_command(author: str, command: str) -> list:
    """
    Processes a dice roll command.
    First, valid and invalid commands are separated.
    Second, valid commands are rolled and results are recorded.
    Third, a list of Discord embed dictionaries are prepared for a response.

    Parameters:
        author (str): The name of the user that called the command.
        command (str): A string of characters used in the original command.

    Returns:
        embeds (list[dict]): A list of embed dictionaries with the following structure:
            title (str): The title of the embed.
            fields (list[dict]): A list of dictionaries representing fields in the embed containing:
                name (str): The title of the field.
                value (str): The text of the field.

        ---- Might add more but it'd be default like color and things.
    """
    print(f"Command: {command} \n")

    valid, invalid = parse_command(command)
    roll_results = roll_dice(valid)

    # Send information to DATABASE.
    # 

    embeds = create_embeds(author, roll_results, invalid)

    return embeds




def parse_command(command: str) -> tuple:
    """
    Parses a !roll command and collects the valid and invalid commands into lists.

    Parameters:
        command (str): String of characters used in the original command.

    Returns:
        valid, invalid (tuple): A tuple of lists.
            valid (list[dict]): A list of dictionaries representing roll commands.
                "num": The number of dice to roll.
                "sides": The number of sides on the die.
                "mod": The modifier to use for the roll.
                "adv": Whether the roll had advantage, disadvantage, or neither.
            invalid (list[str]): A list of invalid commands. 
    """
    pattern = re.compile(r"\b(?P<num>\d{0,3})d(?P<sides>\d{1,3})"
                         r"(?:\s*(?P<mod>[-+]\d{1,3}))?"
                         r"(?:\s*(?P<adv>adv|dis))?(?=\s|$)",
                         re.IGNORECASE)

    valid = []
    invalid = []
    last_end = 0

    for match in re.finditer(pattern, command):
        # Everything from the last match to the current match start is a non-match.
        if match.start() > last_end:
            invalid.append(command[last_end:match.start()])

        valid.append(match.groupdict())
        last_end = match.end()

    # Everything from last match to the end of the string is a non-match.
    if last_end < len(command):
        invalid.append(command[last_end:])

    return valid, invalid

def get_roll_information(roll: dict) -> tuple:
    """
    Unpacks a roll dictionary and fixes potential errors.

    Parameters:
        valid (dict): A list of dictionaries representing roll commands.
            num (int): The number of dice to roll.
            sides (int): The number of sides on the die.
            mod (int): The modifier to use for the roll.
            adv (str): Whether the roll had advantage, disadvantage, or neither.
    
    Returns:
        tuple: A tuple containing the roll information.
            num (int): The number of dice to roll.
            sides (int): The number of sides on the die.
            mod (int): The modifier to use for the roll.
            adv (str): Whether the roll has advantage, disadvantage, or neither.
    """
    num = int(roll["num"]) if roll["num"] else 1
    num = num if num > 0 else 1

    sides = int(roll["sides"]) if roll["sides"] else 20
    sides = sides if sides > 0 else 20

    mod = int(roll["mod"]) if roll["mod"] else 0
    adv = roll["adv"] if roll["adv"] else None

    return num, sides, mod, adv

def roll_dice(valid: list) -> dict:
    """
    Takes a list of dictionaries representing roll commands, 'rolls' them, then aggregates them in a dictionary.

    Parameters:
        valid (dict): A list of dictionaries representing roll commands.
            "num": Number of dice to roll.
            "sides": Number of sides on the die.
            "mod": Modifier to use for the roll.
            "adv": Whether the roll has advantage, disadvantage, or neither.

    Returns:
        roll_results (dict): A dictionary whose keys are unique dice notations and has the following values:
            rolls (list[int]): A list of individual roll results.
            total (int): The total of the rolls and modifier.
            sides (int): The number of sides on the die.
            num (int): The number of dice rolled.
            modifier (int): The modifier used for the rolls.
            adv (str): If the roll had advantage, disadvantage, or neither.
    """
    roll_results = dict()

    for roll in valid: # {"num": ?, "sides": ?, "mod": ?, "adv": ?}
        num, sides, mod, adv = get_roll_information(roll)

        # Create dice notation for key.
        notation = (
            f"d{sides}"
            f"{'+' if mod > 0 else ''}{mod if mod != 0 else ''}"
            f"{adv if adv else ''}"
        )

        if adv: # Roll dice with advantage/disadvantage.
            pool_1 = [(secrets.randbelow(sides) + 1) for _ in range(num)]
            pool_2 = [(secrets.randbelow(sides) + 1) for _ in range(num)]

            rolls = [max(a, b) if adv == "adv" or "++" else min(a, b) for a, b in zip(pool_1, pool_2)]

            rolls = [max(1, i) for i in rolls] # Make sure roll is at least 1.
            total = max(0, sum(rolls) + mod * num) # Make sure total is at least 0.

        else: # Roll dice.
            rolls = [(secrets.randbelow(sides) + 1) for _ in range(num)]
            rolls = [max(0, i) for i in rolls] # Make sure roll is at least 1.
            total = max(0, sum(rolls) + mod * num) # Make sure total is at least 0.

        if notation in roll_results: # Aggregate same dice notations together.
            roll_results[notation]["rolls"] += rolls
            roll_results[notation]["total"] += total
            roll_results[notation]["num"] += num
            
        else:
            roll_results[notation] = {
                "rolls": rolls,
                "total": total,
                "sides": sides,
                "num": num,
                "mod": mod,
                "adv": adv
            }

    return roll_results



def create_embeds(author: str, roll_results: dict, invalid: list, max_size = 6000):
    """
    Creates a list of dictionaries representing Disocrd embeds.
    Enforces the 6000 character limit on embeds, starting a new embed when the limit is reached.
    Separate embed is created for invalid commands.

    Parameters:
        author (str): The name of the user that called the command.
        roll_results (dict): A dictionary whose keys are unique dice notations and has the following values:
            rolls (list[int]): A list of individual roll results.
            total (int): The total of the rolls and modifier.
            sides (int): The number of sides on the die.
            num (int): The number of dice rolled.
            modifier (int): The modifier used for the rolls.
            adv (str): If the roll had advantage, disadvantage, or neither.
        invalid (list[str]): A list of invalid commands.
        max_size (int): The character limit of a Discord embed. Default 6000.
    """
    fields = list()

    if invalid:
        fields += (prepare_invalid_fields(invalid))

    if roll_results:
        fields += (prepare_roll_fields(roll_results))

    embeds = list()
    title = f"{author} rolled..."

    current_fields = list()
    current_length = 0

    for field in fields:
        field_length = len(field.get("value", 0))

        # More than 25 fields or more than 6000 characters total? New embed.
        if (len(current_fields) > 25) or (current_length + field_length + len(title) > 6000):
            embeds.append({
                "title": title,
                "fields": current_fields
            })
            current_fields = field
            current_length = len(field["value"])

        else:
            current_fields.append(field)
            current_length += len(field["value"])

    if current_fields:
        embeds.append({
            "title": title,
            "fields": current_fields
        })

    return embeds



def prepare_invalid_fields(invalid: list, max_size = 1024, separator = ", ") -> list:
    """
    Creates a list of dictionaries representing Discord fields.
    Enforces the 1024 character limit on Discord field's text, starting a new field when the limit is reached.

    Parameters:
        invalid (list[str]): A list of invalid commands.
        max_size (int): The character limit of Discord field's text area. Default 1024.
        separator (str): The separator used to join rolls in the field's text. Default ", ".    
    """
    fields = list()
    current_field = list()
    current_length = 0

    for item in invalid:
        item_str = f"{item}"

        # Add separator length if field has items.
        sep_len = len(separator) if current_field else 0

        if current_length + sep_len + len(item_str) > max_size:
            current_field = separator.join(current_field)
            fields.append({
                "name": "Invalid",
                "value": current_field
            })
            current_field = [item_str]
            current_length = len(item_str)

        else:
            current_field.append(item_str)
            current_length += len(item_str)

    if current_field:
        current_field = separator.join(current_field)
        fields.append({
            "name": "Invalid",
            "value": current_field
        })

    return fields



def prepare_roll_fields(roll_results: dict, max_size = 1024, separator = ", ") -> list:
    """
    Creates a list of dictionaries representing Discord fields.
    Enforces the 1024 character limit on Discord field's text, starting a new field when the limit is reached.
    
    Parameters:
        roll_results (dict): A dictionary whose keys are unique dice notations and has the following values:
            rolls (list[int]): A list of individual roll results.
            total (int): The total of the rolls and modifier.
            sides (int): The number of sides on the die.
            num (int): The number of dice rolled.
            mod (int): The modifier used for the rolls.
            adv (str): Whether the roll had advantage, disadvantage, or neither.
        max_size (int): The character limit of Discord field's text area. Default 1024.
        separator (str): The separator used to join rolls in the field's text. Default ", ".  
    
    Returns:
        fields (list[dict]): A list of dictionaries representing Discord embed fields, containing:
            name (str): The title of the field.
            value (str): The text of the field.
    """
    fields = list()

    for value in roll_results.values():
        rolls = value["rolls"]
        total = value["total"]
        sides = value["sides"]
        num = value["num"]
        mod = value["mod"] # Then make a string version.
        mod_str = f"{'+' if mod > 0 else ''}{mod if mod != 0 else ''}"
        adv = value["adv"]

        current_field = list()
        current_length = 0
        last_index = 0

        for index, roll in enumerate(rolls):
            roll_str = f"**{roll}**{mod_str}" if roll == sides else f"{roll}{mod_str}"

            # Add separator length if field has items.
            sep_len = len(separator) if current_field else 0

            if current_length + sep_len + len(roll_str) > max_size:
                current_field = separator.join(current_field)
                fields.append({
                    "name": current_title, # f"{len(rolls[last_index:index+1])}d{sides}{mod_str} | last_index{sum(rolls[last_index:index+1]) + mod * num}"
                    "value": current_field
                })
                current_field = [roll_str]
                current_length = len(roll_str)
                last_index = index

            else:
                current_title = f"{len(rolls[last_index:index+1])}d{sides}{mod_str} | {sum(rolls[last_index:index+1]) + mod * num}"
                current_field.append(roll_str)
                current_length += len(roll_str)

        if current_field:
            current_field = separator.join(current_field)
            fields.append({
                "name": current_title,
                "value": current_field
            })

    return fields



# Testing.
if __name__ == "__main__":
    author = 'tebbz'
    tests = [
        "d20+1 dd 4d8 --./rm rf 2d20 d0 10000d20000 D4 d20adv d6dis disadv d6++ 2d6dis",
        "2d20"
    ]

    for test in tests:
        no_issue = process_command(author, test)



