 IMPORTS
import os
import time
import random
import sqlite3
import telebot
from telebot import types

# --- CONFIGURATION & TOKEN ---
API_TOKEN = os.getenv(8885739902:AAGfDtqJVPGS43b3AXWCEAj1pazS7RvfNMU)
if not API_TOKEN:
    API_TOKEN = "YOUR_LOCAL_BOT_TOKEN_HERE"  

bot = telebot.TeleBot(8885739902:AAGfDtqJVPGS43b3AXWCEAj1pazS7RvfNMU)
DB_FILE = "jjk_legends.db"

# --- SYSTEM SETTINGS & CONSTANTS ---
VALID_SHOPS = [
    "shop", "bossshop", "raidshop", "weaponshop", "skillshop", 
    "lowlvlshop", "artifactshop", "potionshop", "shikigamishop", 
    "premiumshop", "eventshop"
]

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Players core stats table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS players (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            level INTEGER DEFAULT 1,
            exp INTEGER DEFAULT 0,
            hp INTEGER DEFAULT 100,
            max_hp INTEGER DEFAULT 100,
            cursed_energy INTEGER DEFAULT 50,
            max_ce INTEGER DEFAULT 50,
            coins INTEGER DEFAULT 500,
            gems INTEGER DEFAULT 10,
            dark_shards INTEGER DEFAULT 0,
            soul_tokens INTEGER DEFAULT 0,
            grade TEXT DEFAULT 'Grade 4',
            clan TEXT DEFAULT 'None',
            skills TEXT DEFAULT 'Punch',
            inventory TEXT DEFAULT 'Wooden Sword',
            last_daily INTEGER DEFAULT 0,
            last_weekly INTEGER DEFAULT 0,
            last_monthly INTEGER DEFAULT 0,
            first_claim INTEGER DEFAULT 0
        )
    ''')
    
    # World Boss configuration table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS world_boss (
            id INTEGER PRIMARY KEY DEFAULT 1,
            name TEXT DEFAULT 'Sukuna',
            hp INTEGER DEFAULT 10000,
            max_hp INTEGER DEFAULT 10000,
            end_time INTEGER DEFAULT 0
        )
    ''')
    
    # Initialize global world boss if not present
    cursor.execute("SELECT COUNT(*) FROM world_boss")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO world_boss (id, name, hp, max_hp) VALUES (1, 'Sukuna (20 Fingers)', 10000, 10000)")
        
    conn.commit()
    conn.close()

init_db()

# --- DATABASE LOGIC HELPERS ---
def get_player(user_id, username="Unknown"):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM players WHERE user_id = ?", (user_id,))
    player = cursor.fetchone()
    if not player:
        cursor.execute("INSERT INTO players (user_id, username) VALUES (?, ?)", (user_id, username))
        conn.commit()
        cursor.execute("SELECT * FROM players WHERE user_id = ?", (user_id,))
        player = cursor.fetchone()
    conn.close()
    return player

def update_player(user_id, field, value):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(f"UPDATE players SET {field} = ? WHERE user_id = ?", (value, user_id))
    conn.commit()
    conn.close()

def get_boss():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT name, hp, max_hp FROM world_boss WHERE id = 1")
    boss = cursor.fetchone()
    conn.close()
    return boss

def damage_boss(dmg):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("UPDATE world_boss SET hp = MAX(0, hp - ?) WHERE id = 1", (dmg,))
    conn.commit()
    conn.close()

# --- KEYBOARD BUTTONS MENU ---
def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(types.KeyboardButton("⚔️ Battle"), types.KeyboardButton("👹 Boss Battle"))
    return markup

# --- COMMAND HANDLERS ---

@bot.message_handler(commands=['start'])
def cmd_start(message):
    p = get_player(message.from_user.id, message.from_user.username)
    welcome = (
        f"👋 Welcome *{message.from_user.first_name}* to *Jujutsu Legend RPG*!\n\n"
        "Aap ek Jujutsu Sorcerer ban chuke hain. Cursed spirits ko harayein aur Special Grade tak rank up karein.\n\n"
        "📖 Sabhi commands dekhne ke liye `/help` type karein."
    )
    bot.send_message(message.chat.id, welcome, parse_mode="Markdown", reply_markup=main_menu())

