(function()
{
	var app=angular.module("course-pagenation-app",[]);

	app.controller("course-pagenation-controller",function($scope,$http)
	{
		$http({
			method : 'GET',
			url : '/'
		})	
	});
})();
