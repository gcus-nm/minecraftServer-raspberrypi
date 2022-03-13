# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 12:28:29 2022

@author: gcus_nm12
"""

import os
import socket
import discord.ext
from discord.ext import commands
from discord.ext import tasks
import subprocess

# デフォルトチャンネルID　（今は開発用サーバーのチャンネル）
default_channel = 951654109788905502

# 送信先チャンネルID
send_channel = 0

client = commands.Bot(command_prefix='#')
prevConnection = 76534639315283

# Python（Bot）起動時
@client.event
async def on_ready():
    
    #　サーバー接続チェック開始
    SurveillanceServer.start()
    
    # 送信チャンネルのデフォルト設定
    global send_channel
    global default_channel
    
    send_channel = client.get_channel(default_channel)
    print("Bot Start.")
    
# commandコマンド
@client.command()
async def command(ctx):
    
    # 送信者がbotである場合は弾く
    if ctx.message.author.bot:
        return 
    
    # チャンネルIDを保存
    global send_channel
    send_channel = ctx.message.channel
    # チャンネルにメッセージ送信
    await send_channel.send("現在有効なコマンド\n#start\tサーバーの起動\n#reboot\tPCの再起動")

# startコマンド
@client.command()
async def start(ctx, version = "1.18.1P", ram = 6):
    
    # 送信者がbotである場合は弾く
    if ctx.message.author.bot:
        return 
    
    # チャンネルIDを保存
    global send_channel
    send_channel = ctx.message.channel
    
    # javaバージョン
    javaVer = "17"
    
    # チャンネルにメッセージ送信
    await send_channel.send("サーバーの起動を開始します...")
    
    if (version == "takumi" or version == "Takumi" or version == "TAKUMI"):
        version = "1.12.2Mohist"
        javaVer = "8"
    
    # 起動コマンドをシェルで起動
    command = "bash /home/pi/minecraft/Git/build.sh";
    command = command + " " + str(version) + " " + str(ram) + " " + str(javaVer)
    
    subprocess.run(command, shell=True)
    
# rebootコマンド
@client.command()
async def reboot(ctx):
    
    # 送信者がbotである場合は弾く
    if ctx.message.author.bot:
        return 
    
    # チャンネルIDを保存
    global send_channel
    send_channel = ctx.message.channel
    # チャンネルにメッセージ送信
    await send_channel.send("サーバーPCの再起動を行います。")
    
    # リブート
    subprocess.run("sudo reboot", shell=True)
    
# サーバーとの接続が行えるか（サーバーが起動しているか）指定秒おきにチェック
@tasks.loop(seconds=5)
async def SurveillanceServer():
    
    # 前回の接続状況
    global prevConnection
    
    # サーバーアドレス
    serverAdr = 'raspberrypi.local'    
    # ポート
    port = 25565
    
    # 接続テスト
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mySocket.settimeout(5)
    result = mySocket.connect_ex((serverAdr, int(port)))
    
    # 接続成功
    if result == 0:                
        # Botのステータス変更
        stat = discord.Game(name="Minecraft Server")
        await client.change_presence(status=discord.Status.online, activity=stat)
        
        # 前回は接続できなかった場合
        if (prevConnection != result and prevConnection != 76534639315283):
            print("Server Running.")
            await send_channel.send("サーバーが起動しました！")
                       
        
    # 接続失敗
    else:        
        # Botのステータス変更
        stat = discord.Game(name="#start でサーバーを起動できます　")
        await client.change_presence(status=discord.Status.idle, activity=stat)
        
        # 前回は接続できていた場合
        if (prevConnection != result and prevConnection != 76534639315283):
            print("Server Stopped.")
            await send_channel.send("サーバーが停止しました。")
        
    # 今回の接続状況を保存
    prevConnection = result
    
    # 切断
    mySocket.close()
    
    
client.run(os.environ.get('DISCORD_TOKEN'))