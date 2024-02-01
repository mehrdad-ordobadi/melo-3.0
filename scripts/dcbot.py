import discord
from discord.ext import commands
import asyncio
from dispatch import run_dispatch

gh_token = "***********x"
owner = "mehrdad-ordobadi"
repo = "melo-3.0"
# workflow_id = "tf_apply_dispatch.yml"
workflow_id = "tf_destroy_dispatch.yml"
ref = "env"
inputs = {"env_name": "env1", "branch_name": "env"}

skip_auto_destroy = False

tfwb_apply_id = 1202038606613729320

def is_in_channel(channel_id):
    def predicate(ctx):
        return ctx.channel.id == channel_id
    return commands.check(predicate)




def main(token):
    intents = discord.Intents.default()
    intents.message_content = True  # Needed to read message content if you're processing commands
    intents.guilds = True            # Needed for operations within guilds
    intents.members = True          # Needed to interact with guild members (privileged intent)

    bot = commands.Bot(command_prefix='!', intents=intents)

    @bot.event
    async def on_ready():
        print(f'Logged in as {bot.user.name}')

    @bot.command(name='hello')
    @is_in_channel(1202004399942279208)
    async def hello(ctx):
        await ctx.send('Hello to you too!')

    @bot.command(name='destroy')
    @is_in_channel(1202004399942279208)
    async def destroy(ctx, *, arg):
        global skip_auto_destroy
        if arg == 'now':
            await ctx.send('Destroying the environment immediately...')
            skip_auto_destroy = True
            await run_dispatch(gh_token, owner, repo, workflow_id, ref, inputs)
        # elif arg == 'later':
        #     await ctx.send('The environment will be destroyed in 2 minutes...')
        #     await asyncio.sleep(120)
        #     run_dispatch()
        else:
            await ctx.send('Invalid argument. Use "now".')

    @bot.event  
    async def on_message(message):
        # Ignore messages sent by the bot itself
        if message.author == bot.user:
            return
        
        # Check if the message is from the specified channel and webhook
        if message.channel.id == 1202004399942279208 and message.author.id == tfwb_apply_id:
            # The message was sent by the webhook, perform an action after a delay
            global skip_auto_destroy
            skip_auto_destroy = False
            await asyncio.sleep(60)  # Wait for 2 minutes
            if not skip_auto_destroy:
                await message.channel.send("The 1-minute wait is up. The destroy dispatch has been triggered.")
                await run_dispatch(gh_token, owner, repo, workflow_id, ref, inputs)  # Make sure this is an async function

        # Process commands in the message
        await bot.process_commands(message)

    bot.run(token)


if __name__ == "__main__":
    # generated_url = "https://discord.com/api/oauth2/authorize?client_id=1202017828144955453&permissions=535260821568&scope=bot"
    # permission_int = "535260821568"
    token = "************"
    main(token)