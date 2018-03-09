from discord.ext import commands
import discord
from thehammer.decorators import is_server_admin

class ModModule:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @is_server_admin()
    async def kick(self, ctx, user:discord.Member, *, reason:str):
        is_special = ctx.author == ctx.guild.owner
        if not ctx.guild.get_member(ctx.bot.user.id).guild_permissions.kick_members and not ctx.guild.get_member(ctx.bot.user.id).guild_permissions.administrator:
            return await ctx.send(":robot: **Hey, I can't do that, please ask an administrator to give me KICK_MEMBERS or ADMINISTRATOR permission!**")
        if ctx.author.top_role.position > user.top_role.position or is_special:
            guild = await self.bot.modlog.get_guild(ctx.guild)
            _type = "Kick"
            moderator = ctx.author
            await guild.new_case(_type, user, moderator, reason)
            await user.kick(reason=reason)
            return await ctx.send(":robot: **Kicked user <@{}> for {}**".format(user.id, reason))
        else:
            return await ctx.send(":robot: **Hey, I'm sorry, but that user is higher in the hierarchy than you are, I can't let you do that...**")

def setup(bot):
    bot.add_cog(ModModule(bot))
