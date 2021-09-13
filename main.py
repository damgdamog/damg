import discord, config, json
from discord.ext import commands, tasks
from utils import messages, permissions, Countdown

bot = commands.Bot(command_prefix=config.command_prefix)

@bot.event
async def on_ready():
	print(messages.on_ready_message)
	check_data.start()

@permissions.has_permissions(manage_roles=True)
@bot.command(name=config.tempRole_name, aliases=config.tempRole_aliases, help=messages.tempRole_help)
async def temp_role(ctx, member: discord.Member = None, role: discord.Role = None, time_format: str = None):
	if await permissions.check_priv(ctx, member):
		return
	if member is None or role is None or time_format is None:
		return await ctx.send(messages.tempRole_usage.replace('[user]', ctx.author.mention).replace('[userName]', ctx.author.name).replace('[prefix&command]', ctx.prefix+ctx.command.name))

	expiry = Countdown.Countdown(time_format)
	if expiry.errorMessage != '':
		return await ctx.send(expiry.errorMessage)

	try:
		await member.add_roles(role)
	except Exception as e:
		return await ctx.send(str(e))

	date = expiry.getDate()

	data = {
		"id": member.id,
		"role_id": role.id,
		"guild": ctx.guild.id,
		"until": date.strftime('%Y-%m-%d %H:%M:%S'),
		'24h_alert': False
	}

	with open('./data/data.json', 'r') as openfile:
		json_object = json.load(openfile)

	index = 0
	for item in json_object:
		if member.id == item['id']:
			json_object.pop(index)
			index = index + 1
	json_object.append(data)
	with open("./data/data.json", "w") as outfile:
		json.dump(json_object, outfile)

	await member.add_roles(role)
	await ctx.send(messages.tempRole_done.replace('[role]', str(role)).replace('[user]', member.mention).replace('[userName]', member.name).replace('[time_format]', Countdown.timeToNow(date.strftime('%Y-%m-%d %H:%M:%S'))))

@permissions.has_permissions(manage_roles=True)
@bot.command(name=config.renew_name, aliases=config.renew_aliases, help=messages.renew_help)
async def renew(ctx, member: discord.Member = None, role: discord.Role = None, time_format: str = None):
	if member is None or time_format is None or role is None:
		return await ctx.send(messages.renew_usage.replace('[user]', ctx.author.mention).replace('[userName]', ctx.author.name).replace('[prefix&command]', ctx.prefix+ctx.command.name))

	expiry = Countdown.Countdown(time_format)
	if expiry.errorMessage != '':
		return await ctx.send(expiry.errorMessage)
	date = expiry.getDate()

	with open('./data/data.json', 'r') as openfile:
		json_object = json.load(openfile)
	
	found = False
	index = 0
	for item in json_object:
		if member.id == item['id']:
			if role.id == item['role_id']:
				found = True
				json_object.pop(index)
				break

	if not found:
		return await ctx.send(messages.data_not_found.replace('[user]', ctx.author.mention).replace('[userName]', ctx.author.name))

	item['until'] = date.strftime('%Y-%m-%d %H:%M:%S')

	with open('./data/data.json', 'r') as openfile:
		json_object = json.load(openfile)
	json_object.append(item)
	with open("./data/data.json", "w") as outfile:
		json.dump(json_object, outfile)

	await ctx.send(messages.renew_done.replace('[role]', str(role)).replace('[user]', member.mention).replace('[userName]', member.name).replace('[time_format]', Countdown.timeToNow(date.strftime('%Y-%m-%d %H:%M:%S'))))

@bot.event
async def on_member_update(before, after):
	index = 0
	for item in json_object:
		if after.id == item['id']:
			if after.guild.id != item['guild']:
				continue
			role = after.guild.get_role(item['role_id'])
			if role is None:
				continue
			if not role in before.roles:
				continue
			if not role in after.roles:
				with open('./data/data.json', 'r') as openfile:
					json_object = json.load(openfile)
				json_object.pop(index)
				with open("./data/data.json", "w") as outfile:
					json.dump(json_object, outfile)
		index = index + 1


@tasks.loop(seconds=5.0)
async def check_data():
	with open('./data/data.json', 'r') as openfile:
		json_object = json.load(openfile)
	index = 0
	for item in json_object:
		if Countdown.time_to_now_in_seconds(item['until']) <= 0:
			json_object.pop(index)
			with open("./data/data.json", "w") as outfile:
				json.dump(json_object, outfile)
			guild = await bot.fetch_guild(item['guild'])
			if guild is None :
				continue
			member = await guild.fetch_member(item['id'])
			if member is None: 
				continue
			role = guild.get_role(item['role_id'])
			if role == None:
				continue
			await member.remove_roles(role)
		elif Countdown.time_to_now_in_seconds(item['until']) <= 86400:
			if not item['24h_alert']:
				guild = await bot.fetch_guild(item['guild'])
				if guild is None :
					continue
				member = await guild.fetch_member(item['id'])
				if member is None: 
					continue
				await member.send(messages.time_24h_alert.replace('[user]', member.mention).replace('[userName]', member.name))
				json_object.pop(index)
				item['24h_alert'] = True
				json_object.append(item)
				with open("./data/data.json", "w") as outfile:
					json.dump(json_object, outfile)
	index = index + 1


bot.run(config.token)