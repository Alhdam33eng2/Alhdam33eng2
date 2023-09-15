import telebot, os, requests, json , re, asyncio
from datetime import datetime, timedelta
from time import sleep 
import pyrogram
from pyrogram import enums
from pyrogram import Client , filters, compose
from pyrogram.handlers import MessageHandler
from pyrogram.types import InlineKeyboardMarkup as Mk , InlineKeyboardButton as btn, InlineQueryResultPhoto, InlineQueryResultCachedPhoto, InlineQueryResultCachedVideo
from pyrogram.types import WebAppInfo as wb
from pyrogram.types import (InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardMarkup, InlineKeyboardButton)
from kvsqlite.sync import Client as Database
from rich import print_json
from rich.traceback import install  # اظهار الخطأ بشكل منسق
install()
#import uvloop
from pyrogram.errors.exceptions.bad_request_400 import PasswordHashInvalid,PhoneCodeInvalid, ApiIdInvalid, PhoneCodeExpired
from pyrogram.errors.exceptions.not_acceptable_406 import PhoneNumberInvalid
import traceback
from pyrogram.errors import FloodWait
import random
import sys,time, os
from PIL import Image, ImageDraw, ImageFont
import textwrap
from pyrogram.types import ChatPermissions
print ()

#print (dir(enums.ChatMemberStatus.OWNER.OWNER))

#print (dir(enums.chat_member_status))



Restriction = ChatPermissions(
    can_send_messages=False,
    can_send_media_messages=False,
    can_send_other_messages=False,
    can_send_polls=False,
    can_add_web_page_previews=False,
    can_change_info=False,
    can_invite_users=False, 
    can_pin_messages=False 
)

Un_Restriction = ChatPermissions(
    can_send_messages=True ,
    can_send_media_messages=True,
    can_send_other_messages=True,
    can_send_polls=True,
    can_add_web_page_previews=True,
    can_change_info=True,
    can_invite_users=True, 
    can_pin_messages=True 
)

db = Database ('CAPTCH.sqlite')

if str(db.get ("db")) == "None" :
	data = {"111111": { "Owner": "222222" ,"CAPTCHA": {} , "Real_Acc": {}}}
	db.set ("db", data)
#if str(db.get ("bot")) == "None" :

data = {"Status_Bot": True, "Type_Captcha": "CAPTCHA_Emoj" ,"CAPTCHA": {} , "Real_Acc": {}, "members": {}}
db.set ("bot", data)

print_json (data=db.get("db"))
print_json (data=db.get("bot"))

api_id1 = 25230816
api_hash1 = "671a0b830f1dd8fc8f685886613baefc"
TOKEN = "6314885962:AAFhxIml92c6k24mIEj84HEtx4SBz3BXxZM"
bot = Client ("iii5bot",  api_id=api_id1, api_hash=api_hash1, bot_token=TOKEN )

Numbers = ["1","2","3","4","5","6","7","8","9","10", "11", "12"]
Numbers2 = ["1","2","3","4","5","6" ,"7","8","9"]
#Emoji = {"1": '😀',"2": '😃',"3": '😄',"4": '😁',"5": '😆',"6": '😅',"7": '🤣',"8": '😂',"9": '🙂',"10": '🙃',"11": '😉',"12": '😊',"13": '😇',"14": '🥰',"15": '😍',"16": '🤩',"17": '😗',"18": '😘',"19": '🐵',"20": '🐒',"21": '🦍',"22": '🦧',"23": '🐶',"24": '🐮',"25": '🐼',"26": '🐰',"27": '🐬',"28": '🍖',"29": '🎉',"30": '🎯',"31": '🎁',"32": '🎀',"33": '🎳',"34": '💍',"35": '👑',"36": '💎',"37": '💄',"38": '☎'}
#print_json (data=Emoji)
Emoji = ["🍨", "🍦", "🥦", "🍇", "🍿", "🌚", "🎱", "🎁","💼", "☎️", "📹", "🎉", "🗽", "🦁", "⏳️", "💻","🧳", "🚀"]



