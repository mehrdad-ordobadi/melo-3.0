import discord
from discord.ext import commands
import asyncio
from dispatch import run_dispatch
from collections import defaultdict

gh_token = "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"
owner = "mehrdad-ordobadi"
repo = "melo-3.0"
workflow_id = "tf_destroy_dispatch.yml"
ref = "env"

env_timers = defaultdict(lambda: None)

tfwb_apply_id = 1202038606613729320


def is_in_channel(channel_id):
    def predicate(ctx):
        return ctx.channel.id == channel_id
    return commands.check(predicate)


async def automatic_destroy(env_name, message):
    await asyncio.sleep(120)  # Wait for 2 minutes
    if env_timers[env_name]:  # Check if timer is still active
        inputs = {"env_name": env_name, "branch_name": "env"}
        await message.channel.send("The 2-minute wait is up. The destroy dispatch has been triggered.")
        await run_dispatch(gh_token, owner, repo, workflow_id, ref, inputs)
        del env_timers[env_name]  # Remove the environment from the tracking dict


def main(token):
    intents = discord.Intents.default()
    intents.message_content = True
    intents.guilds = True
    intents.members = True

    bot = commands.Bot(command_prefix='!', intents=intents)

    @bot.event
    async def on_ready():
        print(f'Logged in as {bot.user.name}')

    @bot.command(name='destroy')
    @is_in_channel(1202004399942279208)
    async def destroy(ctx, env_name):
        inputs = {"env_name": env_name, "branch_name": "env"}
        await ctx.send(f'Destroying environment {env_name} immediately...')
        timer = env_timers.pop(env_name, None)
        if timer:
            timer.cancel()  # Cancel automatic destruction if manual destroy is invoked
        await run_dispatch(gh_token, owner, repo, workflow_id, ref, inputs)

    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return

        if message.channel.id == 1202004399942279208 and message.author.id == tfwb_apply_id:
            # Extract the environment name from the message
            if "has been completed successfully" in message.content:
                env_name = message.content.split()[3]  # Adjust this based on the message format
                env_timers[env_name] = asyncio.create_task(automatic_destroy(env_name,message))
                await message.channel.send(f"Environment {env_name} will be automatically destroyed after 2 minutes unless manually destroyed.")

        await bot.process_commands(message)

    bot.run(token)


if __name__ == "__main__":
    # token = "your_discord_bot_token"
    token = "MTIwMjAxNzgyODE0NDk1NTQ1Mw.Gu_AD3.amyNtiuhmBhhukrORtieqtM5LzhAXWH0Az-zMA"
    main(token)


# generated_url = "https://discord.com/api/oauth2/authorize?client_id=1202017828144955453&permissions=535260821568&scope=bot"
# permission_int = "535260821568"
    
