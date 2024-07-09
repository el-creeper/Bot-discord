# 1/ Importation

# a/ discord + regex

import re
import discord
from discord.ext import commands,tasks

# b/ BeautifulSoup et Requests

import os
import csv
import requests
from bs4 import BeautifulSoup

# 2/ prefixe

bot = commands.Bot(command_prefix='/')

# 3/ démarage du bot

@bot.event
async def on_ready():
    print("ready!")

# 4/ commande

# Les vrais commandes

# Création de fichier



# k/ commande permetant d'ajouter des gens dans la liste des personnes pouvant accéder a /perf

@bot.command()
@commands.has_permissions(ban_members = True)
async def Idpermperf(ctx, id : discord.User):
    await ctx.message.delete()
    with open(r"E:\Projet Felisisa\bot\data.txt", "a") as fichier:
        id = str(id) + "\n"
        fichier.write(str(id))


# j/ permet de savoir la derniere perfs du joueur
def pseudoidtrue(ctx):
    with open(r"E:\Projet Felisisa\bot\data.txt", "r") as f:
        l = f.read().splitlines()
        author = str(ctx.message.author)
        return author in l


# perfs

@bot.command()
@commands.check(pseudoidtrue)
async def perfs(ctx, User : discord.User):
    await ctx.message.delete()


    #On définit url de la page


    chaine = str(User)
    epic = ""
    with open(r"E:\Projet Felisisa\bot\link.txt", "r") as fichier:
        lignes = fichier.read().splitlines()
        for ligne in lignes:
            if chaine in ligne:
                print(ligne)
                _, epic = ligne.split("=")
                print(epic)
                break

    if epic == "":
        print("Error, cannot find epic")

    epics = "%20".join(epic.split(" "))

    avatar = User.avatar_url
    p1 = "https://fortnitetracker.com/profile/all/"
    p2 = "/events?plat=Global&region=GLOBAL"
    url = p1+epics+p2
    print(url)
    #requete a la page
    requete = requests.get(url)
    page = requete.content

    s = str(page)
    for c in ["\\n","\\t","\\r"," ","-"]:
        s = s.replace(c, "")
    #print(s)
        tournois = re.findall('"windowId":"(\w+)","doneLoading":(true|false),"teamId":"[\w-]+","accountIds":\[[^\]]+\],"pointsEarned":(\d+),"rank":(\d+),"percentile":([\d\.]+),', s)
    embed = discord.Embed(title = "**__"+str(epic)+"__**", description = "Tournois", url = url, color = 0x008080)
    embed.set_thumbnail(url = avatar)
    embed.set_author(name = User)
    embed.set_footer(text = "Bot créé par FLS Creeper")

    compteur = 0
    x=1
    for tournoi in tournois:
        if compteur>30:
            await ctx.send(embed = embed)
            compteur = 0
            embed = discord.Embed(title = "**__"+str(epic)+"__**", description = "Tournois", url = url, color = 0x008080)
            embed.set_thumbnail(url = avatar)
            embed.set_author(name = User)
            embed.set_footer(text = "Bot créé par FLS Creeper")

        else:
            (id, dl, pts, rank, pourcentage) = tournoi
            print("Tournoi", id, "avec", pts, "points et un rang", rank, "avec pourcentage", float(pourcentage)*100, "%")
            #embed
            pts = f"{pts} pts"
            pourcentage = f"{float(pourcentage)*100}"[:4] + "%"
            id = " ".join(id.split("_"))
            embed.add_field(name =  id, value = str(rank) + "°\n" + str(pts) + "\n" + str(pourcentage), inline = True)
            compteur = compteur+1

    await ctx.send(embed = embed)


# l/  link

@bot.command()
async def link(ctx, User : discord.User, *epic):
    await ctx.message.delete()
    chaine = str(User)
    epic = " ".join(epic)
    with open(r"E:\Projet Felisisa\bot\link.txt", "r") as fichier:
        lignes = fichier.read().splitlines()
        for ligne in lignes:
            if chaine in ligne:
                embed = discord.Embed(title = "Votre compte est déjà link", color = 0xffc63a)
                embed.add_field(name = f"{User} est déjà link", value = "*Si vous voulez unlink votre compte faite /unlink [pseudo discord] [pseudo epic]*")
                embed.set_footer(text = "Bot créé par FLS Creeper")
                await ctx.send(embed = embed)
                return

    fichier = open(r"E:\Projet Felisisa\bot\link.txt", "a")
    message = str(User) +"=" +str(epic) +"\n"
    fichier.write(message)
    fichier.close()
    embed = discord.Embed(title = "Votre compte a bien été link", color = 0x00FF00)
    embed.add_field(name = f"{User} a été link a {epic}", value = "*Si vous voulez unlink votre compte faite /unlink [pseudo discord] [pseudo epic]*")
    embed.set_footer(text = "Bot créé par FLS Creeper")
    await ctx.send(embed = embed)

