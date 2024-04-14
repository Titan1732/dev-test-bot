import discord

class infoEmbed(discord.Embed):
    def __init__(self):

        super().__init__(title="Info Embed", type="rich", description="Put explanation of how to use here, maybe put event info too")


class Confirm(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None


    @discord.ui.button(label='Confirm', style=discord.ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Thanks for confirming your attendance to EVENT_TITLE!')
        self.value = True
        self.stop()

    # This one is similar to the confirmation button except sets the inner value to `False`
    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.grey)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(f'Cancelling RSVP for {interaction.user.global_name}')
        self.value = False
        self.stop()