async def check_join(id):
	#قراءة الملف
	read_file = db.get ("bot")
	ids_members_bot = read_file["members"]
	if id in ids_members_bot :
		result=True
	else:
		result=False
	
	return result
	



async def Commands_Admin(group_id) :
	data = db.get ("db")
	
	text_comnds  = "- الاوامر"
	Status_Bot = "✅️" if data[group_id]["Status_Bot"] == True else "❌️"
	Status_emoji = "✅️" if data[group_id]["Type_Captcha"] ==  "CAPTCHA_Emoj" else "❌️"
	Status_number = "✅️" if Status_emoji == "❌️" else "❌️"
	Status_DelMssgBot = "✅️" if data[group_id]["Delete_Messg_Bot"] == True else "❌️"
	Mark_comnds = Mk ([
	[btn (f"عمل البوت : {Status_Bot}", callback_data="Status_Bot")],
	[btn ("تحقق من خلال :", callback_data="*&*")],
	[btn (f"الارقام: {Status_number}" , callback_data="NumberTrue"), btn (f"الايموجي: {Status_emoji}" , callback_data="EmojiTrue")],
	[btn (f"حذف رسائل البوت: {Status_DelMssgBot}", callback_data="Delete_Messg_Bot")]
	])
	return text_comnds , Mark_comnds
	
	
	




@bot.on_message (filters.private & filters.command(["start"]))
async def Start_bot (bot, message) :
	print("filters.private & filters.command(['start']) ......")
	#رسالة في خاص البوت
	Bot_username = "iii5bot"
	owner_id  = "1009015069"
	
	#print(message)
	dataBot = db.get ("bot")
	#فحص البوت يعمل او لااا
	if dataBot["Status_Bot"] == False :
		#اذا كان البوت متوقف
		text_stop = "**● عذراً ، تم ايقاف البوت لأغراض الصيانة . \n~ سيتم الأعادة للعمل في اقرب وقت ✅️ .**"
		await bot.send_message (id, text_stop, parse_mode=enums.ParseMode.MARKDOWN)
	
	else:
		#اذا كان البوت يعمل
		id = str (message.from_user.id)
		user = str (message.from_user.username)
		name = str (message.from_user.first_name)
		#فحص اذا مستخدم  جديد راح يدز للادمن مستخدم جديد
		if await check_join(id) == False  :
			# اضافة الايدي الى مستخدمين البوت
			dataBot["members"][id] = {"username": str(user), "url_share": 0}
			db.set ("bot", dataBot)
			#معرفة العدد الكلي لمستخدمين البوت
			numb= len(dataBot["members"])
					
			Mark = Mk([ [btn(text="فتح المحادثة" ,url=f"tg://openmessage?user_id={id}")] ])
			await bot.send_message(owner_id , text=f"""**⌯ New member login to your bot:
⌯⌯⌯⌯⌯⌯⌯⌯⌯⌯⌯⌯⌯⌯⌯⌯⌯⌯⌯⌯⌯⌯⌯⌯
NAME : {name}
USER : `@{user}`
iD : `{id}`
⌯⌯⌯⌯⌯⌯⌯⌯⌯⌯⌯⌯⌯⌯⌯⌯⌯⌯⌯⌯⌯⌯⌯⌯
⌯ Total Members : {numb} **""", parse_mode=enums.ParseMode.MARKDOWN, disable_web_page_preview=True, reply_markup=Mark)
			
		
		
		if id not in dataBot["Real_Acc"]  :
			await message.reply_text (text="**- مرحباً بك ، للمتابعة نتأكد أولاً من انك لست روبوتاً 🤖 **", parse_mode=enums.ParseMode.MARKDOWN, quote=True,
																reply_markup=Mk([[btn("تحقق الآن", callback_data=dataBot["Type_Captcha"])]]))
		else:
			await message.reply_text (text="**- مرحباً بك في بوت التحقق CAPTCHA **", parse_mode=enums.ParseMode.MARKDOWN, quote=True,
																reply_markup=Mk([ [btn(text="فتح المحادثة" ,url=f"tg://openmessage?user_id={id}")] ]))
	
	


