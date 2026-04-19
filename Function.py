import discord
import numpy as np
import math
from collections import Counter

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

from discord import slash_command
from discord import option

import asyncio
PI = math.pi

a = open('token.txt', 'r')
tokendata = a.read()
TOKEN = f"{tokendata}"
print(tokendata)
a.close()

b = open('guild_id.txt', 'r')
giddata = a.read()
GID = f"{giddata}"
print(giddata)
b.close()


intents = discord.Intents.all()
client = discord.Bot(auto_sync_command=True, intents=intents)


class App(discord.Cog):
    def __init__(self, bot: discord.Bot):
        super().__init__()
        self.bot = bot

    #素因数分解
    @slash_command(
        name = "prime_factorize",
        description = "素因数分解したい数字nを入力",
        guild_ids = [GID]
    )
    @option(
        "n",
        int,
        required = True
    )
    async def prime_factorize(self, ctx: discord.ApplicationContext, n: int):
        m = n
        a = []
        while m % 2 == 0:
            a.append(2)
            m //= 2
        f = 3
        while f * f <= m:
            if m % f == 0:
                a.append(f)
                m //= f
            else:
                f += 2
        if n != 1:
            a.append(m)

        anslist = Counter(a) #個数をカウント
        b = list(set(a))
        print(b)
        print(anslist)
        message = f"{n}を素因数分解すると "

        for i in range(len(b)):
            message += str(b[i]) + "^" + str(anslist[b[i]]) + " * "
        await ctx.respond(message)
    
    #一次関数 y = ax + b
    @slash_command(
        name = "linear",
        description = "一次関数 y = ax + b",
        guild_ids = [GID]
    )
    @option(
        "a",
        int,
        required = True
    )
    @option(
        "b",
        int,
        required = True
    )
    async def linear(self, ctx: discord.ApplicationContext, a: int, b: int):
        x = np.linspace(-10,10,100)
        y = a * x + b
        
        plt.figure()

        #plt.gca().set_aspect('equal', adjustable='box')
        plt.grid(which='major', color='gray', linestyle='--')
        plt.grid(which='minor', color='gray', linestyle='--')

        plt.plot(x,y)
        plt.savefig("./Fig/linear.png")

        file = discord.File("./Fig/linear.png")
        await ctx.respond(file=file)

    #二次関数 y = ax^2 + bx + c
    @slash_command(
        name = "quadratic",
        description = "二次関数 y = ax^2 + bx + c",
        guild_ids = [GID]
    )
    @option(
        "a",
        int,
        required = True
    )
    @option(
        "b",
        int,
        required = True
    )
    @option(
        "c",
        int,
        required = True
    )
    async def quadratic(self, ctx: discord.ApplicationContext, a: int, b: int, c: int):
        x = np.linspace(-10,10,100)
        y = a*x*x + b*x + c
        
        plt.figure()

        #plt.gca().set_aspect('equal', adjustable='box')
        plt.grid(which='major', color='gray', linestyle='--')
        plt.grid(which='minor', color='gray', linestyle='--')

        plt.plot(x,y)
        plt.savefig("./Fig/quadratic.png")

        file = discord.File("./Fig/quadraticr.png")
        await ctx.respond(file=file)
        
    #円/楕円 x=acaos(t), y=bsin(t)
    @slash_command(
        name = "circle",
        description = "円/楕円 x=acos(t), y=bsin(t)",
        guild_ids = [GID]
    )
    @option(
        "a",
        int,
        required = False
    )
    @option(
        "b",
        int,
        required = False
    )
    async def circle(self, ctx: discord.ApplicationContext, a: int=5, b: int=7):
        t = np.linspace(-PI,PI,10000)

        x = a * np.sin(t)
        y = b * np.cos(t)
        
        plt.figure()
        
        plt.plot(x, y ,color="green")
        plt.xlim(-20,20)
        plt.ylim(-20,20)

        plt.gca().set_aspect('equal', adjustable='box')
        plt.grid(which='major', color='gray', linestyle='--')
        plt.grid(which='minor', color='gray', linestyle='--')
        plt.savefig("./Fig/circle.png")

        file = discord.File("./Fig/circle.png")
        await ctx.respond(file=file)
        
    #リサージュ曲線 x=sin(at), y=sin(bt)
    @slash_command(
        name = "lissajous",
        description = "リサージュ曲線 x=sin(at), y=sin(bt)",
        guild_ids = [GID]
    )
    @option(
        "a",
        int,
        required = False
    )
    @option(
        "b",
        int,
        required = False
    )
    async def lissajous(self, ctx: discord.ApplicationContext, a: int=5, b: int=7):
        t = np.linspace(-PI,PI,10000)

        x = np.sin(a * t)
        y = np.sin(b * t)
        
        plt.figure()

        plt.plot(x, y ,color="green")
        plt.xlim(-1.2,1.2)
        plt.ylim(-1.2,1.2)

        plt.gca().set_aspect('equal', adjustable='box')
        plt.grid(which='major', color='gray', linestyle='--')
        plt.grid(which='minor', color='gray', linestyle='--')
        plt.savefig("./Fig/lissajous.png")

        file = discord.File("./Fig/lissajous.png")
        await ctx.respond(file=file)

        await ctx.respond(f"x=sin{a}t,y=sin{b}t")
    
        #リサージュ曲線 x=sin(at), y=sin(bt)
    
    #アステロイド x=cos(t)^a, y=sin(t)^b
    @slash_command(
        name = "asteroid",
        description = "アステロイド曲線 x=cos(t)^a, y=sin(t)^b",
        guild_ids = [GID]
    )
    @option(
        "a",
        int,
        required = False
    )
    @option(
        "b",
        int,
        required = False
    )
    async def asteroid(self, ctx: discord.ApplicationContext, a: int=3, b: int=3):
        t = np.linspace(-PI,PI,10000)

        x = (np.cos(t)) ** a
        y = (np.sin(t)) ** b
        
        plt.figure()

        plt.plot(x, y ,color="green")
        plt.xlim(-1.2,1.2)
        plt.ylim(-1.2,1.2)

        plt.gca().set_aspect('equal', adjustable='box')
        plt.grid(which='major', color='gray', linestyle='--')
        plt.grid(which='minor', color='gray', linestyle='--')
        plt.savefig("./Fig/asteroid.png")

        file = discord.File("./Fig/asteroid.png")
        await ctx.respond(file=file)

        await ctx.respond(f"x=cos(t)^{a},y=sin(t)^{b}")

    # 陰関数 F(x,y) = ax^2+ bxy + cy^2 + dx + ey + f = 0
    @slash_command(
        name = "implicit",
        description = "陰関数 F = 0",
        guild_ids = [GID]
    )
    @option(
        "a",
        int,
        required = False
    )
    @option(
        "b",
        int,
        required = False
    )
    @option(
        "c",
        int,
        required = False
    )
    @option(
        "d",
        int,
        required = False
    )
    @option(
        "e",
        int,
        required = False
    )
    @option(
        "f",
        int,
        required = False
    )
    async def implicit(self, ctx: discord.ApplicationContext
                       ,a: int=1, b: int=0, c: int=1, d: int=0, e: int=0, f: int=-1):
        # x の範囲
        x_range = np.linspace(-10, 10, 1000)
        # y の範囲
        y_range = np.linspace(-10, 10, 1000)

        #格子点の作成
        x, y = np.meshgrid(x_range, y_range)

        # 陰関数 F = 0
        F = a*x**2 + b*x*y + c*y**2 + d*x + e*y + f
        
        plt.figure()

        plt.gca().set_aspect('equal', adjustable='box')
        plt.grid(which='major', color='gray', linestyle='--')
        plt.grid(which='minor', color='gray', linestyle='--')

        plt.contour(x, y, F, [0], colors="blue")   
        plt.savefig("./Fig/implicit.png")

        file = discord.File("./Fig/implicit.png")
        await ctx.respond(file=file)

    #p,q結び目
    @slash_command(
        name = "torusknot",
        description = "p,q結び目",
        guild_ids = [GID]
    )
    @option(
        "p",
        int,
        required = True
    )
    @option(
        "q",
        int,
        required = True
    )
    async def torusknot(self, ctx: discord.ApplicationContext, p: int, q: int):
        n = 100

        #define function
        theta = np.linspace(0, 2.*np.pi, n)
        phi = np.linspace(0, 2.*np.pi, n)
        theta, phi = np.meshgrid(theta, phi)
        x = (5 - np.cos(phi) + np.sin(q*theta))*np.cos(p*theta)
        y = (5 - np.cos(phi) + np.sin(q*theta))*np.sin(p*theta)
        z = np.cos(q*theta) + np.sin(phi)

        #color map
        start_color = "blue"
        end_color = "cyan"
        cmap = mcolors.LinearSegmentedColormap.from_list("my_gradient", [start_color, end_color])

        #plot
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d', facecolor="black")
        ax.set_zlim(-3,3)
        ax.plot_surface(x, y, z, rstride=5, cstride=5, cmap=cmap)
        ax.view_init(90, 45)
        ax.axis("off")
        plt.savefig("./Fig/torusknot.png")

        file = discord.File("./Fig/torusknot.png")
        await ctx.respond(file=file)
    
if __name__ == "__main__":
    client.add_cog(App(bot=client))
    client.run(TOKEN)
