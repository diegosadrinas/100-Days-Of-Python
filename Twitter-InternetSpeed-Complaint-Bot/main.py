from TwitterBotClasses import InternetSpeedTwitterBot

tw_bot = InternetSpeedTwitterBot()
get_internet_speed = tw_bot.get_internet_speed()
print(f"Current speed: {get_internet_speed}, ISP speed: {tw_bot.speed_up}")
if get_internet_speed < (tw_bot.speed_up - 20):
    tw_bot.tweet_internet_company()



