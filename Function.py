import discord
import numpy as np
import math
from collections import Counter

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

from discord import slash_command
from discord import option

import os
import io

PI = math.pi

# --- トークン・ギルドID読み込み ---
with open('token.txt', 'r') as a:
    TOKEN = a.read().strip()

with open('guild_id.txt', 'r') as b: 
    GID = int(b.read().strip()) 

os.makedirs('./Fig', exist_ok=True)

intents = discord.Intents.all()
client = discord.Bot(auto_sync_commands=True, intents=intents)


class App(discord.Cog):
    def __init__(self, bot: discord.Bot):
        super().__init__()
        self.bot = bot

    # -------------------------
    # 素因数分解
    # -------------------------
    @slash_command(
        name="prime_factorize",
        description="素因数分解したい数字 n を入力",
        guild_ids=[GID]
    )
    @option("n", int, required=True, description="素因数分解する正の整数")
    async def prime_factorize(self, ctx: discord.ApplicationContext, n: int):
        # --- 入力チェック ---
        if n <= 1:
            await ctx.respond(f"`n = {n}` は素因数分解できません（2以上の整数を入力してください）")
            return

        # --- 素因数分解 ---
        m = n
        factors = []

        while m % 2 == 0:
            factors.append(2)
            m //= 2

        f = 3
        while f * f <= m:
            while m % f == 0:
                factors.append(f)
                m //= f
            f += 2

        if m > 1:
            factors.append(m)

        # --- 結果を整形（見やすく） ---
        count = Counter(factors)
        primes_sorted = sorted(count.keys())

        # 例: 360 = 2³ × 3² × 5¹
        factor_strs = []
        for p in primes_sorted:
            exp = count[p]
            if exp == 1:
                factor_strs.append(str(p))
            else:
                # Unicodeの上付き数字に変換
                sup_map = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
                factor_strs.append(f"{p}{str(exp).translate(sup_map)}")

        formula = " × ".join(factor_strs)

        # 指数表記も併記（コピペしやすいように）
        formula_plain = " * ".join(
            f"{p}^{count[p]}" for p in primes_sorted
        )

        message = (
            f"**{n}** の素因数分解\n"
            f"```\n"
            f"{n} = {formula}\n"
            f"```\n"
            f"（テキスト形式: `{n} = {formula_plain}`）"
        )
        await ctx.respond(message)


        x = np.linspace(-10, 10, 100)
        y = a * x**2 + b * x + c

        fig, ax = plt.subplots()
        ax.grid(which='major', color='gray', linestyle='--')
        ax.plot(x, y, label=f"y = {a}x² + {b}x + {c}")
        ax.legend()
        ax.set_title(f"y = {a}x² + {b}x + {c}")
        fig.savefig("./Fig/quadratic.png")
        plt.close(fig)

        await ctx.respond(file=discord.File("./Fig/quadratic.png"))

    # -------------------------
    # 円/楕円 x=acos(t), y=bsin(t)
    # -------------------------
    @slash_command(
        name="circle",
        description="円/楕円 x=acos(t), y=bsin(t) のグラフを描画",
        guild_ids=[GID]
    )
    @option("a", int, required=False, description="x 方向の半径（デフォルト: 5）")
    @option("b", int, required=False, description="y 方向の半径（デフォルト: 7）")
    async def circle(self, ctx: discord.ApplicationContext, a: int = 5, b: int = 7):
        t = np.linspace(-PI, PI, 10000)
        x = a * np.cos(t)
        y = b * np.sin(t)

        fig, ax = plt.subplots()
        ax.set_aspect('equal', adjustable='box')
        ax.grid(which='major', color='gray', linestyle='--')
        ax.plot(x, y, color="green", label=f"x=a·cos(t), y=b·sin(t)  (a={a}, b={b})")
        ax.set_xlim(-20, 20)
        ax.set_ylim(-20, 20)
        ax.legend()
        ax.set_title(f"楕円  a={a}, b={b}")
        
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        plt.close(fig)
        buf.seek(0)  # 読み込み位置を先頭に戻す

        file = discord.File(buf, filename="graph.png")
        await ctx.respond(file=file)

    # -------------------------
    # リサージュ曲線 x=sin(at), y=sin(bt)
    # -------------------------
    @slash_command(
        name="lissajous",
        description="リサージュ曲線 x=sin(at), y=sin(bt) のグラフを描画",
        guild_ids=[GID]
    )
    @option("a", int, required=False, description="x の周波数（デフォルト: 5）")
    @option("b", int, required=False, description="y の周波数（デフォルト: 7）")
    async def lissajous(self, ctx: discord.ApplicationContext, a: int = 5, b: int = 7):
        t = np.linspace(-PI, PI, 10000)
        x = np.sin(a * t)
        y = np.sin(b * t)

        fig, ax = plt.subplots()
        ax.set_aspect('equal', adjustable='box')
        ax.grid(which='major', color='gray', linestyle='--')
        ax.plot(x, y, color="green")
        ax.set_xlim(-1.2, 1.2)
        ax.set_ylim(-1.2, 1.2)
        ax.set_title(f"リサージュ曲線  x=sin({a}t), y=sin({b}t)")

        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        plt.close(fig)
        buf.seek(0)  # 読み込み位置を先頭に戻す

        file = discord.File(buf, filename="graph.png")
        await ctx.respond(file=file)

    # -------------------------
    # アステロイド x=cos(t)^a, y=sin(t)^b
    # -------------------------
    @slash_command(
        name="asteroid",
        description="アステロイド曲線 x=cos(t)^a, y=sin(t)^b のグラフを描画",
        guild_ids=[GID]
    )
    @option("a", int, required=False, description="cos の指数（デフォルト: 3）")
    @option("b", int, required=False, description="sin の指数（デフォルト: 3）")
    async def asteroid(self, ctx: discord.ApplicationContext, a: int = 3, b: int = 3):

        t = np.linspace(-PI, PI, 10000)
        x = np.cos(t) ** a
        y = np.sin(t) ** b

        fig, ax = plt.subplots()
        ax.set_aspect('equal', adjustable='box')
        ax.grid(which='major', color='gray', linestyle='--')
        ax.plot(x, y, color="green")
        ax.set_xlim(-1.2, 1.2)
        ax.set_ylim(-1.2, 1.2)
        ax.set_title(f"アステロイド  x=cos(t)^{a}, y=sin(t)^{b}")
        
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        plt.close(fig)
        buf.seek(0)  # 読み込み位置を先頭に戻す

        file = discord.File(buf, filename="graph.png")
        await ctx.respond(file=file)
    
    # -------------------------
    # 陰関数 F(x,y) = ax² + bxy + cy² + dx + ey + f = 0
    # -------------------------
    @slash_command(
        name="implicit",
        description="陰関数 F(x,y) = ax²+bxy+cy²+dx+ey+f = 0 のグラフを描画",
        guild_ids=[GID]
    )
    @option("a", int, required=True, description="x² の係数")
    @option("b", int, required=True, description="xy の係数")
    @option("c", int, required=True, description="y² の係数")
    @option("d", int, required=True, description="x の係数")
    @option("e", int, required=True, description="x の係数")
    @option("f", int, required=True, description="定数項")
    async def implicit(self, ctx: discord.ApplicationContext,
                       a: int, b: int, c: int, d: int, e: int, f: int):
        x_range = np.linspace(-10, 10, 1000)
        y_range = np.linspace(-10, 10, 1000)
        x, y = np.meshgrid(x_range, y_range)
        F = a*x**2 + b*x*y + c*y**2 + d*x + e*y + f

        fig, ax = plt.subplots()
        ax.set_aspect('equal', adjustable='box')
        ax.grid(which='major', color='gray', linestyle='--')
        ax.contour(x, y, F, [0], colors="blue")
        ax.set_title(f"F = {a}x²+{b}xy+{c}y²+{d}x+{e}y+{f} = 0")

        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        plt.close(fig)
        buf.seek(0)  # 読み込み位置を先頭に戻す

        file = discord.File(buf, filename="graph.png")
        await ctx.respond(file=file)

    # -------------------------
    # p,q トーラス結び目
    # -------------------------
    @slash_command(
        name="torusknot",
        description="p,q トーラス結び目を描画",
        guild_ids=[GID]
    )
    @option("p", int, required=True)
    @option("q", int, required=True)
    async def torusknot(self, ctx: discord.ApplicationContext, p: int, q: int):
        n = 100
        theta = np.linspace(0, 2.*np.pi, n)
        phi = np.linspace(0, 2.*np.pi, n)
        theta, phi = np.meshgrid(theta, phi)
        x = (5 - np.cos(phi) + np.sin(q*theta)) * np.cos(p*theta)
        y = (5 - np.cos(phi) + np.sin(q*theta)) * np.sin(p*theta)
        z = np.cos(q*theta) + np.sin(phi)

        cmap = mcolors.LinearSegmentedColormap.from_list("my_gradient", ["blue", "cyan"])

        fig = plt.figure()
        ax = fig.add_subplot(projection='3d', facecolor="black")
        ax.set_zlim(-3, 3)
        ax.plot_surface(x, y, z, rstride=5, cstride=5, cmap=cmap)
        ax.view_init(90, 45)
        ax.axis("off")

        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        plt.close(fig)
        buf.seek(0)  # 読み込み位置を先頭に戻す

        file = discord.File(buf, filename="graph.png")
        await ctx.respond(file=file)

if __name__ == "__main__":
    client.add_cog(App(bot=client))
    client.run(TOKEN)