@bot.on_message (filters.new_chat_members)
async def Start (bot, message) :
	print("filters.new_chat_members ......")
	
	Bot_username = "iii5bot"
	owner_id  = "1009015069"
	
	#print(message)
	data = db.get ("db")
	if data[str(message.chat.id)]["Status_Bot"] == True :
		for uid in message.new_chat_members :
			id = str(uid.id)
			user = str(uid.username)
			if not uid.is_bot and  id not in data[str(message.chat.id)]["Real_Acc"]  :
				#استخراج الوقت بعد مده من الزمن المحدد
				ban_end_time = datetime.now() + timedelta(seconds=2)
				#تقييد المستخدم وارسل رسالة طلب التحقق
				await message.chat.restrict_member (user_id=id, permissions=Restriction ,until_date= ban_end_time)
				await message.reply_text (text="**- مرحباً بك ، للمتابعة تأكد أولاً من انك لست روبوتاً 🤖 **", parse_mode=enums.ParseMode.MARKDOWN, quote=True,
																	reply_markup=Mk([[btn("تحقق الآن", callback_data=data[str(message.chat.id)]["Type_Captcha"])]]))


		







@bot.on_callback_query ()
async def callback (bot, call):
	print (call.data)
	id = str (call.from_user.id)
	user = str(call.from_user.username)
	
	if call.message.chat.title :
		group_id = str(call.message.chat.id)
		if "CPTCH_" in call.data :
			data =db.get ("db")
			group_id = str(call.message.chat.id)
			if id in data[group_id]["CAPTCHA"] and str(call.message.reply_to_message_id) == data[group_id]["CAPTCHA"][id]["message_id"] :
				New_Btn = []
				for uid in call.message.reply_markup.inline_keyboard:
					#قائمة للسطر الاول
					list_btn = []
					for sid in uid:
						#اذا كان هذا الز يساوي الزر الذي تم الضغط عليه
						if sid.callback_data == call.data :
							#ضع صح مكانه
							list_btn.append (btn("✅️", callback_data="True"))
						else:
							#اذا كان لااا ، اعد اضافته نفسه
							list_btn.append (btn(sid.text , callback_data=sid.callback_data))
					#اضافة هذا السطر الى القائمة الرئيسية
					New_Btn.append (list_btn)
				
				#تعديل الازرار فقط
				await call.message.edit_reply_markup (Mk(New_Btn))
				
				data[group_id]["CAPTCHA"][id]["input_code"].append (call.data.split ("CPTCH_")[1])
				input_code = data[group_id]["CAPTCHA"][id]["input_code"]
				print (f"input_code : {input_code}")
				db.set ("db", data)
				if len(input_code) >= len (data[group_id]["CAPTCHA"][id]["Code"]) :
					Code_id = data[group_id]["CAPTCHA"][id]["Code"]
					print (sorted(data[group_id]["CAPTCHA"][id]["input_code"]))
					print (sorted (Code_id))
					if sorted(Code_id) == sorted(data[group_id]["CAPTCHA"][id]["input_code"]) :
						await call.message.delete ()
						await call.message.chat.restrict_member (user_id=id, permissions=Un_Restriction)
						await call.message.reply_text(text="- شـڪراً لك، انته لست روبوت، يمكنك استخدام المجموعة 🎉✨️",reply_to_message_id=call.message.reply_to_message_id , parse_mode=enums.ParseMode.MARKDOWN, quote=True)
						if id != "6037245969":
							data[group_id]["Real_Acc"][id] = {"username": user}
							del data[group_id]["CAPTCHA"][id]
							db.set ("db", data)
	    				
					else:
						bot_user = (await bot.get_me()).username
						await call.message.delete ()
						await call.message.reply_text(text="**- لم يتم اثبات هويتك❌️ ، أعد المحاولة.**" ,reply_to_message_id=call.message.reply_to_message_id , parse_mode=enums.ParseMode.MARKDOWN, quote=True, 
	    																			reply_markup=Mk([[btn("تحقق الآن", callback_data=data[group_id]["Type_Captcha"])]]))
	    				
						del data[group_id]["CAPTCHA"][id]
						db.set ("db", data)
	    	
		
		
		elif call.data == "CAPTCHA_Number" :
			#اذا تم الضغط على زر التحقق وكان موجود في كابتشا سيتم اعادة انشاء له التحقق مره ثانية
			
			data = db.get ("db")
			group_id = str(call.message.chat.id)
			if id in data[group_id]["CAPTCHA"] :
				del data[group_id]["CAPTCHA"][id]
				db.set ("db", data)
			
			if id not in data[group_id]["Real_Acc"] :
				List_Code_cap = []
				random.shuffle(Numbers2)
				for Cap in Numbers2[:5] :
					List_Code_cap.append (Cap)
				
				print (List_Code_cap)
				data =db.get ("db")
				data[group_id]["CAPTCHA"][id]= {"username": user, "Code": List_Code_cap , "input_code": [] , "message_id": str(call.message.reply_to_message_id) }
				db.set ("db", data)
				
				
				img = Image.open("page5.jpg")
				draw = ImageDraw.Draw(img)
				fnt = "text_to_handwriting/resources/fonts/karate.ttf"
				#حجم الخط
				font = ImageFont.truetype(fnt, 117)
				# x : هي بداية النص من الاعلى
				x = [300, 270, 320, 280,305]
				#sp هي مسافة اول حرف عن بداية السطر
				sp = 135
				for numb ,line in enumerate (List_Code_cap , start=0) :
				   #ال 120 هي جعل النص في وسط الصفحه ،
				   #لجعل النص في بادية الصفحه  القيمةهي 45
				    draw.text((sp, x[numb]) ,line , font=font, fill="#101e75")
				    sp += 100
				    print (line)
				img.save(f"{id}.png", "png")
				
				ButtonCap = []
				for sid in List_Code_cap :
					ButtonCap.append (btn (sid, callback_data=f"CPTCH_{sid}"))
				
				for uid in Numbers :
					if uid not in List_Code_cap :
						ButtonCap.append (btn (uid, callback_data=f"CPTCH_{uid}"))
				
				random.shuffle(ButtonCap)
				MarkCap = []
				for i in range(0, len(ButtonCap), 4):
					MarkCap.append (ButtonCap[i:i+4])
				
				await call.message.delete ()
				await call.message.reply_photo (photo=f"{id}.png", caption="**- اكتب الرمز الذي في الصوره من خلال الازرار :**", quote=True , reply_to_message_id=call.message.reply_to_message_id  ,parse_mode=enums.ParseMode.MARKDOWN, reply_markup=Mk(MarkCap))
		
		
		
		
		
		elif call.data == "CAPTCHA_Emoj" :
			data = db.get ("db")
			group_id = str(call.message.chat.id)
			#print (call)
			if id not in data[group_id]["Real_Acc"] :
				data = db.get ("db")
				lst_key = list (data["Files"])
				random.shuffle(lst_key)
				
				dict_Code = data["Files"][random.choice(lst_key)]
				List_Code_cap = dict_Code["Code"]
				print (List_Code_cap)
				
				data =db.get ("db")
				data[str(call.message.chat.id)]["CAPTCHA"][id]= {"username": user, "Code": List_Code_cap , "input_code": [] , "message_id": str(call.message.reply_to_message_id) }
				db.set ("db", data)
				
				ButtonCap = []
				for sid in List_Code_cap :
					ButtonCap.append (btn (sid, callback_data=f"CPTCH_{sid}"))
				
				random.shuffle(Emoji)
				for uid in Emoji :
					if uid.replace('\uFE0F', '') not in List_Code_cap :
						ButtonCap.append (btn (uid, callback_data=f"CPTCH_{uid}"))
						if len(ButtonCap) == 12 :
							break 
							
				random.shuffle(ButtonCap)
				MarkCap = []
				for i in range(0, len(ButtonCap), 4):
					MarkCap.append (ButtonCap[i:i+4])
				
				await call.message.delete ()
				await call.message.reply_photo (photo=dict_Code["File_id"] , caption="**- اكتب الرمز الذي في الصوره من خلال الازرار :**", quote=True , reply_to_message_id=call.message.reply_to_message_id  ,parse_mode=enums.ParseMode.MARKDOWN, reply_markup=Mk(MarkCap))
				print (call.message.id)
		
	
	
		data =db.get ("db")
		if call.data == "NumberTrue" :
			if id == data[group_id]["Owner"] :
				
				group_idd = str(call.message.chat.id)
				if data[group_idd]["Type_Captcha"] == "CAPTCHA_Number" :
					#اظهار رسالة منبثقة
					await bot.answer_callback_query (call.id,  "- هذا الامر مُفعل مسبقاً️", show_alert=True)
				else:
					data[group_idd]["Type_Captcha"] = "CAPTCHA_Number"
					db.set ("db", data)
					
					text_comnds , Mark_comnds = await Commands_Admin(group_idd)
					await bot.answer_callback_query (call.id, "- تم تفعيل التحقق من خلال الارقام ✅️.", show_alert=True)
					#تعديل الازرار فقط
					await call.message.edit_reply_markup (Mark_comnds)
			
			else:
				await bot.answer_callback_query (call.id, "- هذا الامر خاص في المالك فقط️", show_alert=True)
				
								
		
			
					
		elif call.data == "EmojiTrue" :
			if id == data[group_id]["Owner"] :
				group_idd = str(call.message.chat.id)
				if data[group_idd]["Type_Captcha"] ==  "CAPTCHA_Emoj" :
					#اظهار رسالة منبثقة
					await bot.answer_callback_query (call.id, "- هذا الامر مُفعل مسبقاً️", show_alert=True)
				else:
					data[group_idd]["Type_Captcha"] =  "CAPTCHA_Emoj"
					db.set ("db", data)
					
					text_comnds , Mark_comnds = await Commands_Admin(group_idd)
					await bot.answer_callback_query (call.id, "- تم تفعيل التحقق من خلال الايموجي ✅️.", show_alert=True)
					#تعديل الازرار فقط
					await call.message.edit_reply_markup (Mark_comnds)
			
			else:
				await bot.answer_callback_query (call.id, "- هذا الامر خاص في المالك فقط️", show_alert=True)
				
			
			
		elif call.data == "Delete_Messg_Bot" :
			if id == data[group_id]["Owner"] :
				if data[group_id]["Delete_Messg_Bot"] == False :
					data[group_id]["Delete_Messg_Bot"]= True
					db.set ("db", data)
					
					text_comnds , Mark_comnds = await Commands_Admin(group_id)
					await bot.answer_callback_query (call.id, "- تم تفعيل حذف رسائل البوت تلقائياً بعد 2 دقيقه من ارسالها ✅️.", show_alert=True)
					#تعديل الازرار فقط
					await call.message.edit_reply_markup (Mark_comnds)
				
				else:
					data[group_id]["Delete_Messg_Bot"]= False 
					db.set ("db", data)
					
					text_comnds , Mark_comnds = await Commands_Admin(group_id)
					await bot.answer_callback_query (call.id, "- تم تعطيل حذف رسائل البوت تلقائياً بنجاح.", show_alert=True)
					#تعديل الازرار فقط
					await call.message.edit_reply_markup (Mark_comnds)
			
			else:
				await bot.answer_callback_query (call.id, "- هذا الامر خاص في المالك فقط️", show_alert=True)
				
	
		elif call.data == "Status_Bot" :
			if id == data[group_id]["Owner"] :
				if data[group_id]["Status_Bot"] == True :
					data[group_id]["Status_Bot"] = False
					db.set ("db", data)
					
					text_comnds , Mark_comnds = await Commands_Admin(group_id)
					await bot.answer_callback_query (call.id, "- تم تعطيل عمل البوت", show_alert=True)
					#تعديل الازرار فقط
					await call.message.edit_reply_markup (Mark_comnds)
					
				else:
					data[group_id]["Status_Bot"] = True 
					db.set ("db", data)
					
					text_comnds , Mark_comnds = await Commands_Admin(group_id)
					await bot.answer_callback_query (call.id, "- تم تشغيل بوت التحقق بنجاح ✅️", show_alert=True)
					#تعديل الازرار فقط
					await call.message.edit_reply_markup (Mark_comnds)
						
			else:
				await bot.answer_callback_query (call.id, "- هذا الامر خاص في المالك فقط️", show_alert=True)
		
		
		
		if call.message.id not in data[group_id]["Delete_Messages"] :
			#اضافة ايدي
			data[group_id]["Delete_Messages"].append (call.message.id)
			db.set ("db", data)
				
	
	else:
		if "CPTCH_" in call.data :
			Botdata =db.get ("bot")
			
			if id in Botdata["CAPTCHA"] :
				New_Btn = []
				for uid in call.message.reply_markup.inline_keyboard:
					#قائمة للسطر الاول
					list_btn = []
					for sid in uid:
						#اذا كان هذا الز يساوي الزر الذي تم الضغط عليه
						if sid.callback_data == call.data :
							#ضع صح مكانه
							list_btn.append (btn("✅️", callback_data="True"))
						else:
							#اذا كان لااا ، اعد اضافته نفسه
							list_btn.append (btn(sid.text , callback_data=sid.callback_data))
					#اضافة هذا السطر الى القائمة الرئيسية
					New_Btn.append (list_btn)
				
				#تعديل الازرار فقط
				await call.message.edit_reply_markup (Mk(New_Btn))
				
				Botdata["CAPTCHA"][id]["input_code"].append (call.data.split ("CPTCH_")[1])
				input_code = Botdata["CAPTCHA"][id]["input_code"]
				print (f"input_code : {input_code}")
				db.set ("bot", Botdata)
				if len(input_code) >= len (Botdata["CAPTCHA"][id]["Code"]) :
					Code_id = Botdata["CAPTCHA"][id]["Code"]
					print (sorted(Botdata["CAPTCHA"][id]["input_code"]))
					print (sorted (Code_id))
					if sorted(Code_id) == sorted(Botdata["CAPTCHA"][id]["input_code"]) :
						await call.message.delete ()
						await call.message.reply_text(text="- شـڪراً لك، انته لست روبوت، يمكنك استخدام البوت 🎉✨️",reply_to_message_id=call.message.reply_to_message_id , parse_mode=enums.ParseMode.MARKDOWN, quote=True)
						if id != "6037245969":
							Botdata["Real_Acc"][id] = {"username": user}
							del Botdata["CAPTCHA"][id]
							db.set ("bot", Botdata)
	    				
					else:
						bot_user = (await bot.get_me()).username
						await call.message.delete ()
						await call.message.reply_text(text="**- لم يتم اثبات هويتك❌️ ، أعد المحاولة.**" ,reply_to_message_id=call.message.reply_to_message_id , parse_mode=enums.ParseMode.MARKDOWN, quote=True, 
	    																			reply_markup=Mk([[btn("تحقق الآن", callback_data=data[group_id]["Type_Captcha"])]]))
	    				
						del Botdata["CAPTCHA"][id]
						db.set ("bot", Botdata)
	    	
		
		
		
		elif call.data == "CAPTCHA_Emoj" :
			#خاص في البوت
			Botdata = db.get ("bot")
			data = db.get ("db")
			if id not in Botdata["Real_Acc"] :
				lst_key = list (data["Files"])
				random.shuffle(lst_key)
				
				dict_Code = data["Files"][random.choice(lst_key)]
				List_Code_cap = dict_Code["Code"]
				print (List_Code_cap)
				
				Botdata["CAPTCHA"][id]= {"username": user, "Code": List_Code_cap , "input_code": []}
				db.set ("bot", Botdata)
				
				ButtonCap = []
				for sid in List_Code_cap :
					ButtonCap.append (btn (sid, callback_data=f"CPTCH_{sid}"))
				
				random.shuffle(Emoji)
				for uid in Emoji :
					if uid.replace('\uFE0F', '') not in List_Code_cap :
						ButtonCap.append (btn (uid, callback_data=f"CPTCH_{uid}"))
						if len(ButtonCap) == 12 :
							break 
							
				random.shuffle(ButtonCap)
				MarkCap = []
				for i in range(0, len(ButtonCap), 4):
					MarkCap.append (ButtonCap[i:i+4])
				
				await call.message.delete ()
				await call.message.reply_photo (photo=dict_Code["File_id"] , caption="**- اكتب الرمز الذي في الصوره من خلال الازرار :**", quote=True , reply_to_message_id=call.message.reply_to_message_id  ,parse_mode=enums.ParseMode.MARKDOWN, reply_markup=Mk(MarkCap))
				
		
	
	
		
		





