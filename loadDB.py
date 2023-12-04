import sqlite3
import findLoc


def loadToliet():
    
    # my lat, my long load
    mylat, mylong = findLoc.findMyLocation()

    # sqlite connect 
    conn = sqlite3.connect("yeonsuToilet.db")
    
    # cursor 지정
    cursor = conn.cursor()

    # all_toilet 변수 지정 
    all_toilet = cursor.execute("select 화장실명,위도,경도 from data  where 위도 IS NOT null")
    all_toilet = all_toilet.fetchall()
    
    all_toilet = [list(element) for element in all_toilet]
    
    # top3 (가장 가까운 화장실 3곳) 지정
    query = "SELECT 화장실명,위도,경도\
            From data\
            where 위도 IS NOT null\
            ORDER BY (위도-{})*(위도-{}) + (경도-{})*(경도-{})\
            LIMIT 3;"\
        .format(mylat,mylat,mylong,mylong)
    
    try:
        # query 실행
        top3 = cursor.execute(query)
    
        # 결과 가져오기 --> list 형태
        top3 = top3.fetchall()
        top3 = [list(element) for element in top3]
        # 결과 출력
        # for row in top3:
        #     print(row)
        
    except sqlite3.Error as e:
        print("SQLite 에러 발생",e)
    
    
    # 연결해제
    conn.close()
    
    return top3, all_toilet


