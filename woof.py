import time, random, json, pathlib
import pyMastoChat
class woofer(pyMastoChat.chatbot):
    def __init__(self):
        self.bot_name = "woof"
        self.log_name = "woof-"+pyMastoChat.datetime() # whithout extension
        self.config_host = database()
        self.convers_host = database()
        self.initiation()
    def watching(self):
        self.log_host.timeStamp("Start: watch()")
        small_msg = "woof~"
        large_msg = "WOOF!!!!!! WOOF!!!!!!\n"
        ear_list = ["V{}V","▼{}▼","U{}U","◖{}◗","(V{})","(▼{})","(U{})","(◖{})","({}V)","({}▼)","({}U)","({}◗)"]
        face_list = [" ● ᴥ ● "," ・ ᴥ ・ "," ´ ꓃ ` "," ^ ｪ ^ "," ⚆ ᴥ ⚆ ","´• ﻌ •`"," ❍ᴥ❍ "]
        continue_bool = True
        count_int = 1

        record_host = pyMastoChat.database()
        record_host.target_path = "userData/woof-record.json"
        record_host.load()

        photo_host = pyMastoChat.database()
        photo_host.target_path = "userData/woof-photo.json"
        photo_host.load()
                
        content_dict = record_host.data.get("#content",dict())
        date_set = set(record_host.data.get("#time",list()))
        photo_time_set = set(record_host.data.get("#photoTime",list()))
        post_time_set = set(record_host.data.get("#postTime",list()))
        post_photo_set = set(record_host.data.get("#postPhoto",list()))
        photo_dict = photo_host.data.get("#photo",dict())

        while continue_bool:
            title_Str = pyMastoChat.datetime(output_str="yyyymmddhh")
            hour_int = int(pyMastoChat.datetime(output_str="H"))
            min_int = int(pyMastoChat.datetime(output_str="N"))
            if title_Str not in date_set and 10 > min_int:
                print("Period start:",count_int,end="\r")
                if hour_int >= 12:
                    woof_msg = large_msg
                    hour_int = hour_int - 12
                else:
                    woof_msg = ""
                while hour_int > 0:
                    hour_int = hour_int - 4
                    if hour_int > 0:
                        woof_msg = woof_msg + small_msg * 4 + "\n"
                    else:
                        woof_msg = woof_msg + small_msg * (4 + hour_int)
                magic_msg = ""
                if woof_msg == "":
                    if [ n for n in photo_dict.keys() if n not in post_photo_set ]:
                        woof_msg = random.choice(ear_list).format(random.choice(face_list))
                        target_hour_int = random.choice(range(1,24))
                        if len(str(target_hour_int)) == 1:
                            target_hour_str = "0"+ str(target_hour_int)
                        elif len(str(target_hour_int)) == 2:
                            target_hour_str = str(target_hour_int)
                        magic_msg = target_hour_str
                        photo_time_Set.update({ "{}{}".format(pyMastoChat.datetime(output_str="yyyymmdd"),target_hour_str) })
                    else:
                        woof_msg = random.choice(ear_list).format(" T ᴥ T ")
                        magic_msg = "!"
                if title_str in photo_time_Set and title_str not in post_time_set:
                    spoiler_msg = woof_msg
                    photo_list = [ n for n in photo_dict.keys() if n not in post_photo_set ]
                    target_photo = random.choice(photo_list)
                    final_msg = photo_dict[target_photo]["final_msg"]
                    file_str = photo_dict[target_photo]["file_str"]
                    media_toot = self.host.media_post(file_str)
                    pathlib.Path('userData/media-woof/photoID').mkdir(parents=True,exist_ok=True)
                    json_str = 'userData/media-woof/photoID/{id}.json'.format(id=media_toot.id)
                    with open(json_str,'w') as target_handle:
                        json.dump(media_toot, target_handle, indent=2)
                    post_toot = self.host.status_post(final_msg, media_ids=[media_toot.id], sensitive=True, visibility="public", spoiler_text=spoiler_msg)
                    post_photo_set.update({ target_photo })
                    post_time_set.update({ title_str })
                    date_set.update({ title_str })
                elif magic_msg == "!":
                    post_toot = self.host.status_post("Magic are finding their way today", visibility="public", spoiler_text=woof_msg)
                    date_set.update({ title_str })

                elif magic_msg != "" :
                    post_toot = self.host.status_post("Magic: {}".format(magic_msg), visibility="public", spoiler_text=woof_msg)
                    date_set.update({ title_str })

                else:
                    post_toot = self.host.status_post(woof_msg, visibility="public")
                    date_set.update({ title_str })
                record_set = set(content_dict.get(woof_msg,list()))
                record_set.update({ title_str })
                content_dict[woof_msg] = list(record_set)
                # self.logHost.record("  Reply: {}".format(post_toot.content))

                record_host.setIt("#content",content_dict)
                record_host.update_set("#time",date_set)
                record_host.update_set("#photoTime",photo_time_Set)
                record_host.update_set("#postTime",post_time_set)
                record_host.update_set("#postPhoto",post_photo_set)

                print(post_toot.content)

            pyMastoChat.countdown(60,"Period done:  {}".format(count_int))
            count_int = count_int + 1

if __name__ == "__main__":
    Bot = woofer()
    Bot.watching()
