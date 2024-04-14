import discord


confirmDescription = "Thanks for showing interest in this event!\n\nBelow, you will see three buttons:\n"
confirmDescription += "* To confirm your attendance to this event, please select Confirm RSVP\n"
confirmDescription += "* To confirm your tenative attendance* to this event, please select Tenative RSVP\n"
confirmDescription += "* To cancel your spot reservation, please select Cancel RSVP\n"
confirmDescription += "\n*Tenative attendance means you are willing to join, but only if more people are needed."

confirmEmbed = discord.Embed(title="RSVP Confirmation", type="rich", description=confirmDescription)





class confirmButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label='Confirm RSVP', style=discord.ButtonStyle.green, row=0)

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: dmView = self.view

        for child in view.children:
            child.disabled=True

        await interaction.response.edit_message(view=view)
        await interaction.followup.send("Thank you for confirming your attendance to EVENT_TITLE")
        self.view.value = "confirm"
        self.view.stop()





class tenativeButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label='Tenative RSVP', style=discord.ButtonStyle.grey, row=0)

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: dmView = self.view

        for child in view.children:
            child.disabled=True

        await interaction.response.edit_message(view=view)
        await interaction.followup.send("Thank you for confirming your tenative attendance to EVENT_TITLE")
        self.view.value = "tenative"
        self.view.stop()






class denyButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label='Cancel RSVP', style=discord.ButtonStyle.danger, row=0)

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: dmView = self.view

        for child in view.children:
            child.disabled=True

        await interaction.response.edit_message(view=view)
        await interaction.followup.send("RSVP for EVENT_TITLE cancelled successfully!")
        self.view.value = "cancel"
        self.view.stop()





class dmView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.value = None

        self.add_item(confirmButton())
        self.add_item(tenativeButton())
        self.add_item(denyButton())


