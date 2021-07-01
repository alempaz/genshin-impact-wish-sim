import random
from Wish import wishes
from Inventory import inventory as inv
from Inventory import list_comb as lst

# Pity Count
five_star_pity_standard = 0
four_star_pity_standard = 0

# pulls used to check inventory
gacha = []
# pulls used to print in console
gacha_show = []


def show_pulls():
    global gacha_show
    print('`~`' * 3, ' Obtained ', '`~`' * 3)
    for _ in gacha_show:
        print(f'{_}')
    wishes.init()


# --------------------------------------- STANDARD BANNER ---------------------------------------------
def standard_banner(limit):
    """
    Banner contains all standard 5 star characters and weapons, not including promotional ones
    Contains all standard 4 star characters and weapons, not including promotional ones
    Contains all 3 Star Weapons

    5 Star Hard Pity is configured at 90 , having higher probability of getting a 5 star after 74 (soft pity)
    4 Star Hard Pity is configured at 10
    There is a 50-50 chance to get either a 5 Star Character or Weapon
    There is a 50-50 chance to get either a 4 Star Character or Weapon

    Percentages:
    94.3% Chance to get a 3 Star
    5.1% Chance to get a 4 Star
    0.6% Chance to get a 5 Star
    """
    global five_star_pity_standard
    global four_star_pity_standard
    global gacha
    global gacha_show

    # Empty gatcha pulls
    gacha = []
    gacha_show = []

    # Weighted list for pull percentages (0.6% - 5.1% - 94.3%)
    # https://stackoverflow.com/questions/14992521/python-weighted-random
    og_pull_percentage = ['3'] * 943 + ['4'] * 51 + ['5'] * 6
    pull_percentage = og_pull_percentage.copy()

    for _ in range(1, limit + 1):
        # Pity System
        # 90 - Is 5 Star pity (n-1) = 89
        if five_star_pity_standard >= 89:
            # Returning to the original weight percentages
            pull_percentage = og_pull_percentage.copy()
            banner_pity(5)
        # 10 - is 4 star pity (n-1) = 9
        elif four_star_pity_standard >= 9:
            banner_pity(4)
        else:
            # Pulls
            if five_star_pity_standard > 74:
                # Adding more prob to get a 5 star
                pull_percentage.extend(['5'] * 250)
            magic = random.choice(pull_percentage)
            # 3 Star
            if magic == '3':
                a = random.choice(lst.star3_weapons)
                add_gacha(3, a)
                inv.add_3star_weapon_inv(a)
                add_pity(four=True, five=True)
            # 4 Star
            elif magic == '4':
                # 50-50 chance of getting either a character or a weapon
                if random.randint(1, 2) == 1:
                    # Character won
                    a = random.choice(lst.star4_standard_characters)
                    # Adding to Inventory
                    inv.add_4star_char_inv(a)
                else:
                    # Weapon won
                    a = random.choice(lst.star4_standar_weapons)
                    # Adding to Inventory
                    inv.add_4star_weapon_inv(a)
                add_gacha(4, a)
                add_pity(four=True, five=True)
                four_star_pity_standard = 0
            # 5 Star
            else:
                # 50-50 chance of getting either a character or a weapon
                if random.randint(1, 2) == 1:
                    # Character won
                    a = random.choice(lst.star5_standard_characters)
                    # Adding to Inventory
                    inv.add_5star_char_inv(a)
                else:
                    # Weapon won
                    a = random.choice(lst.star5_standar_weapons)
                    # Adding to Inventory
                    inv.add_5star_weapon_inv(a)
                add_gacha(5, a)
                add_pity(four=True, five=True)
                # Returning to the original weight percentages
                pull_percentage = og_pull_percentage.copy()
                five_star_pity_standard = 0
                four_star_pity_standard = 0

    # Init Star Animation
    # Checking if there is a 5*,4* or 3* in the pulls. If there are, the animation changes.
    check4 = any(item in gacha for item in lst.all_4star)
    check5 = any(item in gacha for item in lst.all_5star)
    if check5:
        # 5 Star animation
        wishes.animation(5,f'{wishes.banner_}')
    elif check4:
        # 4 Star animation
        wishes.animation(4,f'{wishes.banner_}')
    else:
        # 3 Star animation
        wishes.animation(3,f'{wishes.banner_}')


def banner_pity(rarity):
    global five_star_pity_standard
    global four_star_pity_standard

    if rarity == 5:
        # 50-50 chance of getting either a character or a weapon
        if random.randint(1, 2) == 1:
            # Character won
            a = random.choice(lst.star5_standard_characters)
            # Adding to Inventory
            inv.add_5star_char_inv(a)
        else:
            # Weapon won
            a = random.choice(lst.star5_standar_weapons)
            # Adding to Inventory
            inv.add_5star_weapon_inv(a)
        add_gacha(5, a)
        add_pity(four=True, five=True)
        five_star_pity_standard = 0
        four_star_pity_standard = 0

    elif rarity == 4:
        # 50-50 chance of getting either a character or a weapon
        if random.randint(1, 2) == 1:
            # Character won
            a = random.choice(lst.star4_standard_characters)
            # Adding to Inventory
            inv.add_4star_char_inv(a)
        else:
            # Weapon won
            a = random.choice(lst.star4_standar_weapons)
            # Adding to Inventory
            inv.add_4star_weapon_inv(a)
        add_gacha(4, a)
        add_pity(four=True, five=True)
        four_star_pity_standard = 0


# Function to keep track of pity
def add_pity(four=False, five=False):
    global five_star_pity_standard
    global four_star_pity_standard
    if five and four:
        five_star_pity_standard += 1
        four_star_pity_standard += 1
    elif not five:
        four_star_pity_standard += 1
    elif not four:
        five_star_pity_standard += 1
    else:
        raise Exception('Error while adding pity to perma pity. There needs to be a True statement')


# Add to the list for
def add_gacha(rarity, item):
    global gacha
    global gacha_show

    if rarity == 3:
        gacha.append(item)
        gacha_show.append(item)
    elif rarity == 4:
        gacha.append(item)
        gacha_show.append(wishes.Color.PURPLE + f'{item}   ⭐⭐⭐⭐' + wishes.Color.END)
    elif rarity == 5:
        gacha.append(item)
        gacha_show.append(wishes.Color.YELLOW + f'{item}   🌟🌟🌟🌟🌟' + wishes.Color.END)
    else:
        raise Exception('Invalid rarity type. Rarity can be 3,4 or 5.')

# -----------------------------------------------------------------------------------------------------
