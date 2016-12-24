import sqlite3
import pandas as pd
import numpy as np
from numpy.random import normal
import re
import matplotlib.pyplot as plt

##just a comitt


conn = sqlite3.connect('database.sqlite')

c = conn.cursor()



player_fifa_api_id = []
player_fifa_id2 = c.execute("SELECT player_fifa_api_id FROM Player")
ids2 = player_fifa_id2.fetchall()[0:10]
for id_fifa in ids2:
	id_fifa = re.findall(r"[0-9]+", str(id_fifa))[0]
	player_fifa_api_id.append(id_fifa)
	#id_fifa = Playa(id_fifa)
	#player_objects.append(id_fifa)





player_name_list = []
overall_rating_list = []
for item in player_fifa_api_id:
	player_name = c.execute("SELECT player_name FROM Player Where player_fifa_api_id =" + item)
	name_temp = player_name.fetchone()
	name_temp = str(re.findall(r"([a-z,A-Z]+)", str(name_temp))[1] +" " +re.findall(r"([a-z,A-Z]+)", str(name_temp))[2])
	player_name_list.append(name_temp)
	overall_rating = (c.execute("SELECT overall_rating FROM Player_Attributes Where player_fifa_api_id =" + item)).fetchone()
	overall_rating = re.findall(r"[0-9]+" , str(overall_rating))[0]
	print len(overall_rating_list)
	overall_rating_list.append(overall_rating)



	#item.setName(name_temp)




numpy_player_id =  np.array(player_fifa_api_id)
numpy_player_name = np.array(player_name_list)
numpy_overall_rating = np.array(overall_rating_list).astype(np.float)



list_ = np.array([numpy_player_id , numpy_player_name, numpy_overall_rating]).T



Player_table = pd.DataFrame(data = list_, index = range(0,len(numpy_player_id)), columns=['player_fifa_api_id', 'player_name', 'overall_rating'])


#a=  Player_table['player_name'].mean()

#print Player_table['overall_rating']


# print Player_table['overall_rating']

plt.hist(np.array(Player_table['overall_rating']).astype(np.float), bins=30)

print Player_table.loc[Player_table['overall_rating'] == 70]




plt.show()