@bot.message_handler(commands=['help'])
def cmd_help(message):
    help_text = (
        "📖 *JUJUTSU LEGEND RPG - MENU* 📖\n\n"
        "🎮 *Core Gameplay:*\n"
        "/start - Menu Open karein\n"
        "/battle - Fight Cursed Spirits\n"
        "/raid - Clan Boss Battle join karein\n"
        "/mission - Timed Sorcerer Quests\n"
        "/train - Base stats Meditate/Train karein\n"
        "/awaken - True potential unlock karein\n\n"
        "👤 *Profile & Items:*\n"
        "/profile - Stats & Currencies\n"
        "/skills - Equipped Techs\n"
        "/inventory - Items & Artifacts\n"
        "/rank - Sorcerer Grade System\n\n"
        "🪙 *Rewards System:*\n"
        "/firstclaim | /daily | /weekly | /monthly\n\n"
        "🏪 *All Shop Types:*\n"
        "/shop, /bossshop, /raidshop, /weaponshop, /skillshop, /lowlvlshop, /artifactshop, /potionshop, /shikigamishop, /premiumshop, /eventshop\n\n"
        "🤝 *Social & PvP System:*\n"
        "/clan - View Clan list\n"
        "/trade - Secure item swap\n"
        "/gift - Box Event unlock\n"
        "/give - Items transfer\n"
        "/summon - Roll Gacha Shikigami\n"
        "/challenge - 1v1 Ranked Duel\n"
        "/league - Seasonal matches\n\n"
        "👹 *World Boss Actions:*\n"
        "/boss - Boss HP & Stats\n"
        "/strike - Attack current World Boss\n"
        "/rewards - Get Boss loot"
    )
    bot.send_message(message.chat.id, help_text, parse_mode="Markdown")

@bot.message_handler(commands=['profile'])
def cmd_profile(message):
    p = get_player(message.from_user.id, message.from_user.username)
    text = (
        f"👤 *SORCERER STATUS PROFILE*\n"
        f"━━━━━━━━━━━━━━━━━━━\n"
        f"🏅 *Name:* {message.from_user.first_name} (@{p[1]})\n"
        f"🎖️ *Grade:* {p[12]} | *Level:* {p[2]} (EXP: {p[3]})\n"
        f"❤️ *HP:* {p[4]}/{p[5]} | 🌀 *CE:* {p[6]}/{p[7]}\n"
        f"🛡️ *Clan:* {p[13]}\n\n"
        f"💰 *CURRENCY STORAGE*\n"
        f"🪙 Coins: {p[8]} | 💎 Gems: {p[9]}\n"
        f"⬛ Dark Shards: {p[10]} | 🎟️ Soul Tokens: {p[11]}"
    )
    bot.send_message(message.chat.id, text, parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.text == "⚔️ Battle" or m.text == "/battle")
@bot.message_handler(commands=['battle'])
def cmd_battle(message):
    p = get_player(message.from_user.id, message.from_user.username)
    if p[6] < 10:
        return bot.reply_to(message, "❌ Game action ke liye kam se kam 10 Cursed Energy (CE) chahiye!")
    
    spirits = ["Fly Head", "Finger Bearer", "Hanami Clone", "Mahito Core"]
    spirit = random.choice(spirits)
    coins_reward = random.randint(40, 120)
    exp_reward = random.randint(15, 30)
    
    update_player(message.from_user.id, "cursed_energy", p[6] - 10)
    update_player(message.from_user.id, "coins", p[8] + coins_reward)
    update_player(message.from_user.id, "exp", p[3] + exp_reward)
    
    bot.send_message(message.chat.id, f"⚔️ *Battle Outcome:* Aapne ek *{spirit}* par attack kiya!\n🪙 Coins Gained: +{coins_reward}\n✨ EXP: +{exp_reward}", parse_mode="Markdown")

@bot.message_handler(commands=['raid'])
def cmd_raid(message):
    bot.reply_to(message, "🏰 *Clan Raid:* Aapne apne clan ke sath mil kar Shinjuku Raid execute kiya! Rewards update system active hai.")

@bot.message_handler(commands=['mission'])
def cmd_mission(message):
    bot.reply_to(message, "📜 *Bounty Quest:* Timed sorcerer quest deploy ho chuki hai. Check your log.")

@bot.message_handler(commands=['skills'])
def cmd_skills(message):
    p = get_player(message.from_user.id, message.from_user.username)
    bot.reply_to(message, f"🌀 *Equipped Cursed Techniques:* {p[14]}")

@bot.message_handler(commands=['inventory'])
def cmd_inventory(message):
    p = get_player(message.from_user.id, message.from_user.username)
    bot.reply_to(message, f"🎒 *Your Cursed Storage:* {p[15]}")

@bot.message_handler(commands=VALID_SHOPS)
def cmd_shops(message):
    shop_name = message.text.replace("/", "").lower()
    bot.reply_to(message, f"🏪 *{shop_name.upper()}* Market open hai! Aap Coins aur Gems se rare items deploy kar sakte hain.")

@bot.message_handler(commands=['clan'])
def cmd_clan(message):
    p = get_player(message.from_user.id, message.from_user.username)
    bot.reply_to(message, f"🛡️ *Clan System:* Aapka current clan allocation: *{p[13]}*")

@bot.message_handler(commands=['firstclaim'])
def cmd_firstclaim(message):
    p = get_player(message.from_user.id, message.from_user.username)
    if p[19] == 1:
        return bot.reply_to(message, "❌ Aap Newbie Starter Kit pehle hi claim kar chuke hain!")
    update_player(message.from_user.id, "coins", p[8] + 2000)
    update_player(message.from_user.id, "first_claim", 1)
    bot.reply_to(message, "🎁 *Starter Kit Claimed:* +2000 Coins assigned!")

