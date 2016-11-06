import re

			




class time_dignosis:
	def __init__ (self, time):
		self.time = time
		self.alaly()
		self.convert_to_military()

	def alaly(self):
		self.Part_of_day = re.search('(..$)', self.time)
		self.Part_of_day = self.Part_of_day.group()
		self.raw_time = self.time.replace(self.Part_of_day, '')
		self.segmented_time = self.raw_time.split(':')

	def convert_to_military(self):
		if (self.Part_of_day == 'PM') & (self.segmented_time[0] != '12'):
			self.segmented_time[0] = str(int(self.segmented_time[0])+12)
        
		if (self.Part_of_day == 'AM') & (self.segmented_time[0] == '12'):
			self.segmented_time[0] = '00'



first_ob = time_dignosis('12:40:00PM')



		

print first_ob.Part_of_day, first_ob.raw_time, first_ob.segmented_time, ':'.join(first_ob.segmented_time)






class time_dignosis:
	def __init__ (self, time):
		Part_of_day = re.search('(..$)', time)
		Part_of_day = m.group()
		raw_time = time.replace(Part_of_day, '')
		segmented_time = raw_time.split(':')


	def convert_to_military(self):
		if Part_of_day == 'PM':
			segmented_time[0] = str(int(segmented_time[0])+12)
		if (Part_of_day == 'AM') & (int(segmented_time[0]) == 12):
			segmented_time[0] == '00'