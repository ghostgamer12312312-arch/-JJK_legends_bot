# START OF CODE
import os
import random
import telebot

# This securely grabs your Bot Token from Render's cloud settings
API_TOKEN = os.environ.get('API_TOKEN')
bot = telebot.TeleBot(API_TOKEN)

# Live test data saved temporarily in memory
enemy_hp = 1000
player_inventory = ["Playful Cloud", "Health Elixir x5"]

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(
        message, 
        "Welcome to JJK_LAGENDS!\n\n"
        "⚔️ Send /battle to fight Cursed Spirits\n"
        "🎒 Send /inventory to check your gear"
    )

@bot.message_handler(commands=['battle'])
def handle_battle(message):
    global enemy_hp
    damage = random.randint(150, 320)
    enemy_hp -= damage
    
    if enemy_hp <= 0:
        enemy_hp = 1000  # Resets curse HP for the next target
        bot.reply_to(message, f"💥 You dealt {damage} damage!\n\n🏆 The Cursed Spirit was exorcised! You earned 50 Gold!")
    else:
        bot.reply_to(message, f"⚔️ You unleashed Dragon Shroud!\n💥 Dealt {damage} damage.\n\n👹 Cursed Spirit HP remaining: {enemy_hp}")

@bot.message_handler(commands=['inventory'])
def handle_inventory(message):
    items = "\n• ".join(player_inventory)
    bot.reply_to(message, f"🎒 YOUR INVENTORY:\n• {items}")

bot.infinity_polling()