@bot.on_message  (filters.regex (".الاوامر") | filters.regex (".comments") & filters.group)
async def message_group (bot, message):
	data = db.get ("db")
	id = str(message.from_user.id)
	group_id = str (message.chat.id )
	#اذا كان مالك المجموعة
	if id == data[group_id]["Owner"] :
		print("@bot.on_message  (filters.regex (.الاوامر) | filters.regex (.comments) & filters.group)")
		
		text_comnds , Mark_comnds = await Commands_Admin(group_id)
		await message.reply_text (text=text_comnds , quote=True , parse_mode=enums.ParseMode.MARKDOWN , reply_markup=Mark_comnds)
		#حذف الرسائل التي تم اضافتها في الحذف التلقائي بدون تحديد وقت
		if data[group_id]["Delete_Messages"] != [] :
			list_message_ids = data[group_id]["Delete_Messages"]
			await bot.delete_messages(message.chat.id, list_message_ids)
			data[group_id]["Delete_Messages"] =[]
			db.set ("db", data)
			print ("- Delete Messages .....")
			
	
	else:
		await message.reply_text (text="**- هذا الامر خاص في المالك فقط .**" , quote=True , parse_mode=enums.ParseMode.MARKDOWN)
	
		






@bot.on_chat_member_updated ()
async def in_group (bot,message):
	print ("@bot.on_chat_member_updated ()")
	data = db.get ("db")
	print (message)
	if message.new_chat_member :
		#print (message)
		group_id = str (message.chat.id)
	
		#if message.new_chat_member.user.is_self and str(message.new_chat_member.status) == "ChatMemberStatus.BANNED" :
			#del data[str(message.chat.id)]
			#db.set ("db", data)
			#print_json (data=data)
	
		if message.new_chat_member.user.is_self and str(message.new_chat_member.status) == "ChatMemberStatus.ADMINISTRATOR" :
			print ("- Add Bot Admin ...... ")
			async for member in bot.get_chat_members(message.chat.id):
				if str(member.status) == "ChatMemberStatus.OWNER" :
					print ("ChatMemberStatus.OWNER....")
					data[group_id]=  {"Owner": str(member.user.id) , "Status_Bot": True ,"Type_Captcha": "CAPTCHA_Emoj", "Delete_Messg_Bot": False, "Delete_Messages": [] , "CAPTCHA": {} , "Real_Acc": {}}
					db.set ("db", data)
					await bot.send_message (chat_id=message.chat.id, text="**- تم تفعيل البوت بنجاح ✅️.**" )
					data[group_id]["Delete_Messages"] =[]
					db.set ("db", data)
					print (data)
					break
		
		
		
		elif message.new_chat_member.user.is_self and str(message.new_chat_member.status) == "ChatMemberStatus.MEMBER" :
			print ("- Add Bot member ...... ")
			owner_id  = "1009015069"
			group_id = str(message.chat.id)
			group_name = message.chat.title
			group_user = str(message.chat.username)
			group_invited = message.new_chat_member.joined_date
			members_count = await bot.get_chat_members_count(group_id)
			
			text_to_owner = f"""**
⌯ تم اضافة البوت الى مجموعة جديدة :

⧆↫اسم المجموعة : {group_name}
⧆↫معرف المجموعة : {group_user}
⧆↫ايدي المجموعة : {group_id}
⧆↫عدد الاعضاء : {members_count}
⧆↫تاريخ الانضمام : 
{group_invited}
**"""	
			await bot.send_message (chat_id=owner_id, text=text_to_owner )
			
			await bot.send_message (chat_id=message.chat.id, text="**- اضف البوت ادمن لكي يتم تفعيل البوت ✅️.**" )
		
		
		






