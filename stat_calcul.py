import sqlite3

class Pal:
    def __init__(self, base_hp, base_defense, base_att):
        self.base_hp = base_hp
        self.base_defense = base_defense
        self.base_att = base_att

    
    @staticmethod
    def from_name(name, db_path='pals.db'):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT base_hp, base_defense, base_att FROM pals WHERE name = ?", (name,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Pal(*row)
        else:
            raise ValueError("Pal with the given name not found")

    
class IV:
    def __init__(self, iv_hp, iv_defense, iv_att):
        self.iv_hp = iv_hp
        self.iv_defense = iv_defense
        self.iv_att = iv_att

    def convert_to_percentage(self):
        max_iv = 100
        max_percentage = 30.0
        self.iv_hp = (self.iv_hp / max_iv) * max_percentage
        self.iv_defense = (self.iv_defense / max_iv) * max_percentage
        self.iv_att = (self.iv_att / max_iv) * max_percentage
        return IV(self.iv_hp , self.iv_att , self.iv_defense)
        

class EV:
    def __init__(self, ev_hp, ev_defense, ev_att):
        self.ev_hp = ev_hp
        self.ev_defense = ev_defense
        self.ev_att = ev_att


class Bonus:
    def __init__(self, bonus_hp, bonus_defense, bonus_att):
        self.bonus_hp = bonus_hp
        self.bonus_defense = bonus_defense
        self.bonus_att = bonus_att

class Stat():
    def __init__(self, pal:Pal, iv:IV, ev:EV, lvl, stars , bonus:Bonus):
        
        self.pal = pal
        self.iv = iv
        self.ev = ev
        self.lvl = lvl
        self.stars = stars
        self.bonus = bonus

    

    def calculate_hp(self):
        HP_IV = self.iv.convert_to_percentage().iv_hp/100
        HP_Bonus = self.bonus.bonus_hp/100
        HP_SoulBonus = self.ev.ev_hp / 100  # Each EV value gives 3%
        CondenserBonus = self.stars * 0.05  # Each star gives 5%
        
        hp = (500 + 5 * self.lvl + self.pal.base_hp * 0.5 * self.lvl * (1 + HP_IV)) * (1 + HP_Bonus) * (1 + HP_SoulBonus) * (1 + CondenserBonus)
        return round(hp)

    def calculate_att(self):
        Att_IV = self.iv.convert_to_percentage().iv_att/100
        Attack_Bonus = self.bonus.bonus_att/100
        Attack_SoulBonus = self.ev.ev_att / 100  # Each EV value gives 3%
        CondenserBonus = self.stars * 0.05  # Each star gives 5%
        
        att = (100 + self.pal.base_att * 0.075 * self.lvl * (1 + Att_IV)) * (1 + Attack_Bonus) * (1 + Attack_SoulBonus) * (1 + CondenserBonus)
        return round(att)

    def calculate_defense(self):
        Defense_IV = self.iv.convert_to_percentage().iv_defense/100
        Defense_Bonus = self.bonus.bonus_defense/100
        Defense_SoulBonus = self.ev.ev_defense / 100  # Each EV value gives 3%
        CondenserBonus = self.stars * 0.05  # Each star gives 5%
        
        defense = (100 + self.pal.base_defense * 0.075 * self.lvl * (1 + Defense_IV)) * (1 + Defense_Bonus) * (1 + Defense_SoulBonus) * (1 + CondenserBonus)
        return round(defense)

def calculate_palworld_damage(pal_level,move_power,pal_attack,target_defense,stab=bool):

    damage = 1.1 * ((1.5 * pal_level + 20) * move_power * pal_attack / target_defense) / 15
        
    if stab:
        damage += damage*0.2
        
    min_damage = damage * 0.9
    max_damage = damage * 1.1 

    return {'min_damage': min_damage , 'max_damage': max_damage}

       
        

        


# Example usage
pal_name = "Frostallion"  # Replace with the actual name of the Pal in the database
pal = Pal.from_name(pal_name)


iv = IV(40, 15, 20)
print(iv.convert_to_percentage())
ev = EV(5, 5, 5)
bonus = Bonus(0,0,0)
lvl=10
stars=3


stats = Stat(pal, iv, ev, lvl, stars, bonus)

 
print(f"HP: {stats.calculate_hp()}")
print(f"Defense: {stats.calculate_defense()}")
print(f"Attack: {stats.calculate_att()}")
