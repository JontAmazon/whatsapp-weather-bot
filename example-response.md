# example response from "https://api.openweathermap.org/data/2.5/forecast"

dt: 1754956800
main:
	temp: 14.74
	feels_like: 14.38
	temp_min: 14.74
	temp_max: 14.74
	pressure: 1019
	sea_level: 1019
	grnd_level: 1015
	humidity: 81
	temp_kf: 0
weather:
	- id: 803
	  main: Clouds
	  description: broken clouds
	  icon: 04n
clouds:
	all: 68
wind:
	speed: 3.17
	deg: 245
	gust: 6.3
visibility: 10000
pop: 0
sys:
	pod: n
dt_txt: 2025-08-12 00:00:00
rain:
	3h: 0.26

^ note: the key "rain" is not present at all when it's not raining...


