from django.shortcuts import render

# Create your views here.
"""
DB 백업 하는 방법 

1. 인터넷에서 django-dbbackup 검색해서 찾는다.
(그전에 무슨 파일인지 알면 그냥 pip로 sudo pip django-dbbackup 치면 될듯??(오타 일수도 있으니 인터넷 확인바람))
2. django db setting 한다.(이건 원래 django framework 세팅과 똑같으니 똑같이 하면 됨)
3. local에서 개발할 경우에는 바로 python manage.py dbbackup 치면 backup이 됨
3-1. 만약 aws에서 하는 경우 mysql.sock파일을 현재 localhost에서 인식하는 곳으로 옮긴다.
3-2. 그리고 나서 mysql에서 unix socket을 현 localhost위치로 바꾼다.(바꾸는 방법은 인터넷 참조)
3-3. 3에서와 같이 하면 db backup이 된다.
4. 그리고 db를 restore하고싶으면 그냥 python manage.py dbrestore 치면 그 폴더상에 db backup파일이 있으면 알아서 찾아서 한다.
-끝-  
"""
