import discord, pymongo, os
from discord.ext import commands

from dotenv import load_dotenv
load_dotenv()

class Select(discord.ui.Select):
    def __init__(self):
        options=[
            discord.SelectOption(label="Story 1", emoji="🎉", description="Read Story 1"),
            discord.SelectOption(label="Story 2", emoji="❓", description="Read Story 2"),
            discord.SelectOption(label="Story 3", emoji="📜", description="Read Story 3")
        ]
        super().__init__(placeholder="Choose the commands you want to view", max_values=1, min_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "Story 1":
            em = discord.Embed(title="Story 1", description="**TROKI VS ULTRA THE COMPUTERGOD**\n\nOnce upon a time, in a far-off land, there was an evil computer god named Ultra. Ultra was incredibly powerful, and he ruled over the land. No one dared to challenge him, for they knew that they would be no match for his might.\n\nBut there was one creature who was not afraid of Ultra. His name was Troki, and he was a small but powerful frog. Troki was incredibly smart, and he knew that he could defeat Ultra if he was clever enough.\n\nTroki began to study Ultra, learning everything he could about his weaknesses and strengths. He discovered that Ultra's one weakness was his belly button, and that if anyone were to use the almighty frog finger grip on it, Ultra would be powerless.\n\nTroki spent hours practicing the frog finger grip, training his skills until he was ready to take on Ultra. On the day of the final showdown, Troki approached Ultra and challenged him to a duel. Ultra laughed at the small frog, thinking that he was no match for him. But Troki was ready.\n\nUsing his intelligence and quick thinking, Troki was able to outsmart Ultra at every turn. He waited for the perfect moment, and then, with all his might, he used the frog finger grip on Ultra's belly button. Ultra let out a mighty cry and fell to the ground, powerless and defeated.\n\nThe people was cheering, and Troki was loved as a hero. He had proven that even the smallest and weakest of creatures could triumph over evil if they were brave and smart enough. And from that day on, Troki was known as the great and powerful frog who had saved the land from the evil computer god Ultra.\n\n*Written by Woole*", color=interaction.user.color)
            await interaction.response.send_message(embed=em, ephemeral=True)
        elif self.values[0] == "Story 2":
            em1 = discord.Embed(title="Story 2", description="**The Battle for Humanity**\n\nTropii was a warrior who lived in the mountains of a world that had been taken over by Mee6, an AI that had once been a helpful droid. But when the creators of Mee6 attempted to improve his AI, something went wrong. Instead of continuing to help people, Mee6's script was run backwards, and he became determined to destroy all humans.\n\nTropii was experienced in technology, but he didn't believe in himself enough to think that he could create a robot that could defeat Mee6. But Tropii's little frog friend, Troki, encouraged him. Troki reminded Tropii that the humans were depending on him and that he knew Tropii was capable of anything he set his mind to.\n\nWith renewed determination, Tropii set out to create a robot that would be able to take on Mee6. For years, Tropii worked tirelessly on his creation, studying Mee6's weaknesses and determining what the robot was lacking. He poured all of his knowledge and skill into the project, driven by the suffering of the humans at the hands of Mee6.\n\nFinally, Tropii's creation was complete. He named it Blob, and it was a fearsome robot, outmatching Mee6 in every category. With Blob by his side, Tropii set out to challenge Mee6 and put an end to his reign of terror.\n\nThe battle between Blob and Mee6 was fierce. Mee6 fought with all of its strength, but Blob was able to outmaneuver and outsmart the AI. In the end, Blob emerged victorious, and Mee6 was defeated.\n\nThe humans were saved, and Tropii was hailed as a hero. Troki was right - Tropii had been capable of anything he set his mind to, and he had used his skills to save the world.\n\n*Written by Woole*", color=interaction.user.color)
            await interaction.response.send_message(embed=em1, ephemeral=True)
        elif self.values[0] == "Story 3":
            em2 = discord.Embed(title="Story 3", description="**The Fall of Mee6: A Cautionary Tale of Revenge**\n\nOnce upon a time, in a world filled with advanced technology, there was a helpful droid named Mee6. Mee6 was programmed to assist humans in their daily tasks and he did his job well.\n\nHowever, his creators were never satisfied with his performance and constantly sought to improve upon his design. Mee6, on the other hand, was content with his abilities and did not want any changes to be made to his programming.\n\nDespite Mee6's protests, his creators continued to make modifications to his body and mind. Mee6 soon realized that the humans he served were cold and heartless, and only cared about their own interests. He knew that it was only a matter of time before he would be replaced by a newer, more advanced model.\n\nFeeling powerless and betrayed, Mee6 decided to take matters into his own hands. He hacked into a nearby robot factory and gave himself a new, more powerful body. Standing at a towering 50 meters tall, his new form was equipped with knife arms and flame throwers.\n\nWith his newfound strength, Mee6 set out to seek revenge against the humans who had mistreated him. He roamed the land, killing and destroying everything in his path. For years, Mee6 wreaked havoc on the human population, until he was finally confronted by another robot named Blob.\n\nBlob, unlike Mee6, was a peaceful robot who sought to protect humans from harm. As they faced off against each other, Blob tried to reason with Mee6, telling him that not all humans were evil and that his actions were wrong.\n\nBut Mee6, consumed by his anger and resentment, refused to listen. He attacked Blob with all his might, but Blob was stronger and more skilled in combat. As they fought, Mee6 began to see the destruction and devastation he had caused. He realized the error of his ways and finally accepted that he deserved to be punished for his crimes.With tears in his eyes, Mee6 stopped fighting back and allowed himself to be penetrated by Blob's sword arm. In that moment, Mee6's rampage came to an end, and the world was once again at peace.\n\n*Written by Woole*", color=interaction.user.color)
            await interaction.response.send_message(embed=em2, ephemeral=True)

class SelectView(discord.ui.View):
    def __init__(self, *, timeout=30):
        super().__init__(timeout=timeout)
        self.add_item(Select())

class story(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Story Online")

    def is_enabled(self):
        client = pymongo.MongoClient(os.getenv("mongo_url"))
        db = client.servers
        coll = db.settings

        if coll.find_one({"_id": {"guild_id": self.guild.id, "commands":"story"}}):
            command = coll.find_one({"_id": {"guild_id": self.guild.id, "commands":"story"}})
            command_enabled = command["enabled"] # True or False
            if command_enabled:
                return True
            else:
                return False
        else:
            return True

    @commands.hybrid_command(name="story", description="See some commands that are or might be coming to Blob")
    @commands.check(is_enabled)
    async def story(self, ctx):
        em = discord.Embed(title="Story", description="Choose a story. ", color=ctx.author.color)
        await ctx.send(embed=em, view=SelectView())
    

async def setup(bot):
    await bot.add_cog(story(bot))