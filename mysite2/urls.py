from django.conf.urls import  include, url

from rest_framework import routers
router = routers.DefaultRouter()
from django.contrib import admin
urlpatterns = [
	url(r'^admin/',include(admin.site.urls)),
	url(r'^api/', include(router.urls)),
	
    url(r'^api/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^',include('login.urls',namespace="login")),
	url(r'^',include('index.urls',namespace="index")),
	url(r'^',include('course.urls',namespace="course")),
	url(r'^',include('recommend.urls',namespace="recommend")),
	url(r'^',include('sugangpage.urls',namespace="sugangpage")),
	url(r'^',include('mypage.urls',namespace='mypage')),
	url(r'^',include('lecture.urls',namespace='lecture')),

	
]
# urlpatterns = patterns('',
#     # Examples:
#     # url(r'^$', 'mysite2.views.home', name='home'),
#     # url(r'^blog/', include('blog.urls')),
#     url(r'^admin/', include(admin.site.urls)), 
# 	url(r'^update/$','lecture.views.lec_update'),
# 	url(r'^DBUpdate/$','lecture.views.UpdateLogin'),
# 	url(r'^CurUpdate/$','lecture.views.AutoFastLecUpdate'),
# 	url(r'^upload/$','course.views.UploadFile'),
# 	url(r'^download/','course.views.download'),
# 	url(r'^sugangchange/','sugangpage.views.sugangpage'),
# 	url(r'^suganginsert/','sugangpage.views.sugangpageWrite'),

# 	url(r'^sugangdelete/','sugangpage.views.sugangpageDelete'),
	
# )

# urlpatterns += patterns('mycourse.views',
# 	url(r'^MyCourse/$','MyCourse'),
# 	url(r'^MyCoursePage/$','MyCoursePageNation'),
# 	url(r'^MyCourseDelete/$','CourseDelete'),
# 	url(r'^UpdateCourse/$','UpdateRedirect'),
# 	url(r'^UpdateWrite/$','CourseUpdate'),
# 	url(r'^LikeCourseDelete/$', 'LikeDelete')
# 	)

# urlpatterns += patterns('schedule.views',
# 	url(r'^sel_period/(?P<period>\w+)/(?P<page>\d+)/$', 'SelectPeriod'),
# 	#url(r'^Schedule/Search/$','SearchSubject'),
# 	url(r'^Schedule/$','SearchSubject'),
# 	url(r'^Sel_lecture/$','SelectLecture'),
# 	url(r'^Sel_periodLecture/$','SearchSelectPeriod'),
# 	url(r'^Remove_lecture/$','RemoveLecture'),
# 	)#schedule view

# urlpatterns += patterns('login.views',
# 	url(r'^Confirm/$','Confirm'),
# 	url(r'^HisnetCeck/$','HisnetCheck'),
# 	url(r'^Register/$','Register'),
# 	url(r'^RegisterInfo/$','RegisterInfo'),
# 	url(r'^$', 'loginCheck'),
# 	url(r'^Logout/$', 'logout_page'),
# 	url(r'^static','static_forbidden')
# 	)#login view

# urlpatterns += patterns('index.views',
# 	url(r'^Search/$', 'Search'),
# 	url(r'^SearchPage/$','SearchPage'),
# 	url(r'^MyPage/$', 'MyPage'), 
# 	url(r'^About/$','About'),
	
# 	url(r'^Judgement/$','Judgement'),
# 	url(r'^Page/$','Page'),
# 	url(r'^SubScript/$','SubScript'),
# 	url(r'^SiteMap/$','SiteMap'),
# 	url(r'^FirstPage/$','Page'),
# 	url(r'^SecondPage/$','Page'),
# 	url(r'^ThirdPage/$','Page'),
# 	url(r'^Select_Course/$','Page'),
# 	url(r'^Select_Professor/$','Page'),
# 	url(r'^Category_Change/','new_category_system'),
# 	url(r'^Category_Subject_Change/','select_subject_list'),
# 	url(r'^Category_Search/','search_subject_list'),
# 	url(r'^SubjectSearchPage/','search_subject_page'),
# 	url(r'^LikeSugangPage/','Page'),
# 	url(r'^TotalDBCountUpdate/','GroupTotalCountRenew'),
# 	url(r'^RenewDB/','renewDB'),
# 	url(r'^RenewCount/','renewTableCount'),
# 	url(r'^EVENT/','ShowEvent')
# )#mainPage view

# urlpatterns += patterns('mypage.views',
# 	url(r'^MyPage/NicknameChange/$', 'NicknameChange'),
# 	url(r'^MyPage/StudentInformation_Update/$','Student_Information_Change')
# )#mypage view

# urlpatterns += patterns('recommend.views',
# 	#url(r'^Recommend/$','Recommend'),
# 	url(r'^Recommend/$','newRecommend'),
# 	#url(r'^Recommend/(\d+)$','Recommend'),
# 	url(r'^Recommend/Recommend_Write$','Recommend_Write'),
# 	#url(r'^Like/$','Like'),
# 	url(r'^NotEmptyRecommend/$','Recommend_NotEmpty'),
# 	url(r'^course-data/$','CourseList'),
# 	url(r'^Course-Semester/$','CourseSelect')


# )#recommend view

# urlpatterns += patterns('qna.views',
# 	url(r'^QnA/Page/','QnA'),
# 	url(r'^QnA/$','QnAMain'),
# 	url(r'^QnA/Write$','QnAWrite'),
# 	url(r'^QnA/Writing$','QnA_Writing'),
# 	url(r'^QnA/(\d+)/$','QnARead'),
# 	url(r'^QnA/Reply/(\d+)$','QnA_Reply'),
# 	url(r'^QnA/Replying/(\d+)$','QnA_Replying'),
# 	url(r'^SubScriptWrite/$','Improvement_Write'),
# 	url(r'^Judgement_Write/$','Judgement_Write'),

# )

# urlpatterns += patterns('course.views',
# 	#url(r'^Course/(\d+)$','Course'),
# 	url(r'^CoursePageNation/(\d+)$','CoursePage'),
# 	url(r'^CourseProfessor/(\d+)$','CourseProfessor'),
# 	#url(r'^Course/Period(\d+)$','PeriodCourse'),
# #	url(r'^CoursePageNation/(\w+)$','PeriodCoursePage')
# ) # course view

# urlpatterns += patterns('notice.views',
# 	url(r'^Notice/$','NoticeMain'),
# 	url(r'^Notice/Page/','Notice'),
# 	url(r'^Notice/(\d+)/$','Notice_Read'),
# 	url(r'^Notice/Write$', 'Notice_Write'),
# 	url(r'^Notice/Writing$', 'Notice_Writing'),

# )#Notice view