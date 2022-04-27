import telebot		
from telebot import REPLY_MARKUP_TYPES, types
import config                                
import os									  
from time import sleep

bot = telebot.TeleBot(config.TOKEN)          


@bot.message_handler(commands = ['start'])			
def start(message):
	
	journal = open('journal.txt', 'r')												
	dictionary = eval(journal.read())
	journal.close()

	if '{.id}'.format(message.from_user) not in os.listdir('work_folder'):			
		
		
		os.mkdir ('work_folder/{.id}'.format(message.from_user))
		os.mkdir ('work_folder/{.id}/passwords'.format(message.from_user))
		
		add_journal = open('work_folder/{.id}/add_journal.txt'.format(message.from_user), 'w') 
		add_journal.write('\n\n\n0')
		add_journal.close()

		callback_list_file = open('work_folder/{.id}/callback_list.txt'.format(message.from_user), 'w')
		callback_list_file.write(str([]))
		callback_list_file.close()

		password_name_list = open('work_folder/{.id}/password_name_list.txt'.format(message.from_user), 'w')
		password_name_list.write(str([]))
		password_name_list.close()

		check_file = open('work_folder/{.id}/check_file.txt'.format(message.from_user), 'w')
		check_file.close()

	
	add_journal = open('work_folder/{.id}/add_journal.txt'.format(message.from_user),'r')
	num = add_journal.read()[-1]
	add_journal.close()
	add_journal = open('work_folder/{.id}/add_journal.txt'.format(message.from_user),'w')
	add_journal.write('\n\n\n' + num)
	add_journal.close()

	markup = types.InlineKeyboardMarkup(row_width=1)								
	item1 = types.InlineKeyboardButton('Список паролей 📃', callback_data='list')
	item2 = types.InlineKeyboardButton('Добавить пароль ➕', callback_data='add')
	item3 = types.InlineKeyboardButton('Удалить пароль 🗑', callback_data='del')
	markup.add(item1, item2, item3)													


	if dictionary.get('{.id}'.format(message.from_user)) == None:																										
		
		sticker = open('hello_sticker.tgs','rb')
		bot.send_sticker(message.chat.id, sticker)
		
		bot.send_message(message.chat.id, 'Привет, {.first_name}, я хранитель паролей. Что будем делать ❓'.format(message.from_user) , reply_markup=markup)
		
		dictionary['{.id}'.format(message.from_user)] = 'start'								
		journal = open('journal.txt', 'w')
		journal.write(str(dictionary))
		journal.close()

	else:
		bot.send_message(message.chat.id, 'Что будем делать ❓'.format(message.from_user) , reply_markup=markup) 






