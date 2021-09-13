import discord
from utils import messages

from discord.ext import commands

owners = []


def is_owner(ctx):
    """ Checks if the author is one of the owners """
    return ctx.author.id in owners


async def check_permissions(ctx, perms, *, check=all):
    """ Checks if author has permissions to a permission """
    if ctx.author.id in owners:
        return True

    resolved = ctx.channel.permissions_for(ctx.author)
    return check(getattr(resolved, name, None) == value for name, value in perms.items())


def has_permissions(*, check=all, **perms):
    """ discord.Commands method to check if author has permissions """
    async def pred(ctx):
        return await check_permissions(ctx, perms, check=check)
    return commands.check(pred)


async def check_priv(ctx, member):
    """ Custom (weird) way to check permissions when handling moderation commands """
    try:
        # Self checks
        '''
        if member == ctx.author:
            return await ctx.send(f"You can't {ctx.command.name} yourself")
        '''
        if member.id == ctx.bot.user.id:
            return await ctx.send(messages.field_perms_1.replace('[user]', ctx.author.mention).replace('[username]', ctx.author.name))
        '''
        # Check if user bypasses
        if ctx.author.id == ctx.guild.owner.id:
            return False
        '''
        # Now permission check
        if member.id in owners:
            if ctx.author.id not in owners:
                return await ctx.send(messages.field_perms_2.replace('[user]', ctx.author.mention).replace('[username]', ctx.author.name).replace('[command_name]', ctx.command.name))
            else:
                pass
        if member.id == ctx.guild.owner.id:
            return await ctx.send(messages.field_perms_3.replace('[user]', ctx.author.mention).replace('[username]', ctx.author.name).replace('[command_name]', ctx.command.name))
        if ctx.author.top_role == member.top_role:
            return await ctx.send(messages.field_perms_4.replace('[user]', ctx.author.mention).replace('[username]', ctx.author.name).replace('[command_name]', ctx.command.name))
        if ctx.author.top_role < member.top_role:
            return await ctx.send(messages.field_perms_5.replace('[user]', ctx.author.mention).replace('[username]', ctx.author.name).replace('[command_name]', ctx.command.name))
    except Exception:
        pass


def can_handle(ctx, permission: str):
    """ Checks if bot has permissions or is in DMs right now """
    return isinstance(ctx.channel, discord.DMChannel) or getattr(ctx.channel.permissions_for(ctx.guild.me), permission)
