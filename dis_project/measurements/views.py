from django.shortcuts import render,get_object_or_404
from .models import Measurements
from .forms import MeasurementModelForm
from geopy.geocoders import Nominatim
from measurements.utils import get_geo
from geopy.distance import geodesic
import folium

# Create your views here.
def calculate_dis_view(request):
    obj=get_object_or_404(Measurements,id=1)
    form = MeasurementModelForm(request.POST or None)
    geolocator=Nominatim(user_agent='measurements') 

    ip='72.14.207.99'
    country,city,lat,lon=get_geo(ip)
    # print('location country',country)
    # print('location city',city)
    # print('location lat lon',l_lat,l_lon)
    location=geolocator.geocode(city)
    # print(location)


    #location coordinate
    l_lat=lat
    l_lon=lon
    pointA=(l_lat,l_lon)
    #intial folium map
    m=folium.Map(width=800,height=500,location=pointA)
    #location marker
    folium.Marker([l_lat,l_lon],tooltip='click here for more',popup=city['city'],icon=folium.Icon(color='purple')).add_to(m)
   

    if form.is_valid():
        instance=form.save(commit=False)
        destination_=form.cleaned_data.get('destination')
        destination=geolocator.geocode(destination_)
        print(destination)

        #dest coordinate
        d_lat=destination.latitude
        d_lon=destination.longitude
        pointB = (d_lat,d_lon)
        distance=round(geodesic(pointA,pointB).km ,2)

    #folium map modification
        m=folium.Map(width=800,height=500,location=pointA)
    #location marker
        folium.Marker([l_lat,l_lon],tooltip='click here for more',popup=city['city'],icon=folium.Icon(color='purple')).add_to(m)
   
    #destination marker
        folium.Marker([d_lat,d_lon],tooltip='click here for more',popup=destination,icon=folium.Icon(color='red',icon='cloud')).add_to(m)
   


        instance.location=location
        instance.distance=distance
        instance.save()

    m=m._repr_html_()   
    
    
    context={
        'distance':obj,
        'form':form,
        'map':m
    }

    return render(request,'measurements/main.html',context)