# m/ unlink

@bot.command()
async def unlink(ctx, User : discord.User, *epic):
    await ctx.message.delete()
    epic = " ".join(epic)
    chaine = str(User) +"=" +str(epic)
    a = 0
    with open(r"E:\Projet Felisisa\bot\link.txt", "r+") as f:
        d = f.readlines()
        f.seek(0)
        for i in d:
            if i.strip("\n") != chaine:
                f.write(i)


            else:
                print("GG", chaine)
                embed = discord.Embed(title = "Votre compte a bien été unlink", color =  0xffc63a)
                embed.add_field(name = f"{User} n'est plus link", value = "*Pour link votre compte faite /link [pseudo disord] [pseudo epic]*")
                embed.set_footer(text = "Bot créé par FLS Creeper")
                await ctx.send(embed = embed)
                a = 1
                break
        f.truncate()
        if a == 1:
            print("Finit")
        else:
            embed = discord.Embed(title = "Votre compte n'est pas link'", color =  0xFF0000)
            embed.add_field(name = f"{User} n'a pas été link avec {epic}", value = "*Pour link votre compte faite /link [pseudo disord] [pseudo epic]*")
            embed.set_footer(text = "Bot créé par FLS Creeper")
            await ctx.send(embed = embed)



@bot.command()
async def maj(ctx, unite = "hours", temps = 24):
    if unite == "seconds":
        majs.start()
        majs.change_interval(seconds = int(temps))
    elif unite == "minutes":
        majs.start()
        majs.change_interval(minutes = int(temps))
    elif unite == "hours":
        majs.start()
        majs.change_interval(hours = int(temps))
    else:
        await ctx.send(unite + " n'est pas définit comme une unité valide'")

@tasks.loop(minutes = 1)
async def majs():
    ctx = []
    print("MAJ des embed")
    msg = True
    while msg != None:
        #client = discord.ext.commands.Bot(733048408826183740)
        channel = bot.get_channel(733099482354286708)
        msg = await channel.history().get(author__name='Fortnite Competitive')
        if msg == None:
            print("Pas trouvé de message")
        else:
            print(msg)
            await msg.delete()

    with open(r"E:\Projet Felisisa\bot\link.txt", "r") as fichier:
        lignes = fichier.read().splitlines()
        for ligne in lignes:
            print(ligne)
            pseudo = ligne.split("=")
            user = pseudo[0]
            _, epic = ligne.split("=")
            print(pseudo)
            print(epic)
            epics = "%20".join(epic.split(" "))
            avatar = bot.user.avatar_url
            p1 = "https://fortnitetracker.com/profile/all/"
            p2 = "/events?plat=Global&region=GLOBAL"
            url = p1+epics+p2
            print(url)
            requete = requests.get(url)
            page = requete.content
            s = str(page)
            for c in ["\\n","\\t","\\r"," ","-"]:
                s = s.replace(c, "")
            #print(s)
            tournois = re.findall('"windowId":"(\w+)","doneLoading":(true|false),"teamId":"[\w-]+","accountIds":\[[^\]]+\],"pointsEarned":(\d+),"rank":(\d+),"percentile":([\d\.]+),', s)
            embed = discord.Embed(title = "**__"+str(epic)+"__**", description = "Tournois", url = url, color = 0x008080)
            embed.set_author(name = user)
            embed.set_footer(text = "Bot créé par FLS Creeper")

            compteur = 0

            for tournoi in tournois:
                if compteur>30:
                    await channel.send(embed = embed)
                    compteur = 0

                    embed = discord.Embed(title = "**__"+str(epic)+"__**", description = "Tournois", url = url, color = 0x008080)
                    embed.set_author(name = user)
                    embed.set_footer(text = "Bot créé par FLS Creeper")

                else:
                    (id, dl, pts, rank, pourcentage) = tournoi
                    print("Tournoi", id, "avec", pts, "points et un rang", rank, "avec pourcentage", float(pourcentage)*100, "%")
                    #embed
                    pts = f"{pts} pts"
                    pourcentage = f"{float(pourcentage)*100}"[:4] + "%"
                    id = " ".join(id.split("_"))
                    embed.add_field(name =  id, value = str(rank) + "°\n" + str(pts) + "\n" + str(pourcentage), inline = True)
                    compteur = compteur+1

            await channel.send(embed = embed)




bot.run("NzMzMDQ4NDA4ODI2MTgzNzQw.Xw9eiA.6Amf1C87mpaMmFOCmZDK8KKphDI")