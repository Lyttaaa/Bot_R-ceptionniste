import discord
import random
import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise ValueError("DISCORD_TOKEN environment variable is not set")
GUILD_ID_STR = os.getenv("GUILD_ID")
GUILD_ID = int(GUILD_ID_STR) if GUILD_ID_STR else None
WELCOME_CHANNEL_ID_STR = os.getenv("WELCOME_CHANNEL_ID")
if not WELCOME_CHANNEL_ID_STR:
    raise ValueError("WELCOME_CHANNEL_ID environment variable is not set")
WELCOME_CHANNEL_ID = int(WELCOME_CHANNEL_ID_STR)

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# Messages de bienvenue aléatoires (channel public)
welcome_messages = [
    """☁ *Un léger brouillard s’élève, et lorsque la brume se dissipe… une nouvelle âme se tient parmi nous.*  
✨ Bienvenue, {user} ! Lumharel t’accueille. Prenez un instant pour lui souhaiter la bienvenue !""",
    """🔥 *Une flamme vacille dans l’air avant de s’élever doucement… Une présence nouvelle s’ancre dans le monde.*  
🌟 {user} vient d’être invoqué·e en Lumharel ! Faites-lui un accueil chaleureux !""",
    """🌪 *Le vent porte un murmure à travers les terres… Une voix nouvelle résonne dans Lumharel.*  
🌍 {user} a rejoint notre monde ! Laissez-lui un message pour guider ses premiers pas !""",
    """✨ *Un éclat de lumière traverse le ciel… Un fragment du destin vient de s’incarner.*  
🔔 {user}, bienvenue parmi nous ! Prenez un instant pour le saluer et l’orienter !""",
    """🦉 *Un cri lointain retentit dans la nuit, annonçant un nouvel arrivant sous la protection des astres.*  
📜 {user} rejoint Lumharel ! Que sa quête commence… Souhaitez-lui un bon départ !"""
]

# Texte du guide immersif (ephemeral)
guide_message = """🌟 **Bienvenue en Lumharel, voyageur !**

Ton périple commence ici. Pour trouver ta place parmi nous, suis ces étapes :  

---

📜 **1. Découvre nos terres**  
→ Consulte le salon <#1352146782095802378> pour en apprendre plus sur l’univers de Lumharel.  
→ Les rumeurs et histoires du monde se trouvent dans <#1352130949403512872>.  

---

🎭 **2. Choisis ton histoire**  
→ Rendez-toi dans Salons et Roles pour choisir tes rôles et débloquer les accès à tout le serveur.
→ Va écrire ton nom dans le registre de guilde <#1497568260722266112>

---

🙏 **3. Approche des Autels**  
→ Chaque jour, tu peux prier ou faire une offrande aux divinités en te rendant à leur autels: <#1353209819879837716>.  
→ Elles t’accorderont des bénédictions et des **Lumes** (notre monnaie magique ✨).  

---

🎯 **4. Accomplis des quêtes**  
→ Consulte <#1352143818929078322> pour découvrir les quêtes journalières et hebdomadaires.  
→ Récompenses : **Lumes, bénédictions, et honneur** !  

---

💡 **5. Besoin d’aide ?**  
→ Le salon <#1345479227310346335> est là pour toutes tes questions.  

---

⚠️ **6. Nota Bene**
→ Lie ton compte Discord et on compte Twitch, pour obtenir plus de récompense! Ça se passe ici: <#1412727717819977768>

---

🍃 *Ton histoire ne fait que commencer.  
Marche avec sagesse, et que les Souffles guident ton pas !*"""

# Classe bouton
class GuideButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="📜 Découvrir mon guide", style=discord.ButtonStyle.primary, custom_id="welcome_guide")
    async def show_guide(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(guide_message, ephemeral=True)

@bot.event
async def on_ready():
    print(f'✅ {bot.user} est bien en ligne !')
    bot.add_view(GuideButton())

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    if channel:
        welcome_text = random.choice(welcome_messages).replace("{user}", member.mention)
        await channel.send(welcome_text, view=GuideButton())  # bouton intégré

bot.run(TOKEN)