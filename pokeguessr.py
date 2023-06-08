import discord
from game import Game, get_random_number

intents = discord.Intents.default()
intents.message_content = True
token = open('token', 'r').read()

client = discord.Client(intents=intents)

games = {}

@client.event
async def on_message(message:discord.Message):
    if message.author == client.user: return

    if message.content.startswith('!start'):
        player = message.author.id
        pkmn = get_random_number()
        games.update({player:Game(player, pkmn)})
        game: Game = games[player]
        await message.reply(game.next_round())

    if message.content.startswith('!guess'):
        player = message.author.id
        try:
            game: Game = games[player]
            pokemon = message.content.split(' ')[1].lower()
            if game.guess(pokemon):
                await message.reply(f'Congratulations ! You found {pokemon.capitalize()}.')
                game.over = True
            else:
                await message.reply(game.next_round())
        except KeyError:
            await message.reply('No game found ! Start a new one with **!start**')
        except IndexError:
            await message.reply('Usage : *!guess <Pokémon>*')
        
client.run(token)