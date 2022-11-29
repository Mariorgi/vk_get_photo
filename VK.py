import requests

class VK:
	def __init__(self, access_token, version='5.131'):
		self.access_token = access_token
		self.version = version
		self.params = {'access_token': self.access_token, 'v': self.version}
	
	def get_profile(self, user_nick):
		url = "https://api.vk.com/method/users.get"
		params = {'user_ids': user_nick}
		response = requests.post(url, params={**self.params, **params})
		return response.json()
	
	def get_photos(self, user_id, album_id='profile', extended = 1):
		url = "https://api.vk.com/method/photos.get"
		params = {'owner_id': user_id, 'album_id': album_id, 'extended': str(extended)}
		response = requests.post(url, params={**self.params, **params})
		return response.json()	
		
	def get_photo_data(self, user_id, photos_id, extended = 1):
		url = "https://api.vk.com/method/photos.getById"
		photos = ''
		if isinstance(photos_id, int):
			photos = f"{str(user_id)}_{str(photos_id)}"
		if isinstance(photos_id, list):
			for item in photos_id:
				photos = photos + f"{str(user_id)}_{str(item)},"

		params = {'photos': photos, 'extended':str(extended)}
		response = requests.post(url, params={**self.params, **params})
		return response.json()['response']