@bot.message_handler(content_types=['text'])			
def lalala(message):
	
	journal = open('journal.txt', 'r')				
	dictionary = eval(journal.read())
	journal.close()

	try:
		check_file = open('work_folder/{.id}/check_file.txt'.format(message.from_user), 'w')
		check_file.write (r'{}'.format(message.text))
		
		check_file.close()
				

		if dictionary['{.id}'.format(message.from_user)] == 'add_name':

			if len(message.text) > 30:
				bot.send_message(message.chat.id, 'Ошибка ⚠️ ! Длина имени не должна превышать 30 символов. Введите имя:'.format(message.from_user))
			
			else:

				add_journal = open('work_folder/{.id}/add_journal.txt'.format(message.from_user),'r')
				num = add_journal.readlines()[-1]
				add_journal.close()
			
				file = open('work_folder/{.id}/add_journal.txt'.format(message.from_user),'w')
				file.write(r'{}'.format(message.text) + '\n\n\n' + num)
				file.close()



		if dictionary['{.id}'.format(message.from_user)] == 'add_login':
		
			if len(message.text) > 50:
				
				bot.send_message(message.chat.id, 'Ошибка ⚠️ ! Длина логина не должна превышать 50 символов. Введите логин:'.format(message.from_user))
			
			else:

				add_journal = open('work_folder/{.id}/add_journal.txt'.format(message.from_user),'r')
				text = add_journal.readlines()
				add_journal.close()

				file = open('work_folder/{.id}/add_journal.txt'.format(message.from_user),'w')
				file.write(r'{}'.format(text[0]) + r'{}'.format(message.text) + '\n\n' + text[-1])
				file.close()


		if dictionary['{.id}'.format(message.from_user)] == 'add_password':
			
			if len(message.text) > 50:
				
				bot.send_message(message.chat.id, 'Ошибка ⚠️ ! Длина пароля не должна превышать 50 символов. Введите пароль:'.format(message.from_user))
			
			else:

				add_journal = open('work_folder/{.id}/add_journal.txt'.format(message.from_user),'r')
				text = add_journal.readlines()
				add_journal.close()
	
				file = open('work_folder/{.id}/add_journal.txt'.format(message.from_user),'w')
				file.write(r'{}'.format(text[0]) + r'{}'.format(text[1]) + r'{}'.format(message.text) + '\n' + text[-1])
				file.close()
	
	except Exception as e:
		
		check_file.close()
		check_file = open('work_folder/{.id}/check_file.txt'.format(message.from_user), 'w')
		check_file.close()

		if dictionary['{.id}'.format(message.from_user)] == 'add_name':
			
			bot.send_message(message.chat.id, 'Ошибка ⚠️ ! Неподходящий символ. Попробуйте другое имя:'.format(message.from_user)) 
		
		elif dictionary['{.id}'.format(message.from_user)] == 'add_login':

			bot.send_message(message.chat.id, 'Ошибка ⚠️ ! Неподходящий символ. Попробуйте другой логин:'.format(message.from_user)) 
	
		elif dictionary['{.id}'.format(message.from_user)] == 'add_password':

			bot.send_message(message.chat.id, 'Ошибка ⚠️ ! Неподходящий символ. Попробуйте другой пароль:'.format(message.from_user)) 

	
		
		