@bot.message_handler(commands=['daily'])
def cmd_daily(message):
    p = get_player(message.from_user.id, message.from_user.username)
    now = int(time.time())
    if now - p[16] < 86400:
        return bot.reply_to(message, "❌ Chill! Daily cooldown active hai, kal wapas aayein.")
    update_player(message.from_user.id, "coins", p[8] + 200)
    update_player(message.from_user.id, "last_daily", now)
    bot.reply_to(message, "🎁 *Daily claimed:* +200 Coins added.")

@bot.message_handler(commands=['weekly'])
def cmd_weekly(message):
    p = get_player(message.from_user.id, message.from_user.username)
    now = int(time.time())
    if now - p[17] < 604800:
        return bot.reply_to(message, "❌ Weekly pack processing running hai!")
    update_player(message.from_user.id, "gems", p[9] + 15)
    update_player(message.from_user.id, "last_weekly", now)
    bot.reply_to(message, "🎁 *Weekly asset delivery:* +15 Gems!")

@bot.message_handler(commands=['monthly'])
def cmd_monthly(message):
    p = get_player(message.from_user.id, message.from_user.username)
    now = int(time.time())
    if now - p[18] < 2592000:
        return bot.reply_to(message, "❌ Monthly bonus already active state par hai.")
    update_player(message.from_user.id, "soul_tokens", p[11] + 2)
    update_player(message.from_user.id, "last_monthly", now)
    bot.reply_to(message, "🎁 *Monthly bonus:* +2 Soul Tokens dispatch successful.")

@bot.message_handler(commands=['give', 'gift', 'trade'])
def cmd_social(message):
    bot.reply_to(message, "🔄 *P2P Room System:* Player security context verified. Trading/Gifting active state par hai.")

@bot.message_handler(commands=['summon'])
def cmd_summon(message):
    p = get_player(message.from_user.id, message.from_user.username)
    if p[9] < 5:
        return bot.reply_to(message, "❌ Summon karne ke liye minimum 5 Gems required hain!")
    shikigamis = ["Divine Dog", "Nue", "Great Serpent", "Mahoraga (Ultra Rare)"]
    rolled = random.choice(shikigamis)
    update_player(message.from_user.id, "gems", p[9] - 5)
    bot.reply_to(message, f"🔮 *Summon Result:* Aapne successfully *{rolled}* ko tame kiya!")

@bot.message_handler(commands=['awaken'])
def cmd_awaken(message):
    bot.reply_to(message, "🔥 *Domain Expansion / Awakening:* Level required criteria match nahi hua.")

@bot.message_handler(commands=['train'])
def cmd_train(message):
    p = get_player(message.from_user.id, message.from_user.username)
    update_player(message.from_user.id, "max_hp", p[5] + 5)
    bot.reply_to(message, "🧘 *Meditation Complete:* Permanent +5 Max HP base values update verified.")

@bot.message_handler(commands=['league', 'challenge'])
def cmd_pvp(message):
    bot.reply_to(message, "⚔️ *Jujutsu Goodwill Tournament:* 1v1 Dual configuration system execution active.")

@bot.message_handler(commands=['rank'])
def cmd_rank(message):
    p = get_player(message.from_user.id, message.from_user.username)
    bot.reply_to(message, f"🎖️ *Your Rank Grade Profile:* {p[12]}")

@bot.message_handler(func=lambda m: m.text == "👹 Boss Battle" or m.text == "/boss")
@bot.message_handler(commands=['boss'])
def cmd_boss(message):
    b = get_boss()
    bot.send_message(message.chat.id, f"👹 *WORLD BOSS STATS* 👹\n\n*Name:* {b[0]}\n*HP:* {b[1]}/{b[2]}\n\nAttack call lagane ke liye `/strike` use karein.", parse_mode="Markdown")

@bot.message_handler(commands=['strike'])
def cmd_strike(message):
    p = get_player(message.from_user.id, message.from_user.username)
    b = get_boss()
    if b[1] <= 0:
        return bot.reply_to(message, "💀 Boss pehle se hara hua hai! `/rewards` claim karein.")
    
    dmg = random.randint(100, 350)
    damage_boss(dmg)
    bot.reply_to(message, f"💥 *BOOM!* Aapne World Boss ko *{dmg} damage* diya!")

@bot.message_handler(commands=['rewards'])
def cmd_rewards(message):
    bot.reply_to(message, f"🎁 *Loot drops:* Boss fight dynamic evaluation done. Rewards added to your inventory profile state.")

# --- WEBHOOK AUTO REMOVAL SYSTEM ---
try:
    bot.remove_webhook()
    time.sleep(1)
except Exception as e:
    print(f"Webhook Status: {e}")

print("🚀 Jujutusu_legend Engine initialization complete. Polling live...")
bot.infinity_polling()
