from django.shortcuts import render
from django.views.generic import TemplateView

from django.http import HttpResponse
import datetime
from django.utils import timezone

from django.template import loader

from django.shortcuts import redirect
import grequests
import requests
from bs4 import BeautifulSoup
import re

from .forms import PostForm
from howdy.models import album
from howdy.models import albums
from howdy.models import fruits
# Create your views here.

class HomePageView(TemplateView):
	def get(self, request, **kwargs):
		return render(request, 'index.html', context = None)


def Fruitapp(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)

def index(request):
    latest_question_list = ['g', 'z', 'a']
    template = loader.get_template('indexvote.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))

def dictindex(request):	

    latest_question_dict = {'g' : '34', 'z': '44', 'a': '54'}
    template = loader.get_template('indexdictionary.html')
    context = {
        'latest_question_dict': latest_question_dict,
    }
    return HttpResponse(template.render(context, request))

def classindex(request):
	dictionary_of_fruits = {'apple':4, 'grape ': 2, 'orange': 7}
	objectified_fruit_list = []
	class ip:
		#"""docstring for ip"""
		def __init__(self, fruit_weight, fruit_name):
			self.fruit_name = fruit_name
			self.fruit_weight = fruit_weight


		def weight_in_grams(self, fruit_weight):
			self.weight_g = fruit_weight*1000
			return self.weight_g

	for key,value in dictionary_of_fruits.items():
		fruit = ip(value, key)
		fruit.weight_in_grams(fruit.fruit_weight)
		objectified_fruit_list.append(fruit)

	hi = 'saluete'

	template = loader.get_template('indexobjects.html')
	context = {
		'latest_question_object' : objectified_fruit_list, 'salsa' : hi
	}
	return HttpResponse(template.render(context, request))

def fruitapptesco(request, fruit1, weight1, fruit2, weight2, fruit3, weight3):

	#dictionary with key and list as value. each list contains objects

	class fruit:
		def __init__(self,description, id , offer , line_price, no_items, id_name,per_price):
			self.description = description
			self.id = id 
			self.line_price = float(re.findall(r"[-+]?\d*\.\d+|\d+",line_price)[0])
			self.offer = offer
			self.no_items = float(no_items)
			self.id_name = id_name
			self.per_price = per_price
			self.determine_price_type()
			self.determine_package_type()

		def determine_price_type(self):
				if 'each' in str(self.per_price):
					self.each_price = float(re.findall(r"[-+]?\d*\.\d+|\d+", self.per_price)[0])
					self.price_tipe = 1
				elif 'kg' in str(self.per_price):
					self.kg_price = float(re.findall(r"[-+]?\d*\.\d+|\d+",self.per_price)[0])
					self.price_tipe = 2
				else:
					self.price_tipe = 0
				if (self.line_price >= 0.69) & (self.price_tipe == 1) & ('pack' not in self.description):
					self.watermelon = True
				else:
					self.watermelon = False
	#if item2.price_tipe == 1 & item2.pack_nub == 1 & item2.watermelon == False:
	#item2.remove()


		def determine_package_type(self):
				try:
					self.weight_in_des = re.findall(r"[0-9]+g", self.description)
					if len(self.weight_in_des) == 0:
						self.weight_in_des = None
						self.weight_in_des_id = 0
					elif len(self.weight_in_des) == 1:
						self.weight_in_des = float((re.findall(r"[-+]?\d*\.\d+|\d+", self.weight_in_des[0]))[0])
						print self.weight_in_des
						self.weight_in_des_id = 1
					else:
						self.weight_in_des = None
						self.weight_in_des_id = 0

				except:
					self.weight_in_des= None
					self.weight_in_des_id = 0

				try:
					if 'pack' in self.description:
						self.pack_numb = float(re.findall(r" [0-9] ", self.description))
						if len(self.pack_numb) == 0 :
							self.pack_numb = None
							self.pack_numb_id = 0
						elif len(self.pack_numb) == 1:
							self.pack_numb = self.pack_numb[0]
							self.pack_numb_id = 1
					else:
						self.pack_numb = None
						self.pack_numb_id = 0
				except:
					self.pack_numb = None
					self.pack_numb_id = 0


				try:
					if 'loose' in self.description:
						self.loose_id = 1

					else:
						self.loose_id=0
				except:
					self.loose_id =0

				try:
					if 'each' in self.description:
						self.each_id = 1
					else :
						self.each_id = 0
				except:
					self.each_id = 0



	brian_list = {fruit1 : weight1, fruit2 : weight2, fruit3: weight3}

	extension = '&Nao='
	iteraction = 0


	url = 'http://www.tesco.com/groceries/product/browse/default.aspx?N=4294793658&Ne=4294793660' + extension
	list_of_random_fruits = []

	def match_function_tesco(item_description, id_number_of_item,offer,line_price,per_price):
		for given_fruit in brian_list:
			no_items = brian_list[given_fruit]
			id_name = str(given_fruit).lower()
			if id_name in item_description:

				given_fruit = fruit(item_description, id_number_of_item, offer, line_price, no_items, id_name, per_price)
				for item in list_of_random_fruits:
					if given_fruit.description == item.description:
						list_of_random_fruits.remove(item)
				list_of_random_fruits.append(given_fruit)



	sorted_dictionary = {}

	def sort_fruits():
		for given_fruit in brian_list:
			id_name = str(given_fruit).lower()
			sorted_list = []
			for algo_found_fruit in list_of_random_fruits:
				if (id_name == algo_found_fruit.id_name):
					sorted_list.append(algo_found_fruit)

			sorted_dictionary.update({given_fruit:sorted_list})


	with requests.Session() as s:
		while (iteraction <= 100): #more flexibility by getting how many pages exist
			#get url first at 0 find the page number and times by n-1 
			#thats number of interaction
			#can even save in a function

			dynamic_url = url + str(iteraction)
			print dynamic_url
			results = s.get(dynamic_url)
			print results.status_code
			soup = BeautifulSoup(results.content, 'html.parser')
			for item in soup.find_all('li'):
				if "product clearfix" in str(item):
					id_number_of_item = item.get('data-product-id')
					product_details = str(item)
					item_description = product_details.split('<span data-title="true">')[1].split('</span>')[0].lower()
					if "promoNew" in str(item):
						offer = True
					else:
						offer = False
					#get image aswell will be usefull when using django
					for price in item.find_all('p', {'class', 'price'}):
						line_price = str(price).split('<span class="linePrice">')[1].split('</span>')[0]
						per_price = str(price).split('<span class="linePriceAbbr">(')[1].split(')</span>')[0]

					match_function_tesco(item_description, id_number_of_item,offer,line_price,per_price)
			print iteraction
			iteraction += 20

	sort_fruits()


	def filter_unduables():
		for item in sorted_dictionary:
			for item2 in sorted_dictionary[item]:

				if (item2.weight_in_des_id == 0) & (item2.pack_numb_id == 0) & (item2.loose_id == 0) & (item2.each_id == 0) & (item2.watermelon == False) & (item2.price_tipe == 1) :
					sorted_dictionary[item].remove(item2)
					print 'base delete', item2.description, '|||' ,item2.weight_in_des_id , item2.weight_in_des, item2.pack_numb_id, item2.pack_numb, item2.loose_id, item2.each_id, '|||', item2.price_tipe, item2.watermelon, item2.line_price, item2.offer
					
				if (item2.weight_in_des_id == 0) & (item2.pack_numb_id == 0) & (item2.loose_id == 0) & (item2.each_id == 1) & (item2.watermelon == False) & (item2.price_tipe == 1)  :
					sorted_dictionary[item].remove(item2)
					print 'each delete', item2.description, '|||' ,item2.weight_in_des_id , item2.weight_in_des,  item2.pack_numb_id, item2.pack_numb, item2.loose_id, item2.each_id, '|||', item2.price_tipe, item2.watermelon, item2.line_price, item2.offer

				if (item2.weight_in_des_id == 0) & (item2.pack_numb_id == 1) & (item2.loose_id == 0) & (item2.each_id == 1) & (item2.watermelon == False) & (item2.price_tipe == 1)  :
					sorted_dictionary[item].remove(item2)
					print 'rest', item2.description, '|||' ,item2.weight_in_des_id , item2.weight_in_des,  item2.pack_numb_id, item2.pack_numb, item2.loose_id, item2.each_id, '|||', item2.price_tipe, item2.watermelon, item2.line_price, item2.offer

				if (item2.weight_in_des_id == 0) & (item2.pack_numb_id == 1) & (item2.loose_id == 0) & (item2.each_id == 0) & (item2.watermelon == False) & (item2.price_tipe == 1)  :
					sorted_dictionary[item].remove(item2)
					print 'optimal', item2.description, '|||' ,item2.weight_in_des_id , item2.weight_in_des,  item2.pack_numb_id, item2.pack_numb, item2.loose_id, item2.each_id, '|||', item2.price_tipe, item2.watermelon, item2.line_price, item2.offer

				
	def price_weight_sorter():
		for item in sorted_dictionary:
			for item2 in sorted_dictionary[item]:
				try:
					if (item2.weight_in_des_id == 1):
						item2.weight_item = item2.weight_in_des/1000.00
					elif item2.watermelon == True :
						item2.weight_item = 1
					elif (item2.loose_id == 1) & (item2.price_tipe == 2):
						item2.weight_item = item2.line_price/item2.kg_price
					elif (item2.pack_numb_id == 1) & (item2.price_tipe == 2):
						item2.weight_item = (item2.line_price/item2.pack_numb)/item2.kg_price
					else:
						item2.weight_item =999
						
					print 'passed', item2.description, item2.weight_item


				except:
					print 'failed at price weight sorter'

				


	filter_unduables()
	price_weight_sorter()




	class bag:
		def __init__ (self, item3, number_of_items):
			self.number_of_items = number_of_items
			self.item3 = item3
			self.find_price()

		def find_price(self):
			self.found_price = self.number_of_items * self.item3.line_price
			#print self.item3.line_price


	Temp_bag_object_list_winner1 = []

	def mathematical_price_mass_optimazation(item_first_loop, item2, item3_next, item3, mass, number_of_items,Temp_bag_object_list_takeover2):


			item = item_first_loop
			index3 = sorted_dictionary[item].index(item3_next)
			
			print 'list 1 inside start function:', Temp_bag_object_list_winner1
			print 'list 2 inside start function:',Temp_bag_object_list_takeover2
			print 'index3', index3, 'should be one smaller than +1', (len(sorted_dictionary[item])-1), 'normal one', len(sorted_dictionary[item])


			if index3 == (len(sorted_dictionary[item])-1):
				print 'hi'
				return


			if str(sorted_dictionary[item][0].description) == str(item2.description):
				#print 'my description should be the same;', sorted_dictionary[item][0].description, 'and', item3_next.description
				print 'my description should be the same;', sorted_dictionary[item][0].description, 'and', item2.description
				if number_of_items != 0.0:
					
					print 'should be more than 0' , number_of_items
					print 'the mass' , mass


				
					reminder = mass % item3_next.weight_item
					print 'weight item in first/1 if'
					
					print 'after the first iteraction no items:', number_of_items

					item_first_loop = bag(item3, number_of_items)
					number_of_items = mass // item3_next.weight_item

					Temp_bag_object_list_winner1.append(item_first_loop)
					print 'the new mass/reminder', reminder
					mathematical_price_mass_optimazation(item , item2, sorted_dictionary[item][index3 + 1],sorted_dictionary[item][index3], reminder, number_of_items, Temp_bag_object_list_takeover2)
					print 'reutn1'
					return
				
				else:
					print 'in else 1 --------------------------------------------------------'
					print 'number_of_items should be 0', number_of_items, 'the current reminder/mass is:', mass, 'weight of item', item3_next.weight_item
					if item3_next.weight_item > mass:
						mathematical_price_mass_optimazation(item , item2, sorted_dictionary[item][index3 + 1], sorted_dictionary[item][index3], mass, number_of_items, Temp_bag_object_list_takeover2)
						print 'return2'
					elif item3_next.weight_item <= mass:
						number_of_items = mass //item3_next.weight_item
						reminder = mass % item3_next.weight_item
						print 'The new number of items', number_of_items,
						mathematical_price_mass_optimazation(item , item2, sorted_dictionary[item][index3 + 1], sorted_dictionary[item][index3], reminder, number_of_items,Temp_bag_object_list_takeover2)
						print 'return3'
						return
					else:
						print 'error'


					#item2 for every item3_next(starts at lady apples) recursion takes it throw appending through found item3_next then next item2. starts agian at item 3 recutsion checks for every item(but starting at first item3_next the recursion)
					#what we want to do is start at item3_next[1] for second iteraction but then check for first item last
					#


			elif str(sorted_dictionary[item][0].description) != str(item2.description):
				print 'my description should not be the same;', sorted_dictionary[item][0].description, 'and', item2.description
				if number_of_items != 0.0:

					print 'should be more than 0' , number_of_items
					print 'the mass' , mass
				
					reminder = mass % item3_next.weight_item
					
					print 'after the first iteraction no items:', number_of_items

					item_first_loop = bag(item3, number_of_items)
					number_of_items = mass // item3_next.weight_item

					Temp_bag_object_list_takeover2.append(item_first_loop)
					print 'the new mass/reminder', reminder
					mathematical_price_mass_optimazation(item , item2, sorted_dictionary[item][index3 + 1],sorted_dictionary[item][index3], reminder, number_of_items, Temp_bag_object_list_takeover2)
					print 'reutn4'
					return

				else:

					print 'in else 2 --------------------------------------------------------'
					print 'number_of_items should be 0', number_of_items, 'the current reminder/mass is:', mass, 'weight of item', item3_next.weight_item
					if item3_next.weight_item > mass:
						mathematical_price_mass_optimazation(item , item2, sorted_dictionary[item][index3 + 1], sorted_dictionary[item][index3] , mass, number_of_items,Temp_bag_object_list_takeover2)
						print 'return5'
					elif item3_next.weight_item <= mass:
						number_of_items = mass //item3_next.weight_item
						reminder = mass % item3_next.weight_item
						print 'The new number of items', number_of_items,
						mathematical_price_mass_optimazation(item , item2, sorted_dictionary[item][index3 + 1],sorted_dictionary[item][index3], reminder, number_of_items,Temp_bag_object_list_takeover2)
						print 'return6'
						return
					else:
						print 'error'


			else:
				print 'error'


	def update_mathematical_optimazation(Temp_bag_object_list_winner1,Temp_bag_object_list_takeover2):
		list1 = []
		list2 = []
		#global Temp_bag_object_list_winner1
		if len(Temp_bag_object_list_takeover2) != 0:
			for obj_instance in Temp_bag_object_list_winner1:
				print 'in winner list',obj_instance.item3.description, obj_instance.found_price, obj_instance.item3.line_price, obj_instance.number_of_items
				list1.append(obj_instance.found_price)
			sum_list1 = sum(list1)
			for obj_instance in Temp_bag_object_list_takeover2:
				print 'in takeover list', obj_instance.item3.description,  obj_instance.found_price, obj_instance.item3.line_price, obj_instance.number_of_items
				list2.append(obj_instance.found_price)
			sum_list2 = sum(list2)
			print 'sum list 1;' , sum_list1, 'sum list 2;', sum_list2
			if float(sum_list2) < float(sum_list1):
				print 'updating 1'
				print 'first temp bag', Temp_bag_object_list_winner1
				Temp_bag_object_list_winner1 = Temp_bag_object_list_takeover2
				print 'after assigning' , Temp_bag_object_list_winner1
				Temp_bag_object_list_takeover2 = []
			elif float(sum_list1) == 0:
				Temp_bag_object_list_winner1 = Temp_bag_object_list_takeover2
				Temp_bag_object_list_takeover2 = []
			else:
				print 'updating 2'
				Temp_bag_object_list_winner1 = Temp_bag_object_list_winner1
				Temp_bag_object_list_takeover2 = []

		else:
			print 'updating 2'
			for obj_instance in Temp_bag_object_list_winner1:
				print 'in winner list', obj_instance.item3.description
			Temp_bag_object_list_winner1 = Temp_bag_object_list_winner1
			Temp_bag_object_list_takeover2 = []



	def show_optimazation():
		list1 = []
		for obj_instance in Temp_bag_object_list_winner1:
			print 'final object', obj_instance.item3.description
			list1.append(obj_instance.found_price)
		sum_list1 = sum(list1)
		return sum_list1

	final_dictionaty_with_optimised_objects = {}

	for item in sorted_dictionary:
		item2_sorted_dictionary = sorted_dictionary[item]
		item3_sorted_dictionary = sorted_dictionary[item] 
		print '---------------------------------------------------------------------------------------------------%s---------------------------------------------------------------------' % (item)

		for item2 in item2_sorted_dictionary:
			 for item3 in item3_sorted_dictionary:
			 	print 'description of item 2', item2.description
			 	
			 	Temp_bag_object_list_takeover2 = [] 
			 	print item3.weight_item


			 	number_of_items = item2.no_items // item3.weight_item
			 	reminder = item2.no_items % item3.weight_item
			 	
			 	# if number_of_items != 0:
			 	# 	item = bag(item3, number_of_items)
			 	# 	Temp_bag_object_list_winner1.append(item)
			 	#aaa(item2,item3, reminder, counter)
			 	print 'list 1 outside start function:', Temp_bag_object_list_winner1
			 	print 'list 2 outside start function:',Temp_bag_object_list_takeover2
			 	mathematical_price_mass_optimazation(item, item2, item3, item3, reminder, number_of_items, Temp_bag_object_list_takeover2)
			 	item3_sorted_dictionary.remove(item3)
			 	item3_sorted_dictionary.append(item3)
			 	print 'winner', Temp_bag_object_list_winner1
			 	print 'challenger', Temp_bag_object_list_takeover2
			 	update_mathematical_optimazation(Temp_bag_object_list_winner1, Temp_bag_object_list_takeover2)
			 	print 'out side of loop ' , Temp_bag_object_list_winner1
			 	print 'end of line'
				break

		final_price = show_optimazation()
		final_dictionaty_with_optimised_objects.update({item: Temp_bag_object_list_winner1})

		print 'end of line, the price is:',final_price 







			
					

	for item in final_dictionaty_with_optimised_objects:
		for item2 in final_dictionaty_with_optimised_objects[item]:
			fruit = item2.item3.description
			number_of_items = item2.number_of_items
			cost = item2.found_price

			#sqlobject = fruits(fruit = fruit, number_of_items = number_of_items, cost = cost)
			#sqlobject.save()

			context = {
				'last_fruit' : final_dictionaty_with_optimised_objects[item]
			}

	template = loader.get_template('fruitapptesco.html')
	return HttpResponse(template.render(context, request))




def ct9project(request):
    template = loader.get_template('CT9 blog.html')
    return HttpResponse(template.render(request))

def post_new(request):
	if request.method == 'POST':
		form = PostForm(request.POST)
		if form.is_valid():
			post = form.save(commit = False)
			post.author = request.user
			post.published_date = timezone.now()
			post.save()
			return redirect('post_list', pk=post.pk)
	else:
		form = PostForm()

	return render(request, 'post_edit.html', {'form': form})

def post_list(request):

	posts = ['hi', ' im brina', 'awangaw']
	context = {
	'posts' : posts
	}
	template = loader.get_template('base.html')
	return HttpResponse(template.render(context, request))

def detail(request, album_id):
	return HttpResponse("<h2>detail" + str(album_id) + '</h2>')


def album_link(request):
	all_albums = albums.objects.all()
	html = ''
	print all_albums
	for album in all_albums:
		url = '/music/' + str(album.id) + '/'
		html += '<a href="' + url + ' ">'+ album.artist + ' </a><br>'
	return HttpResponse(html)


def template_albums(request):
	all_albums = albums.objects.all()
	template = loader.get_template('template_albums.html')
	context = {
		'all_albums' : all_albums,
	}
	return HttpResponse(template.render(context,request) )


def favorite(request, album_id):
	album = album_id
	print album
	select_album = album.get(pk=request.POST['album'])
	select_album.is_favorite = True
	select_album.save()
	template = loader.get_template('template_albums.html')
	context = {
		'all_albums' : all_albums,
	}
	return HttpResponse(template.render(context,request) )





