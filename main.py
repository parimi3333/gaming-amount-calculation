import  pymongo
from datetime import datetime

def amount(x):
    if x <= 2:
        if x == 1:
            return 100
        else:
            return 200
    elif x <=4 :
        if x == 3:
            return 250
        else:
            return 250 + 90
    elif x >= 7 :
        y = x - 7
        return 390 + (85 * y if y > 0 else 0)
    elif x >= 9 :
        y = x - 9
        return 580 + (80 * y if y > 0 else 0)
    else:
        y = x - 10
        return 680 + (75 * y if y > 0 else 0)
connet = pymongo.MongoClient('mongodb://localhost:27017')
db = connet['gaming_hub']
col = db['gamer']

while True:
    output_list = []
    session = input("enter session : ")
    if session == "pause":
        mobile = int(input("mobile no : "))
        data = col.find({"mobile":mobile}).sort("_id", -1).limit(1)
        for i in data:
            output_list.append(i)
        if output_list[-1]["player_status"]=="open":
            up_end_list = []
            for i in output_list[-1]["time_duration"]:
                if i["end"] == "":
                    i['end'] = datetime.now()
                up_end_list.append(i)
            col.update_one({"mobile":mobile},{"$set":{"time_duration":up_end_list}})
    elif session == "resume":
        mobile = int(input("mobile no : "))
        data = col.find({"mobile": mobile})
        for i in data:
            output_list.append(i)
        if output_list[-1]["player_status"] == "open":
            result = col.update_one({"mobile": mobile}, {"$push": {"time_duration": {"start":datetime.now(),"end":""}}})
    elif session == "end":
        mobile = int(input("enter mobile no : "))
        data = col.find({"mobile": mobile}).sort([("_id",-1)]).limit(1)
        for i in data:
            output_list.append(i)
        if output_list[-1]["player_status"] == "open":
            dif = 0
            tl = []
            s = 0
            up_end_list = []
            for i in output_list[-1]["time_duration"]:
                for k,v in i.items():
                    if k == "start":
                        date1 = i[k]
                    if k == "end":
                        if v == '':
                            i['end'] = datetime.now()
                        up_end_list.append(i)
                        date2 = i[k] if i[k]!="" else datetime.now()
                        dif = date2 - date1
                        dif = (dif.total_seconds()/60)/60
                col.update_one({"_id": output_list[-1]['_id']}, {"$set": {"time_duration": up_end_list}})
                tl.append(dif)
        x = round(sum(tl))
        x = x if x > 0 else 1
        x = amount(x)
        result = col.update_one({"_id": output_list[-1]['_id']}, {"$set": {"amount": x, "player_status":"close"}})
        data = col.find({"mobile": mobile})
        for i in data:
            output_list.append(i)
        print(output_list[-1])
    elif session == "get":
        choice = input("enter choice : ")
        if choice == "mobile":
            mobile = int(input("enter mobile no : "))
            if mobile:
                result = col.find({"mobile":mobile})
        else:
            result = col.find({})
        for i in result:
            output_list.append(i)
        print(output_list)

    elif session == "new":
        mobile = int(input("mobile no : "))
        name = input("enter name : ")
        data = col.find_one({"mobile":mobile})
        output_list.append(data)
        if data == None:
            result = col.insert_one({"name":name,"mobile":mobile,"player_status":"open","time_duration": [{"start":datetime.now(),"end":""}]})
        elif output_list[-1]["player_status"] == "close":
            result = col.insert_one({"name": name, "mobile": mobile, "player_status": "open","time_duration": [{"start": datetime.now(), "end": ""}]})
