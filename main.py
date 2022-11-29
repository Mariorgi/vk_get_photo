import json
import os
from VK import VK
from Yandex import Poligon	
import requests
	
access_token = ''
poligon_token = ''

def output_to_console(count_photos, steps_max, step, type_work, wait=False):
	print("\n" * 100)
	print("Колличество фотографий: " + str(count_photos))
	out_type = ""
	index_char = 0
	if type_work == "save":
		out_type = out_type + "Сохраннение фотографии"
		
	elif type_work == "cloud":
		out_type = out_type + "Загрузка фотографии на облако"
		
	print(out_type)
	count_step = steps_max - step
	print("*" * step + "_" * count_step)
	if wait:
		print("Ожидание ответа сервера")




def main():
	print("\n" * 100)
	url_profile = input("Введите url адресс пользователя: ")
	user_nick = url_profile.split('/')[-1]
	if user_nick:
		if not os.path.exists(user_nick):
			os.mkdir(user_nick)
		yandex_poligon = Poligon(poligon_token)
		if not yandex_poligon.dir_exist(user_nick):
			yandex_poligon.create_dir(user_nick)
		vk = VK(access_token)
		data = vk.get_profile(user_nick)['response'][0]
		user_id =  data['id']
		data = vk.get_photos(user_id)['response']
		data_items = data['items']
		count_photos = data['count']
		steps_max = count_photos * 2
		step = 0
		photos_ids = []
		for i in range(data['count']):
			photos_ids.append(data_items[i]['id'])
		
		data = vk.get_photo_data(user_id, photos_ids)
		photos_data = {}

		for item in data:
			count_likes = item['likes']['count']
			width = item['orig_photo']['width']
			height = item['orig_photo']['height']
			sizes = item['sizes']
			date = item['date']
			isExist = False
			if str(count_likes) in photos_data.keys():
				isExist = True

			size_types = ['w', 'z', 'y', 'r', 'q', 'p', 'o', 'x', 'm', 's']
			small_index = len(size_types) - 1
			size_element_id = 0
			for i, item_size in enumerate(sizes):
				photo_size_type = item_size['type']
				size_type_index = size_types.index(photo_size_type)
				if size_type_index < small_index:
					small_index = size_types.index(photo_size_type)
					size_element_id = i
					continue

				elif size_type_index > small_index:
					continue

			element_size_photo = sizes[size_element_id]
			if isExist:
				photos_data[str(count_likes)+"_"+str(date)] = {'url':element_size_photo['url'], 'type':element_size_photo['type']}

			else:
				photos_data[str(count_likes)] = {'url':element_size_photo['url'], 'type':element_size_photo['type']}
						

		photos_list = []
		data_uploads = []
		for key, value in photos_data.items():
			photo_url = value['url']
			photo_extension = '.'+photo_url.split('/')[-1].split('?')[0].split('.')[-1]
			photo_name = str(key) + photo_extension
			response = requests.get(photo_url)
			with open(user_nick + '/' + photo_name, 'wb') as file:
				file.write(response.content)
				step += 1
				output_to_console(count_photos, steps_max, step, type_work="save")
				
			data_uploads.append(yandex_poligon.upload_url_file(photo_url, user_nick, photo_name))
			photos_list.append({"file_name":photo_name, 'size': f"{value['type']}"})
		
		with open(user_nick+'_photos.json', 'w') as file:
			file.write(json.dumps(photos_list, indent=4))
		
		status_list = [False for i in range(len(data_uploads))]
		time_out_cointer = 0 
		while not all(status_list):
			for i, item in enumerate(data_uploads):
				url = item['href']
				if status_list[i] == True:
					continue
				status = yandex_poligon.upload_status(url)
				if status and step <= steps_max:
					step += 1
					output_to_console(count_photos, steps_max, step, type_work="cloud")
					status_list[i] = True
					time_out_cointer = 0 
				else:
					time_out_cointer += 1
					if time_out_cointer > 3:
						output_to_console(count_photos, steps_max, step, type_work="cloud", wait=True)
				
			if time_out_cointer  >= steps_max//2:
				print("Время ожидания подошло к концу."
					  "\nПроверте полученные фотографии."
					  "\nЗавершение программы")
				break
		else:
			print("Успешное выполнение! Завершение программы")

if __name__ == "__main__":
	main()
		
		
		
		
       
