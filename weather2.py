from selenium import webdriver
import chromedriver_autoinstaller as chromedriver
import streamlit as st

#python -m streamlit run weather2.py

def scrape(loc):
	chromedriver.install()
	options = webdriver.ChromeOptions()
	options.add_experimental_option('excludeSwitches', ['enable-logging'])
	driver = webdriver.Chrome(options=options)


	driver.get("https://www.google.com/search?q="+loc+"+coordinates")
	haha = driver.find_element_by_class_name("Z0LcW")

	Coords = haha.text
	s = Coords.replace("°","")
	s = s.replace("N","")
	s = s.replace("W","")
	s = s.replace(",","")
	s = s.split()

	Coord1 = s[0]
	Coord2 = s[1]
	


	driver.get("https://forecast.weather.gov/MapClick.php?lat="+Coord1+"3&lon=-"+Coord2)

	day = []
	tempHigh = []
	tempLow = []
	Temperature = []
	total = []
	y=0
	z=1

	day = driver.find_elements_by_class_name("period-name")
	tempHigh = driver.find_elements_by_class_name("temp.temp-high")
	tempLow = driver.find_elements_by_class_name("temp.temp-low")

	for g in range(len(day)):
		day[g] = day[g].text

	for x in range(len(day)):
		if "Night" in day[x]:
			total.append(tempLow[z].text[5:])
			z+=1
		elif "night" in day[x]:
			total.append(tempLow[0].text[5:])
		else:
			total.append(tempHigh[y].text[6:])	
			y+=1

	driver.quit()
	print_Weather(total,day)

def print_Weather(Weather,Days):
	print(Days)
	print(len(Weather))
	for q in range(0,len(Weather),3):
		a  = int(Weather[q][:3])
		a2 = int(Weather[q+1][:3])
		a3 = int(Weather[q+2][:3])
		b  = int(Weather[q-1][:3])
		b2 = int(Weather[q-2][:3])
		
		col1,col2,col3 = st.columns(3)
		if q == 0:
			col1.metric(Days[q],Weather[q])
			col2.metric(Days[q+1],Weather[q+1])
		else:
			col1.metric(Days[q],Weather[q],str(a-b2)+"°F",delta_color="inverse")
			col2.metric(Days[q+1],Weather[q+1],str(a2-b)+"°F",delta_color="inverse")

		col3.metric(Days[q+2],Weather[q+2],str(a3-a)+"°F",delta_color="inverse")


form = st.form(key='frm1')
Loc = form.text_input('Enter a U.S. City: ')
submit = form.form_submit_button("What's the Weather?")

if submit:
	scrape(Loc)