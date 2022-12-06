import requests
import json

class Poligon:
	def __init__(self, token):
		self.urls = {"resources":"https://cloud-api.yandex.net/v1/disk/resources"} 	
		self.token = token
		self.headers = {'Authorization': 'OAuth ' + self.token}
		
	def dir_exist(self, name_dir):
		params = {"path" : f"{name_dir}"}
		url = self.urls['resources']
		response = requests.get(url, params=params, headers=self.headers)
		if response.ok:
			return True
			
		elif response.status_code == 404:
			return False
			
		else:
			return -1
		
	def create_dir(self, name_dir):
		params = {"path" : f"{name_dir}"}
		url = self.urls['resources']
		response = requests.put(url, params=params, headers=self.headers)
		return response.json()
	
	def upload_url_file(self, url_file, name_dir, name_file, disable_redirects = True):
		params = {"disable_redirects":disable_redirects, "path": f"disk:/{name_dir}/{name_file}", "url":f"{url_file}"}
		url = self.urls['resources'] + "/upload"
		response = requests.post(url, params=params, headers=self.headers)
		return response.json()
	
	def upload_status(self, url):
		response = requests.get(url, headers=self.headers)
		if response.json()['status'] == 'success':
			return True
			
		return False
		
		
	
