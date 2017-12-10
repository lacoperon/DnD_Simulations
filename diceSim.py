import random as rand

# This function emulates different spells cast at different levels,
# potentially utilizing empowered spell
# Input: n_dice : int (number of dice rolled)

def spell_sim_expectedValue(n_dice, dice_num, empSpell = False, charisma=3,
              armorClass=12, advantage=False, disadvantage=False, proficiency=2, simNumber=100000):
    damageCounter = 0
    for i in range(simNumber):
        damageCounter += single_spell_sim(n_dice, dice_num, empSpell, charisma,
                                          armorClass, advantage, disadvantage, proficiency)
    expectedDamage = damageCounter / simNumber
    print("Expected damage is", expectedDamage, "for n=" + str(simNumber), "runs" )
    return damageCounter / simNumber


def single_spell_sim(n_dice, dice_num, empSpell = False, charisma=3,
              armorClass=12, advantage=False, disadvantage=False, proficiency=2):


    spellAtkBonus = proficiency + charisma
    d20_roll = rand.randint(1,20)

    if advantage or disadvantage:
        d20_alt_roll = rand.randint(1,20)
        if advantage:
            d20_roll = max(d20_roll, d20_alt_roll)
        if disadvantage:
            d20_roll = min(d20_roll, d20_alt_roll)

    if d20_roll == 1:
        return 0

    crit = False
    if d20_roll == 20:
        crit = True

    spell_hit_num = d20_roll + spellAtkBonus

    if spell_hit_num < armorClass:
        return 0

    damageRolls = []

    for i in range(n_dice):
        diceRoll = rand.randint(1, dice_num)
        damageRolls += [diceRoll]

    damageRolls = sorted(damageRolls)

    # print(damageRolls)

    # Empowered Spell code run
    if empSpell:
        dice_index = 0
        while dice_index < len(damageRolls) and damageRolls[dice_index] < ((dice_num + 1.) / 2) and charisma > 0:
            damageRolls[dice_index] = rand.randint(1, dice_num)
            charisma  -= 1
            dice_index += 1

    # print(damageRolls)

    damage = sum(damageRolls)
    damage = damage * (int(crit) + 1)

    # print(damage)
    return damage



# Actual simulation scripting
if __name__ == "__main__":

    charisma_level = 4
    levels = [1,2,3]
    ac = 10
    print("Chromatic Orb Expectation: (w charisma)", charisma_level, "and armor class", ac)
    for i in levels:
        print("For level", i)
        print("With empSpell, with advantage")
        spell_sim_expectedValue(i + 3, 8, empSpell = True, charisma=charisma_level,
                      armorClass=ac, advantage=True, disadvantage=False, proficiency=2, simNumber=100000)
        print("With empSpell, no advantage")
        spell_sim_expectedValue(i + 3, 8, empSpell = True, charisma=charisma_level,
                      armorClass=ac, advantage=False, disadvantage=False, proficiency=2, simNumber=100000)
        print("Without empSpell, with advantage")
        spell_sim_expectedValue(i + 3, 8, empSpell = False, charisma=charisma_level,
                      armorClass=ac, advantage=True, disadvantage=False, proficiency=2, simNumber=100000)
        print("Without empSpell, no advantage")
        spell_sim_expectedValue(i + 3, 8, empSpell = False, charisma=charisma_level,
                      armorClass=ac, advantage=False, disadvantage=False, proficiency=2, simNumber=100000)
