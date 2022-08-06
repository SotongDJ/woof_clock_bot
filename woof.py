import time, random, json, pathlib
from pyMastoChat import bot
class woofer(bot.chatbot):
    def __init__(self):
        self.bot_name = "woof"
        self.log_name = "woof-"+bot.datetime(output_str="yyyymmdd") # whithout extension
        self.config_host = bot.database()
        self.convers_host = bot.database()
        self.initiation()
    def watching(self):
        self.log_host.timeStamp("Start: watch()")
        small_msg = "woof~"
        large_msg = "WOOF!!!!!! WOOF!!!!!!\n"
        ear_list = ["V{}V","▼{}▼","U{}U","◖{}◗","(V{})","(▼{})","(U{})","(◖{})","({}V)","({}▼)","({}U)","({}◗)"]
        face_list = [" ● ᴥ ● "," ・ ᴥ ・ "," ´ ꓃ ` "," ^ ｪ ^ "," ⚆ ᴥ ⚆ ","´• ﻌ •`"," ❍ᴥ❍ "]
        continue_bool = True
        count_int = 1

        record_host = bot.database()
        record_host.target_path = "userData/woof-record.json"
        record_host.load()

        photo_host = bot.database()
        photo_host.target_path = "userData/woof-photo.json"
        photo_host.load()
                
        content_dict = record_host.data.get("#content",dict())
        queue_dict = record_host.data.get("#queue",dict())
        posted_dict = record_host.data.get("#posted",dict())
        posted_photo_set = set(record_host.data.get("#posted_photo",list()))

        photo_dict = photo_host.data.get("#photo",dict())
        host_day_str = bot.datetime(output_str="yyyymmdd") 
        while continue_bool:
            today_str = bot.datetime(output_str="yyyymmdd")
            if host_day_str != today_str:
                self.log_name = "woof-"+bot.datetime(output_str="yyyymmdd")
                self.reinitiation()
                host_day_str = today_str
            current_time_str = bot.datetime(output_str="yyyymmddhh")
            hour_int = int(bot.datetime(output_str="H"))
            min_int = int(bot.datetime(output_str="N"))
            run_hour_int = hour_int
            if current_time_str not in posted_dict.keys() and 5 > min_int:
                # print("Period start:",count_int,end="\r")
                emoji_msg = ""
                if hour_int == 0:
                    woof_msg = F"[12AM midnight]\n"
                elif hour_int == 12:
                    run_hour_int = run_hour_int - 12
                    woof_msg = F"[12PM noon]\n{large_msg}"
                elif hour_int > 12:
                    run_hour_int = hour_int - 12
                    woof_msg = F"[{run_hour_int}PM]\n{large_msg}"
                else:
                    woof_msg = F"[{hour_int}AM]\n"
                while run_hour_int > 0:
                    run_hour_int = run_hour_int - 4
                    if run_hour_int > 0:
                        woof_msg = woof_msg + small_msg * 4 + "\n"
                    else:
                        woof_msg = woof_msg + small_msg * (4 + run_hour_int)
                if queue_dict.get(today_str,"") == str(hour_int):
                    photo_list = [ n for n in photo_dict.keys() if n not in posted_photo_set ]
                    if len(photo_list) > 0:
                        target_photo = random.choice(photo_list)
                        final_msg = photo_dict[target_photo]["final_msg"]
                        file_str = photo_dict[target_photo]["file_str"]
                        media_toot = self.host.media_post(file_str)
                        pathlib.Path('userData/media-woof/photoID').mkdir(parents=True,exist_ok=True)
                        json_str = 'userData/media-woof/photoID/{}.json'.format(media_toot.id)
                        with open(json_str,'w') as target_handle:
                            json.dump(media_toot, target_handle, indent=2)
                        spoiler_msg = self.contentPurifier(woof_msg)
                        post_toot = self.host.status_post(final_msg, media_ids=[media_toot.id], sensitive=True, visibility="public", spoiler_text=spoiler_msg)
                        posted_photo_set.update({ target_photo })
                        posted_dict.update({ current_time_str : post_toot.id })
                    else:
                        emoji_msg = random.choice(ear_list).format(random.choice(face_list))
                        woof_msg = woof_msg + "\n#woofwoofhappy"
                        post_toot = self.host.status_post(woof_msg, visibility="public", spoiler_text=emoji_msg)
                        posted_dict.update({ current_time_str : post_toot.id })
                elif today_str not in queue_dict.keys() and hour_int != 23:
                    begin_int = hour_int if hour_int > 8 else 8
                    magic_msg = str(random.choice(range(begin_int,23)))
                    queue_dict[today_str] = magic_msg
                    post_toot = self.host.status_post(woof_msg+F"\nMagic number: {magic_msg}", visibility="public", spoiler_text="Magic are finding their way today! Woof!")
                    posted_dict.update({ current_time_str : post_toot.id })
                else:
                    post_toot = self.host.status_post(woof_msg, visibility="public")
                    posted_dict.update({ current_time_str : post_toot.id })
                record_set = set(content_dict.get(woof_msg,list()))
                record_set.update({ current_time_str })
                content_dict[woof_msg] = list(record_set)
                # self.logHost.record("  Reply: {}".format(post_toot.content))
                record_host.setIt("#content",content_dict)
                record_host.setIt("#queue",queue_dict)
                record_host.setIt("#posted",posted_dict)
                record_host.updateSet("#posted_photo",posted_photo_set)

                self.log_host.timeStamp(post_toot.content)

            second_int = 60
            self.countdown(second_int,F"Period done, current batch: {count_int}, {second_int} sec per batch")
            count_int = count_int + 1
    def exit_now(self, *args):
        self.exit_key = True
if __name__ == "__main__":
    Bot = woofer()
    Bot.watching()
