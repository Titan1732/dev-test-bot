import discord
from discord.ext import commands
import typing
import random
from  rsvp_confirmation import dmView, confirmEmbed

#Variables-----------------
rsvp_list = [] #List of users that have RSVP'd



class infoEmbed(discord.Embed):
    def __init__(self):

        self.rules = (
            "* Lorem ipsum dolor sit amet, consectetur adipiscing elit.\n"
            "* Phasellus tortor ligula, ultricies at purus at, sagittis commodo est.\n"
            "* Nulla tristique molestie lorem quis volutpat.\n"
        )

        self.add_field(name="**Rules**:", value=self.rules, inline=True)
        self.add_field(name="**Lobby Password**:", value="pwr\n", inline=False)
        self.add_field(name="**Event Type**:", value="Official", inline=False)

        self.set_footer(text="\nSupport the club! \nhttps://www.patreon.com/user?u=81785397")

        super().__init__(title="Flex Friday 💪", type="rich")


#Setup for the dropdown-menu displaying the current RSVP list
class rsvpList(discord.ui.Select):
    def __init__(self):

        options = [discord.SelectOption(label=users) for users in rsvp_list] #Read the RSVP list and append each item as a drop-down menu label upon first-creation

        super().__init__(placeholder='RSVP List', min_values=1, max_values=1, options=options) #Set up the actual menu & its parameters

    async def callback(self, interaction: discord.Interaction): #callback function that is performed when an action is taken in the menu
        assert self.view is not None
        view: discordView = self.view

        await interaction.response.edit_message(view=view)      #Refresh the view to reset the selection


#Setup for the RSVP button
class rsvpButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label='RSVP', style=discord.ButtonStyle.green, row=0)


    async def callback(self, interaction: discord.Interaction): #callback function that is performed when an action is taken on the button
        #Variables-----------------
        global rsvp_list
        assert self.view is not None
        view: discordView = self.view
        self.user = f"{interaction.user.global_name}{random.randint(1,1000)}"  #Get the user's name who clicked the button

        #Adds the user's discord name to the rsvp_list if not already added.
        if self.user not in rsvp_list:
            rsvp_list.append(self.user) 

            #Check if the drop-down menu is currently present. If not, add it.
            selectExists = any(isinstance(obj, rsvpList) for obj in self.view.children)

            if selectExists is False:
                self.view.add_item(rsvpList())
            else:                            #If it is present, add new name to it instead.
                self.view.children[3].options.append(discord.SelectOption(label=self.user))
            
        
            await interaction.response.edit_message(view=view)  #Refresh the view to add new names to the RSVP list
            #await interaction.followup.send(f"RSVP Confirmed for {interaction.user.mention}", ephemeral=True) #Sends RSVP confirmation message
            await interaction.user.send(view=dmView(), embed=confirmEmbed)

        else:
            await interaction.response.send_message(f"{interaction.user.mention} - You have already RSVP'd!", ephemeral=True, delete_after=180) #Sends notice of already being RSVPd




class timeButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label='8:00 PM', style=discord.ButtonStyle.grey, row=0, disabled=True)


class infoButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label='Info', style=discord.ButtonStyle.primary, row=0)

    async def callback(self, interaction: discord.Interaction):
        global rulesEmbed
        await interaction.response.send_message(embed=infoEmbed(), ephemeral=True)


#The actual view that is sent alongside the embed
class discordView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

        self.add_item(rsvpButton()) 
        self.add_item(timeButton())
        self.add_item(infoButton())
        


class viewSendCog(commands.Cog, name='View'):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    #Placeholder command to summon the view - Will be replaced eventually by method to create events
    @commands.command(name="View")
    @commands.guild_only()
    async def send_view(self, ctx):
        view = discordView()

        test_embed = discord.Embed(title="Flex Friday 💪 starts today at `8:00 PM`", type='rich', color=discord.Color.blue(), description='Embed Placeholder Description')

        await ctx.send(embed=test_embed , view=view)


    #Placeholder command to manually add/remove from RSVP list
    @commands.command(name="rsvp")
    @commands.guild_only()
    async def rsvp_edit(self, ctx, arg1: typing.Optional[str], arg2: typing.Optional[str]):

        if arg1 is not None:
            arg1 = arg1.lower()
            if arg1 == "add":
                if arg2 is not None:
                    await ctx.send(f"Not yet implemented, but adding {arg2} to RSVP list")
                else:
                    await ctx.send("Syntax error: `rsvp add discordName`")

            elif arg1 == "del":
                if arg2 is not None:
                    await ctx.send(f"Not yet implemented, but removing {arg2} to RSVP list")
                else:
                    await ctx.send("Syntax error: `rsvp del discordName`")

            else:
                await ctx.send("Syntax error: `rsvp add|del discordName`")
        else:
                await ctx.send("Syntax error: `rsvp add|del discordName`")
