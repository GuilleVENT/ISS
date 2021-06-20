import cartopy.crs as ccrs
import matplotlib.pyplot as plt


def plot_it(p_,iss_lat, iss_lon, user_lat,user_lon):
	iss_lat = float(iss_lat)
	iss_lon = float(iss_lon)

	ax = plt.axes(projection=ccrs.Mollweide())
	ax.stock_img()
	
	'''
	print(iss_lat,iss_lon)
	print(type(iss_lat),type(iss_lon))
	print(user_lat,user_lon)'''

	plt.plot([iss_lon], [iss_lat],
	     color='blue', linewidth=2, marker='o',
	     transform=ccrs.Geodetic(),
	     )

	plt.plot([user_lon], [user_lat],
	     color='green', linewidth=2, marker='x',
	     transform=ccrs.Geodetic(),
	     )

	plt.draw()
	
