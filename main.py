# -*- coding: utf-8 -*-
import requests
import pandas as pd
from datetime import datetime, timedelta
import discord
from discord.ext import commands
import io

# Bot の準備
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='tt!', intents=intents)

# Bot 起動時のイベント
@bot.event
async def on_ready():
    print("booted!")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

# スケジュール取得関数
def get_event_schedule_for_date(target_date, class_id):
    start_date = target_date - timedelta(days=1)
    end_date = target_date

    start_date_iso = start_date.strftime('%Y-%m-%dT19:00:00.000Z')
    end_date_iso = end_date.strftime('%Y-%m-%dT20:00:00.000Z')

    base_url = f"https://portfolio.toba-cmt.ac.jp/api/Calendar/CalendarEvents?schoolClassId={class_id}&startDateTime={{}}&endDateTime={{}}"
    
    cookies = {
      //ここにログインcookieを入力
           }

    response = requests.get(base_url.format(start_date_iso, end_date_iso), cookies=cookies)

    if response.status_code == 200:
        try:
            data = response.json()
        except ValueError as e:
            return f"JSONデコードエラー: {e}\nレスポンス内容: {response.text}"
        
        events = []
        for event in data:
            events.append({
                'startDateTime': event['startDateTime'],
                'title': event['title']
            })

        df = pd.DataFrame(events)
        return df.to_csv(index=False)
    else:
        return f"HTTPエラーコード: {response.status_code}\nレスポンス内容: {response.text}"

# スケジュールのフォーマット関数
def format_schedule(schedule_df):
    schedule_df['startDateTime'] = pd.to_datetime(schedule_df['startDateTime'])
    schedule_df = schedule_df.sort_values(by='startDateTime').reset_index(drop=True)
    formatted_schedule = ""
    current_date = None
    for idx, row in schedule_df.iterrows():
        date = row['startDateTime'].date()
        time = row['startDateTime'].time()
        if current_date != date:
            current_date = date
            formatted_schedule += f"{current_date.strftime('%Y-%m-%d')}\n"
        formatted_schedule += f"{row['startDateTime'].strftime('%H:%M')} - {row['title']}\n"
    return formatted_schedule

# メッセージコマンド
@bot.command(name='a')
async def timetable_a(ctx, date: str):
    print(f"Command received: !timetable {date}")
    try:
        target_date = datetime.strptime(date, '%Y-%m-%d')
        schedule = get_event_schedule_for_date(target_date, "クラスID")
        if isinstance(schedule, str):
            await ctx.send(f"```{schedule}```")
        else:
            formatted_schedule = format_schedule(pd.read_csv(io.StringIO(schedule)))
            print(f"Generated schedule: {formatted_schedule}")
            await ctx.send(f"```{formatted_schedule}```")
    except ValueError:
        print("Invalid date format.")
        await ctx.send("日付の形式が正しくありません。例: 2024-11-22")

@bot.command(name='b')
async def timetable_b(ctx, date: str):
    print(f"Command received: !timetable {date}")
    try:
        target_date = datetime.strptime(date, '%Y-%m-%d')
        schedule = get_event_schedule_for_date(target_date, "クラスID")
        if isinstance(schedule, str):
            await ctx.send(f"```{schedule}```")
        else:
            formatted_schedule = format_schedule(pd.read_csv(io.StringIO(schedule)))
            print(f"Generated schedule: {formatted_schedule}")
            await ctx.send(f"```{formatted_schedule}```")
    except ValueError:
        print("Invalid date format.")
        await ctx.send("日付の形式が正しくありません。例: 2024-11-22")

# Bot 実行
try:
    bot.run('discord bot token')
except discord.errors.LoginFailure as e:
    print(f"Invalid token: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