@bot.callback_query_handler(func=lambda call: True)		
def choose(call):
	
	journal = open('journal.txt', 'r')												
	dictionary = eval(journal.read())
	journal.close()
	
	callback_list_file = open('work_folder/{.id}/callback_list.txt'.format(call.from_user), 'r')
	callback_list = eval(callback_list_file.read())
	callback_list_file.close()

	if call.message:
		
		if call.data == 'add':
			
			
			add_journal = open('work_folder/{.id}/add_journal.txt'.format(call.from_user),'r')
			num = add_journal.readlines()[-1]
			add_journal.close()

			if int(num) <= 50:

				bot.delete_message(chat_id=call.message.chat.id, message_id= call.message.message_id)

				markup = types.InlineKeyboardMarkup()								
				
				item1 = types.InlineKeyboardButton('Отмена ❌', callback_data='back')
				item2 = types.InlineKeyboardButton('Далее ➡️', callback_data='add_login')
				
				markup.add(item1,item2)

				bot.send_message(call.message.chat.id, 'Введите название:', reply_markup = markup)

			
				dictionary['{.id}'.format(call.from_user)] = 'add_name'								
				journal = open('journal.txt', 'w')
				journal.write(str(dictionary))
				journal.close()

			else:

				bot.delete_message(chat_id=call.message.chat.id, message_id= call.message.message_id)

				markup = types.InlineKeyboardMarkup()								
				item1 = types.InlineKeyboardButton('Назад ⬅️', callback_data='back')
				markup.add(item1)

				bot.send_message(call.message.chat.id, 'Ошибка ⚠️ ! Количество паролей не должно превышать 50', reply_markup = markup)



		if call.data == 'add_login':
			add_journal = open('work_folder/{.id}/add_journal.txt'.format(call.from_user),'r')
			
			password_name_list = open('work_folder/{.id}/password_name_list.txt'.format(call.from_user), 'r')
			password_list = eval(password_name_list.read())
			password_name_list.close()

			text = add_journal.readlines()[0]
			
			add_journal.close()
			
			if text == '\n':
				bot.delete_message(chat_id=call.message.chat.id, message_id= call.message.message_id)

				markup = types.InlineKeyboardMarkup()
				
				item1 = types.InlineKeyboardButton('Отмена ❌', callback_data = 'back')
				item2 = types.InlineKeyboardButton('Далее ➡️', callback_data='add_login')
								
				markup.add(item1,item2)

				bot.send_message(call.message.chat.id, 'Ошибка ⚠️ ! Введите имя:', reply_markup = markup)
			
			elif text[0:-1] in password_list:
				bot.delete_message(chat_id=call.message.chat.id, message_id= call.message.message_id)

				markup = types.InlineKeyboardMarkup()
				
				item1 = types.InlineKeyboardButton('Отмена ❌', callback_data='back')
				item2 = types.InlineKeyboardButton('Далее ➡️', callback_data='add_login')

				markup.add(item1, item2)
				
				bot.send_message(call.message.chat.id, 'Ошибка ⚠️ ! Это имя уже занято. Введите другое:', reply_markup = markup)
				
			else:		
			
			
				bot.edit_message_text(chat_id=call.message.chat.id, message_id= call.message.message_id, text='Введите название:',
				reply_markup=None)

				markup = types.InlineKeyboardMarkup(row_width = 2)		
				
				item1 = types.InlineKeyboardButton('Отмена ❌', callback_data = 'back')
				item2 = types.InlineKeyboardButton('Пропустить ⏩', callback_data = 'login_pass')
				item3 = types.InlineKeyboardButton('Далее ➡️', callback_data='add_password')
				
				markup.add(item1, item2, item3)

				bot.send_message(call.message.chat.id, 'Введите логин:', reply_markup = markup)

				dictionary['{.id}'.format(call.from_user)] = 'add_login'								
				journal = open('journal.txt', 'w')
				journal.write(str(dictionary))
				journal.close()

		if call.data == 'login_pass':
			
			bot.delete_message(chat_id=call.message.chat.id, message_id= call.message.message_id)
			
			add_journal = open('work_folder/{.id}/add_journal.txt'.format(call.from_user),'r')
			text = add_journal.readlines()
			add_journal.close()
			
			file = open('work_folder/{.id}/add_journal.txt'.format(call.from_user),'w')
			file.write(r'{}'.format(text[0]) + r'{}'.format('None_none_None_none') + '\n\n' + text[-1])
			file.close()
			
			markup = types.InlineKeyboardMarkup()		
			
			item1 = types.InlineKeyboardButton('Отмена ❌', callback_data = 'back')
			item2 = types.InlineKeyboardButton('Готово ✅', callback_data = 'add_password_done')
			
			markup.add(item1, item2)

			bot.send_message(call.message.chat.id, 'Введите пароль:', reply_markup = markup)
			
			journal = open('journal.txt','r')
			dictionary = eval(journal.read())
			journal.close()

			dictionary['{.id}'.format(call.from_user)] = 'add_password'								
			
			journal = open('journal.txt', 'w')
			journal.write(str(dictionary))
			journal.close()
		

		if call.data == 'add_password':
			
			add_journal = open('work_folder/{.id}/add_journal.txt'.format(call.from_user),'r')
			text = add_journal.readlines()
			add_journal.close()

			if text[1] == '\n':
				bot.delete_message(chat_id=call.message.chat.id, message_id= call.message.message_id)

				markup = types.InlineKeyboardMarkup()
				
				item1 = types.InlineKeyboardButton('Отмена ❌', callback_data = 'back')
				item2 = types.InlineKeyboardButton('Далее ➡️', callback_data='add_password')
								
				markup.add(item1,item2)

				bot.send_message(call.message.chat.id, 'Ошибка ⚠️ ! Введите логин:', reply_markup = markup)


			else:
				bot.edit_message_text(chat_id=call.message.chat.id, message_id= call.message.message_id, text='Введите логин:',
				reply_markup=None)
			
				markup = types.InlineKeyboardMarkup()		
				
				item1 = types.InlineKeyboardButton('Отмена ❌', callback_data = 'back')
				item2 = types.InlineKeyboardButton(' Готово ✅', callback_data = 'add_password_done')
			
				markup.add(item1, item2)

				bot.send_message(call.message.chat.id, 'Введите пароль:', reply_markup = markup)
			
				journal = open('journal.txt','r')
				dictionary = eval(journal.read())
				journal.close()

				dictionary['{.id}'.format(call.from_user)] = 'add_password'								
			
				journal = open('journal.txt', 'w')
				journal.write(str(dictionary))
				journal.close()
		

		if call.data == 'add_password_done':
						
			add_journal = open('work_folder/{.id}/add_journal.txt'.format(call.from_user),'r')					
			text = add_journal.readlines()
			add_journal.close()	

			if text[2] == '\n':
				bot.delete_message(chat_id=call.message.chat.id, message_id= call.message.message_id)

				markup = types.InlineKeyboardMarkup()

				item1 = types.InlineKeyboardButton('Отмена ❌', callback_data = 'back')
				item2 = types.InlineKeyboardButton('Готово ✅', callback_data='add_password_done')
				
				markup.add(item1, item2)

				bot.send_message(call.message.chat.id, 'Ошибка ⚠️ ! Введите пароль:', reply_markup = markup)
			
			else:
				password_name_list = open('work_folder/{.id}/password_name_list.txt'.format(call.from_user), 'r')
				password_list = eval(password_name_list.read())
				password_name_list.close()

				add_journal = open('work_folder/{.id}/add_journal.txt'.format(call.from_user),'r')
				num = int(add_journal.read()[-1])
				add_journal.close()

				text1 = text[0][0:-1]

			
				password_list.append(text1)
				password_list.sort()


				index = password_list.index(text1)

				if num > 0 and index != num:
				
					num_count = num - 1
					
					file_write = open ('work_folder/{.id}/passwords/password_{}.txt'.format(call.from_user, num), 'w')
					file_write.close()

					while num_count + 1 != index:
					
						file_read = open ('work_folder/{.id}/passwords/password_{}.txt'.format(call.from_user, num_count), 'r')
						text_overwriting = file_read.read()
						file_read.close()

						file_write = open ('work_folder/{.id}/passwords/password_{}.txt'.format(call.from_user, num_count+1), 'w')
						file_write.write(text_overwriting)
						file_write.close()

						num_count -= 1
					
					file = open(r'work_folder/{.id}/passwords/password_{}.txt'.format(call.from_user, str(index)) ,'w')	
					file.write(r'{}'.format(text[0]) + r'{}'.format(text[1]) + r'{}'.format(text[2]))																							
					file.close()
				
													
				else:
					
					file = open(r'work_folder/{.id}/passwords/password_{}.txt'.format(call.from_user, index) ,'w')	
					file.write(r'{}'.format(text[0]) + r'{}'.format(text[1]) + r'{}'.format(text[2]))																							
					file.close()

				num += 1
				
				add_journal = open('work_folder/{.id}/add_journal.txt'.format(call.from_user),'w')
				add_journal.write('\n\n\n' + str(num))
				add_journal.close()

				password_name_list = open('work_folder/{.id}/password_name_list.txt'.format(call.from_user), 'w')
				password_name_list.write (str(password_list))
				password_name_list.close()

				markup = types.InlineKeyboardMarkup(row_width=1)								 
				item1 = types.InlineKeyboardButton('Список паролей 📃', callback_data='list')
				item2 = types.InlineKeyboardButton('Добавить пароль ➕', callback_data='add')
				item3 = types.InlineKeyboardButton('Удалить пароль 🗑', callback_data='del')
				markup.add(item1, item2, item3)													

				if dictionary['{.id}'.format(call.from_user)] == 'add_password':
					bot.edit_message_text(chat_id=call.message.chat.id, message_id= call.message.message_id, text='Введите пароль:'.format(call.from_user),
					reply_markup=None)


				bot.send_message(call.message.chat.id, 'Что будем делать ❓', reply_markup = markup)

		if call.data == 'list':
			

			bot.delete_message(chat_id=call.message.chat.id, message_id= call.message.message_id)
						
			
			add_journal = open('work_folder/{.id}/add_journal.txt'.format(call.from_user),'r')
			num_count = int(add_journal.readlines()[-1])
			add_journal.close()

			

			markup = types.InlineKeyboardMarkup(row_width=1)
			
			
			if num_count == 0:

				markup = types.InlineKeyboardMarkup()								 
				item = types.InlineKeyboardButton('Назад ⬅️', callback_data='back')
				markup.add(item)

				bot.send_message(call.message.chat.id, 'У вас нет паролей', reply_markup = markup)
				
			else:
				
				for i in range(num_count):
					
					file = open(r'work_folder/{.id}/passwords/password_{}.txt'.format(call.from_user, str(i)) ,'r')
					text = file.readlines()[0][0:-1]

					button = types.InlineKeyboardButton(text, callback_data= str(i))
					markup.add(button)

					file.close()

					callback_list_file = open('work_folder/{.id}/callback_list.txt'.format(call.from_user), 'r')
					callback_list = eval(callback_list_file.read())
					callback_list_file.close()

					callback_list.append(str(i))

					callback_list_file = open('work_folder/{.id}/callback_list.txt'.format(call.from_user), 'w')
					callback_list_file.write(str(callback_list))
					callback_list_file.close()
				
				item_back = types.InlineKeyboardButton('Назад ⬅️', callback_data = 'back')
				markup.add(item_back)
				
				bot.send_message(call.message.chat.id, 'Выберите пароль:', reply_markup = markup)
			
	

		if call.data in callback_list and len(call.data) == 1:
			
			file = open(r'work_folder/{.id}/passwords/password_{}.txt'.format(call.from_user, call.data) ,'r')
			text = file.readlines()
			file.close()

			markup = types.InlineKeyboardMarkup()								 
			item = types.InlineKeyboardButton('Назад ⬅️', callback_data='back')
			markup.add(item)		

			if text[1] == 'None_none_None_none\n':
				bot.send_message(call.message.chat.id, 'Имя: '+text[0]+'\nПароль: '+text[2], reply_markup = markup)
			else:
				bot.send_message(call.message.chat.id, 'Имя: '+text[0]+'\nЛогин: '+text[1]+'\nПароль: '+text[2], reply_markup = markup)

			callback_list_file = open('work_folder/{.id}/callback_list.txt'.format(call.from_user), 'w')
			callback_list_file.write(str([]))
			callback_list_file.close()

			
			bot.delete_message(chat_id=call.message.chat.id, message_id= call.message.message_id)

		if call.data == 'back':
			
			bot.delete_message(chat_id=call.message.chat.id, message_id= call.message.message_id)
			
			markup = types.InlineKeyboardMarkup(row_width=1)								 
			item1 = types.InlineKeyboardButton('Список паролей 📃', callback_data='list')
			item2 = types.InlineKeyboardButton('Добавить пароль ➕', callback_data='add')
			item3 = types.InlineKeyboardButton('Удалить пароль 🗑', callback_data='del')
			markup.add(item1, item2, item3)		

			bot.send_message(call.message.chat.id, 'Что будем делать ❓', reply_markup = markup)


		if call.data == 'del':
			
			bot.delete_message(chat_id=call.message.chat.id, message_id= call.message.message_id)
						
			
			add_journal = open('work_folder/{.id}/add_journal.txt'.format(call.from_user),'r')
			num_count = int(add_journal.readlines()[-1])
			add_journal.close()


			markup = types.InlineKeyboardMarkup(row_width=1)
			
			
			if num_count == 0:

							 
				item = types.InlineKeyboardButton('Назад ⬅️', callback_data='back')
				markup.add(item)

				bot.send_message(call.message.chat.id, 'У вас нет паролей', reply_markup = markup)
				
			else:
				
				for i in range(num_count):
					
					file = open(r'work_folder/{.id}/passwords/password_{}.txt'.format(call.from_user, str(i)) ,'r')
					text = file.readlines()[0][0:-1]

					button = types.InlineKeyboardButton(text, callback_data= str(i) + 'd')
					markup.add(button)

					file.close()

					callback_list_file = open('work_folder/{.id}/callback_list.txt'.format(call.from_user), 'r')
					callback_list = eval(callback_list_file.read())
					callback_list_file.close()

					callback_list.append(str(i) + 'd')

					callback_list_file = open('work_folder/{.id}/callback_list.txt'.format(call.from_user), 'w')
					callback_list_file.write(str(callback_list))
					callback_list_file.close()
				
				item = types.InlineKeyboardButton('Удалить все 🗑', callback_data = 'del_all')
				item_back = types.InlineKeyboardButton('Назад ⬅️', callback_data = 'back')
				markup.add(item,item_back)
				
				bot.send_message(call.message.chat.id, 'Выберите пароль:', reply_markup = markup)

		if call.data in callback_list and len(call.data) == 2:
			os.remove(r'work_folder/{.id}/passwords/password_{}.txt'.format(call.from_user, call.data[0]))

			password_name_list = open('work_folder/{.id}/password_name_list.txt'.format(call.from_user), 'r')
			password_list = eval(password_name_list.read())
			password_name_list.close()

			password_list.pop(int(call.data[0]))

			password_name_list = open('work_folder/{.id}/password_name_list.txt'.format(call.from_user), 'w')
			password_name_list.write (str(password_list))
			password_name_list.close()

			callback_list_file = open('work_folder/{.id}/callback_list.txt'.format(call.from_user), 'w')
			callback_list_file.write(str([]))
			callback_list_file.close()

			add_journal = open('work_folder/{.id}/add_journal.txt'.format(call.from_user),'r') 
			num_count = int(add_journal.readlines()[-1])
			add_journal.close()

			num_count -= 1

			add_journal = open('work_folder/{.id}/add_journal.txt'.format(call.from_user),'w')
			add_journal.write('\n\n\n' +str(num_count))
			add_journal.close()


			bot.delete_message(chat_id=call.message.chat.id, message_id= call.message.message_id)


			if num_count >= 1 and num_count != int(call.data[0]):
				
				for i in range(int(call.data[0]), num_count):
					
					file_read = open ('work_folder/{.id}/passwords/password_{}.txt'.format(call.from_user, i+1), 'r')
					text = file_read.read()
					file_read.close()

					file_write = open ('work_folder/{.id}/passwords/password_{}.txt'.format(call.from_user, i), 'w')
					file_write.write(text)
					file_write.close()

				os.remove (r'work_folder/{.id}/passwords/password_{}.txt'.format(call.from_user, num_count))

			markup = types.InlineKeyboardMarkup(row_width=1)								 
			item1 = types.InlineKeyboardButton('Список паролей 📃', callback_data='list')
			item2 = types.InlineKeyboardButton('Добавить пароль ➕', callback_data='add')
			item3 = types.InlineKeyboardButton('Удалить пароль 🗑', callback_data='del')
			markup.add(item1, item2, item3)		

			bot.send_message(call.message.chat.id, 'Что будем делать ❓', reply_markup = markup)

		if call.data == 'del_all':
			
			password_name_list = open('work_folder/{.id}/password_name_list.txt'.format(call.from_user), 'w')
			password_name_list.write (str([]))
			password_name_list.close()

			add_journal = open('work_folder/{.id}/add_journal.txt'.format(call.from_user),'r') 
			num = int(add_journal.readlines()[-1])
			add_journal.close()

			add_journal = open('work_folder/{.id}/add_journal.txt'.format(call.from_user),'w')
			add_journal.write('\n\n\n' + '0' )
			add_journal.close()

			for i in range(num):
				os.remove(r'work_folder/{.id}/passwords/password_{}.txt'.format(call.from_user, i))
			
			bot.delete_message(chat_id=call.message.chat.id, message_id= call.message.message_id)

			markup = types.InlineKeyboardMarkup(row_width=1)								 
			item1 = types.InlineKeyboardButton('Список паролей 📃', callback_data='list')
			item2 = types.InlineKeyboardButton('Добавить пароль ➕', callback_data='add')
			item3 = types.InlineKeyboardButton('Удалить пароль 🗑', callback_data='del')
			markup.add(item1, item2, item3)		

			bot.send_message(call.message.chat.id, 'Что будем делать ❓', reply_markup = markup)



bot.polling (none_stop=True)		 #RUN bot




