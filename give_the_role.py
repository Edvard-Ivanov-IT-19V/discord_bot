import discord
from discord import utils
import vars_and_roles

class MyClient(discord.Client):
    async def on_ready(self):
        print('\033[1;36;40m Бот \033[1;33;40m {0} \033[1;36;40m онлайн!\033[0;37;40m'.format(self.user))
        print('\033[1;36;40m И готов к ролям!\033[0;37;40m')

    async def on_raw_reaction_add(self, payload):
        if payload.message_id == vars_and_roles.POST_ID:
            channel = self.get_channel(payload.channel_id) # получаем объект канала
            message = await channel.fetch_message(payload.message_id) # получаем объект сообщения
            member = utils.get(message.guild.members, id=payload.user_id) # получаем объект пользователя который поставил реакцию

            try:
                emoji = str(payload.emoji) # эмоджик который выбрал юзер
                role = utils.get(message.guild.roles, id=vars_and_roles.ROLES[emoji]) # объект выбранной роли (если есть)

                if(len([i for i in member.roles if i.id not in vars_and_roles.EXCROLES]) <= vars_and_roles.MAX_ROLES_PER_USER):
                    await member.add_roles(role)
                    print('\033[1;32;40m [SUCCESS] Пользователю {0.display_name} назначена роль {1.name}'.format(member, role))
                else:
                    await message.remove_reaction(payload.emoji, member)
                    print('\033[1;31;40m [ERROR] Превышено кол-во ролей для пользователя {0.display_name}'.format(member))
        
            except KeyError as e:
                print('\033[1;31;40m [ERROR] Роль не найдена для этого ' + emoji)
            except Exception as e:
                print(repr(e))

    async def on_raw_reaction_remove(self, payload):
        channel = self.get_channel(payload.channel_id) # получаем объект канала
        message = await channel.fetch_message(payload.message_id) # получаем объект сообщения
        member = utils.get(message.guild.members, id=payload.user_id) # получаем объект пользователя который поставил реакцию
        
        try:
            emoji = str(payload.emoji) # эмоджик который выбрал юзер
            role = utils.get(message.guild.roles, id=vars_and_roles.ROLES[emoji]) # объект выбранной роли (если есть)

            await member.remove_roles(role)
            print('\033[1;32;40m [SUCCESS] Роль удалена у пользователя {0.display_name}'.format(member, role))

        except KeyError as e:
            print('\033[1;31;40m [ERROR] Роль не найдена для этого ' + emoji)
        except Exception as e:
            print(repr(e))

client = MyClient()
client.run(vars_and_roles.TOKEN)