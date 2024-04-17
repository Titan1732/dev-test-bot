import discord
from discord.ext import commands
import typing
import random
from  rsvp_confirmation import dmView, confirmEmbed

#Variables-----------------
rsvp_list = [] #List of users that have RSVP'd
all_views = {}



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

        super().__init__(title="Lorem Ipsum", type="rich")


#Setup for the dropdown-menu displaying the current RSVP list
class rsvpList(discord.ui.Select):
    def __init__(self, options):

        #options = [discord.SelectOption(label=users) for users in rsvp_list] #Read the RSVP list and append each item as a drop-down menu label upon first-creation

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
        assert self.view is not None
        view: discordView = self.view
        user = f"{interaction.user.global_name}{random.randint(1,1000)}"  #Get the user's name who clicked the button  {random.randint(1,1000)}


        await interaction.response.defer(ephemeral=False, thinking=False)
        
        if user not in rsvp_list:
            await rsvpHandling(channelView=view, interaction=interaction, user=user)
        else:
            await interaction.followup.send(f"{interaction.user.mention} - You have already RSVP'd!", ephemeral=True) #Sends notice of already being RSVPd


#Handles the RSVP DM Confirmation and RSVP list additions
async def rsvpHandling(channelView, interaction, user):
    view = dmView()

    if user not in rsvp_list:
        await interaction.user.send(view=view, embed=confirmEmbed)
        await view.wait()

        if view.value == "confirm":
            print("confirmed " + view.value)
            rsvp_list.append(user)

            if await checkListExist(channelView=channelView):
                channelView.children[3].options.append(discord.SelectOption(label=user))
            else:
                channelView.add_item(rsvpList(options=[discord.SelectOption(label=user)]))



        elif view.value == "tenative":
            print("tenative " + view.value)
            rsvp_list.append(user)

            if await checkListExist(channelView=channelView):
                channelView.children[3].options.append(discord.SelectOption(label=user, emoji="⌚"))
            else:
                channelView.add_item(rsvpList(options=[discord.SelectOption(label=user, emoji="⌚")]))



        elif view.value == "cancel":
            print("cancel " + view.value)
        else:
            print(view.value)
        
        await interaction.edit_original_response(view=channelView)



#Module to check if the RSVP list dropdown-menu is actually showing or not
async def checkListExist(channelView):
    selectExists = any(isinstance(obj, rsvpList) for obj in channelView.children)

    if selectExists is False:
        return False
    else:
        return True


#Setup for the time button that displays in-between the RSVP and Info buttons
class timeButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label='8:00 PM', style=discord.ButtonStyle.grey, row=0)
    
    async def callback(self, interaction: discord.Interaction): 
        await interaction.response.defer(ephemeral=False, thinking=False)


#Setup for the info button
class infoButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label='Info', style=discord.ButtonStyle.primary, row=0)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(embed=infoEmbed(), ephemeral=True)




#The actual view that is sent alongside the embed
class discordView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

        self.add_item(rsvpButton()) 
        self.add_item(timeButton())
        self.add_item(infoButton())

        all_views[id(self)] = self
        


class viewSendCog(commands.Cog, name='View'):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    #Placeholder command to summon the view - Will be replaced eventually by method to create events
    @commands.command(name="View")
    @commands.guild_only()
    async def send_view(self, ctx):
        view = discordView()

        test_embed = discord.Embed(title="Lorem Ipsum", type='rich', color=discord.Color.blue(), description='* Lorem ipsum dolor sit amet, consectetur adipiscing elit.\n* Phasellus tortor ligula, ultricies at purus at, sagittis commodo est.\n* Nulla tristique molestie lorem quis volutpat.\n')

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


    @commands.command(name="get")
    async def interact(self, ctx, arg1: typing.Optional[int]):
        keys = list(all_views.keys())
        if arg1 is None:
            await ctx.send(f"Please provide an ID to interact with.\nValid options are {keys}")
        elif arg1 in all_views:
            spec_view = all_views.get(arg1)

            await ctx.send(spec_view.children)
        else:
            await ctx.send(f"Invalid ID provided.\nValid options are {keys}")

            