@bot.on_message  (filters.text & filters.group)
async def message_text (bot, message ):
	print ("@bot.on_message  (filters.text & filters.group)")
	data = db.get ("db")
	group_id = str (message.chat.id)
	print (message.text)
	#print ("اضف البوت ادمن لكي"  in message.text)
	
	if data[group_id]["Delete_Messages"] != [] :
		list_message_ids = data[group_id]["Delete_Messages"]
		await bot.delete_messages(message.chat.id, list_message_ids)
		data[group_id]["Delete_Messages"] =[]
		db.set ("db", data)
		print ("- Delete Message .....")

	if data[group_id]["Delete_Messg_Bot"] == True:
		for uid in await bot.get_messages(message.chat.id, [ i for i in range(message.id-20 , message.id)]) :
			#اذا كانت الرسالة لم يتم حذفها
			#print (uid)
			if uid.empty == None and uid.outgoing :
				if "شـڪراً لك،" not in uid.text:
					print (f">>>>>>> {uid.id}   {uid.text} <<<<<<" )
					#اذا كانت الرسالة من هذا البوت وكان الوقت الان اكبر من وقت الرسالة بعد اضافة 2 دقيقة على وقت ارسالها
					if  datetime.now() >= (datetime.strptime(str(uid.date) , "%Y-%m-%d %H:%M:%S") + timedelta(minutes=int(2))) :
						await bot.delete_messages(message.chat.id, uid.id)
						print ("- Delete Message Bot.....")
	








#عند مغادرة المستخدم
@bot.on_message (filters.left_chat_member)
async def Left_Chat (bot, message) :
	print("@bot.on_message (filters.left_chat_member)")
	print (message)
	data = db.get ("db")
	id = str(message.from_user.id)
	user = message.from_user.username
	group_id = str(message.chat.id)
	
	if message.left_chat_member.is_self :
		if group_id in data:
			del data[group_id]
			db.set ("db", data)
			print ("- Delete Group_id from Data Successful ✅️")
			print_json (data=data)
	else:
		if  id in data[group_id]["CAPTCHA"] :
			del data[group_id]["CAPTCHA"][id]
			db.set ("db", data)
			
		elif id in data[group_id]["Real_Acc"] :
			del data[group_id]["Real_Acc"][id]
			db.set ("db", data)
	
	
print ("Bot run ......")
asyncio.run (bot.run())
