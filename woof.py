import time, random, json, pathlib
import tool, chatbot
class woofer(chatbot.chatbot):
    def __init__(self):
        self.botName = "woof"

        self.configHost = tool.database()
        self.logHost = tool.logging()
        self.conversHost = tool.database()

        self.initiation()

    def watching(self):
        self.logHost.record("Start: watch()")
        smallMsg = "woof~"
        largeMsg = "WOOF!!!!!! WOOF!!!!!!\n"
        earList = ["V{}V","▼{}▼","U{}U","◖{}◗","(V{})","(▼{})","(U{})","(◖{})","({}V)","({}▼)","({}U)","({}◗)"]
        faceList = [" ● ᴥ ● "," ・ ᴥ ・ "," ´ ꓃ ` "," ^ ｪ ^ "," ⚆ ᴥ ⚆ ","´• ﻌ •`"," ❍ᴥ❍ "]
        continueBool = True
        countInt = 1

        recordHost = tool.database()
        recordHost.targetPath = "userData/woof-record.json"
        recordHost.load()

        photoHost = tool.database()
        photoHost.targetPath = "userData/woof-photo.json"
        photoHost.load()
                
        contentDict = recordHost.data.get("#content",dict())
        dateSet = set(recordHost.data.get("#time",list()))
        photoTimeSet = set(recordHost.data.get("#photoTime",list()))
        postTimeSet = set(recordHost.data.get("#postTime",list()))
        postPhotoSet = set(recordHost.data.get("#postPhoto",list()))
        photoDict = photoHost.data.get("#photo",dict())

        while continueBool:
            titleStr = tool.datetime(outputStr="yyyymmddhh")
            hourInt = int(tool.datetime(outputStr="H"))
            minInt = int(tool.datetime(outputStr="N"))
            if titleStr not in dateSet and 10 > minInt:
                print("Period start:",countInt,end="\r")
                if hourInt >= 12:
                    woofMsg = largeMsg
                    hourInt = hourInt - 12
                else:
                    woofMsg = ""

                while hourInt > 0:
                    hourInt = hourInt - 4
                    if hourInt > 0:
                        woofMsg = woofMsg + smallMsg * 4 + "\n"
                    else:
                        woofMsg = woofMsg + smallMsg * (4+hourInt)

                magicMsg = ""
                if woofMsg == "":
                    if [ n for n in photoDict.keys() if n not in postPhotoSet ]:
                        woofMsg = random.choice(earList).format(random.choice(faceList))

                        targetHourInt = random.choice(range(1,24))
                        if len(str(targetHourInt)) == 1:
                            targetHourStr = "0"+ str(targetHourInt)
                        elif len(str(targetHourInt)) == 2:
                            targetHourStr = str(targetHourInt)

                        magicMsg = targetHourStr
                        photoTimeSet.update({ "{}{}".format(tool.datetime(outputStr="yyyymmdd"),targetHourStr) })
                    else:
                        woofMsg = random.choice(earList).format(" T ᴥ T ")
                        magicMsg = "!"

                if titleStr in photoTimeSet and titleStr not in postTimeSet:
                    spoilerMsg = woofMsg
                    photoList = [ n for n in photoDict.keys() if n not in postPhotoSet ]
                    targetPhoto = random.choice(photoList)
                    finalMsg = photoDict[targetPhoto]["finalMsg"]
                    fileStr = photoDict[targetPhoto]["fileStr"]
        
                    mediaToot = self.host.media_post(fileStr)
                    pathlib.Path('userData/media-woof/photoID').mkdir(parents=True,exist_ok=True)
                    jsonStr = 'userData/media-woof/photoID/{id}.json'.format(id=mediaToot.id)
                    with open(jsonStr,'w') as targetHandle:
                        json.dump(mediaToot, targetHandle, indent=2)

                    postToot = self.host.status_post(finalMsg, media_ids=[mediaToot.id], sensitive=True, visibility="public", spoiler_text=spoilerMsg)
                    postPhotoSet.update({ targetPhoto })
                    postTimeSet.update({ titleStr })
                    dateSet.update({ titleStr })

                elif magicMsg == "!":
                    postToot = self.host.status_post("Magic are finding their way today", visibility="public", spoiler_text=woofMsg)
                    dateSet.update({ titleStr })

                elif magicMsg != "" :
                    postToot = self.host.status_post("Magic: {}".format(magicMsg), visibility="public", spoiler_text=woofMsg)
                    dateSet.update({ titleStr })

                else:
                    postToot = self.host.status_post(woofMsg, visibility="public")
                    dateSet.update({ titleStr })

                recordSet = set(contentDict.get(woofMsg,list()))
                recordSet.update({ titleStr })
                contentDict[woofMsg] = list(recordSet)
                # self.logHost.record("  Reply: {}".format(postToot.content))

                recordHost.setIt("#content",contentDict)
                recordHost.updateSet("#time",dateSet)
                recordHost.updateSet("#photoTime",photoTimeSet)
                recordHost.updateSet("#postTime",postTimeSet)
                recordHost.updateSet("#postPhoto",postPhotoSet)

                print(postToot.content)

            tool.countdown(60,"Period done:  {}".format(countInt))
            countInt = countInt + 1

if __name__ == "__main__":
    Bot = woofer()
    Bot.watching()
