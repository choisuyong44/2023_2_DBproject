import pandas as pd
import folium
import findLoc

# db를 불러와서 전체 화장실과 가장 가까운 3곳 고르기
import loadDB

def showToiletMap():
    lat, long = findLoc.findMyLocation()
    center = [lat,long]
    m = folium.Map(location=center, zoom_start=18)
    top3, all_toilet = loadDB.loadToliet()

    # folim에서 위치를 표시해주는 marker
    from folium import Marker
    
    # sqlite에서 받아올 때 tuple로 받아옴. -> list로 변경
    # 현재 위치를 표기
    Marker(location=[lat,long],
           popup="현 위치",
           icon=folium.Icon(color='green')).add_to(m)
    
    # 모든 주소를 표기
    for row in all_toilet:
        Marker(location = [float(row[1]), float(row[2])],
            popup=row[0],
            icon=folium.Icon(color='blue')
            ).add_to(m)
    
    # best 3 를 표기
    for row in top3:
        Marker(location = [float(row[1]), float(row[2])],
            popup=row[0],
            icon=folium.Icon(color='red',icon="star")
            ).add_to(m)
        
    # best 3와 현재 위치를 잇는 직선
    lat = float(lat)
    long = float(long)
    print([lat,long])
    location_line1 = [ [top3[0][1],top3[0][2]], [lat,long]]
    location_line2 = [ [top3[1][1],top3[1][2]], [lat,long]]
    location_line3 = [ [top3[2][1],top3[2][2]], [lat,long]]
    
    folium.PolyLine(locations=location_line1,tooltip='Polyline',popup="가장 가까운 화장실").add_to(m)
    folium.PolyLine(locations=location_line2,tooltip='Polyline',popup="두 번째로 가까운 화장실").add_to(m)
    folium.PolyLine(locations=location_line3,tooltip='Polyline',popup="세 번째로 가까운 화장실").add_to(m)
        
    m.save("templates/my_map.html")
    
