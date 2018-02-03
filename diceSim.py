import random as rand

'''
This function emulates different spells cast at different levels in D&D 5e,
and models their damage based on the number, and type, of damage dice rolled.
The expected damage value based on the simulations, for the particular input
variables, is printed out.

The code here is far from complete, but serves well to model the particular
character in my campaign (for now).

Input: n_dice : int (number of dice rolled),
       dice_num : int (type of dice rolled, i.e. d6, d8, etc.),
       empSpell : bool (whether or not the spell cast uses 'Empowered Spell',
       (IE you can reroll 'charisma' number of dice if you desire to) ),
       charisma : int (charisma roll modifier of your character),
       armorClass : int (armorClass of your opponent),
       advantage : bool (marks advantage on your spell hit roll),
       disadvantage : bool (marks disadvantage on your spell hit roll),
       proficiency : int (denotes your character's proficiency modifier),
       simNumber : int (number of times to run the simulation to get E(X) )

Output: Currently void
'''

# TODO: Figure out what the return value should be (distribution, perhaps, of all damage scores)
# Also TODO: Parallelize runs, so that the code can return much faster,
#            perhaps using the Pool object within `multithreading`, with map

def spell_sim_expectedValue(n_dice, dice_num, empSpell = False, charisma=3,
              armorClass=12, advantage=False, disadvantage=False, proficiency=2, simNumber=100000):

    assert not (advantage and disadvantage)
    assert armorClass >= 0 and armorClass <= 20
    assert simNumber > 0

    damageCounter = 0
    zeroCounter = 0
    for i in range(simNumber):
        dam = single_spell_sim(n_dice, dice_num, empSpell, charisma,
                                          armorClass, advantage, disadvantage, proficiency)
        damageCounter += dam
        if dam == 0:
            zeroCounter += 1

    expectedDamage = damageCounter / simNumber
    print("Expected damage is", expectedDamage, "for n=" + str(simNumber), "runs" )
    print("Does no damage in", 100. * float(zeroCounter)/simNumber, "% of cases")
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

    # Empowered Spell code run
    if empSpell:
        dice_index = 0
        while dice_index < len(damageRolls) and damageRolls[dice_index] < ((dice_num + 1.) / 2) and charisma > 0:
            damageRolls[dice_index] = rand.randint(1, dice_num)
            charisma  -= 1
            dice_index += 1

    damage = sum(damageRolls)
    damage = damage * (int(crit) + 1)

    return damage



# Actual simulation scripting
if __name__ == "__main__":

    charisma_level = 6
    levels = [1,2,3]
    ac = 10
    prof_bonus = 3
    sim_num = 100000
    print("Fireball Expectation: (w charisma)", charisma_level, "and armor class", ac)
    for i in [1]:
        print("With empSpell, with advantage")
        spell_sim_expectedValue(8, 6, empSpell = True, charisma=charisma_level,
                      armorClass=ac, advantage=True, disadvantage=False, proficiency=prof_bonus, simNumber=sim_num)
        print("With empSpell, without advantage")
        spell_sim_expectedValue(8, 6, empSpell = True, charisma=charisma_level,
                      armorClass=ac, advantage=False, disadvantage=False, proficiency=prof_bonus, simNumber=sim_num)
        print("Without empSpell, with advantage")
        spell_sim_expectedValue(8, 6, empSpell = False, charisma=charisma_level,
                      armorClass=ac, advantage=True, disadvantage=False, proficiency=prof_bonus, simNumber=sim_num)
        print("Without empSpell, without advantage")
        spell_sim_expectedValue(8, 6, empSpell = False, charisma=charisma_level,
                      armorClass=ac, advantage=False, disadvantage=False, proficiency=prof_bonus, simNumber=sim_num)

    print("\n----\n\nChromatic Orb Expectation: (w charisma)", charisma_level, "and armor class", ac)
    for i in levels:
        print("For level {}".format(i))
        print("With empSpell, with advantage")
        spell_sim_expectedValue(2+i, 8, empSpell = True, charisma=charisma_level,
                      armorClass=ac, advantage=True, disadvantage=False, proficiency=prof_bonus, simNumber=sim_num)
        print("With empSpell, without advantage")
        spell_sim_expectedValue(2+i, 8, empSpell = True, charisma=charisma_level,
                      armorClass=ac, advantage=False, disadvantage=False, proficiency=prof_bonus, simNumber=sim_num)
        print("Without empSpell, with advantage")
        spell_sim_expectedValue(2+i, 8, empSpell = False, charisma=charisma_level,
                      armorClass=ac, advantage=True, disadvantage=False, proficiency=prof_bonus, simNumber=sim_num)
        print("Without empSpell, without advantage")
        spell_sim_expectedValue(2+i, 8, empSpell = False, charisma=charisma_level,
                      armorClass=ac, advantage=False, disadvantage=False, proficiency=prof_bonus, simNumber=sim_num)
