// 0---- get token for admin

$.ajax({
    url: 'http://localhost:8000/api/login/',
    method: 'post',
    data: JSON.stringify({username: 'admin', password: 'admin'}),
    dataType: 'json',
    contentType: 'application/json',
    success: function(response, status){console.log(response);},
    error: function(response, status){console.log(response);}
});

localStorage.setItem('api_token', "781436916ba967e8f849a3c1265b854808222721");
api_token = localStorage.getItem('api_token');
// {token: "781436916ba967e8f849a3c1265b854808222721"} ==> my token for admin


// 1-----view all projects
$.ajax({
    url: 'http://localhost:8000/api/projects/',
    method: 'get',
    headers: {'Authorization': 'Token ' + api_token},
    dataType: 'json',
    success: function(response, status){console.log(response);},
    error: function(response, status){console.log(response);}
});


// 2-----view all tasks
$.ajax({
    url: 'http://localhost:8000/api/tasks/',
    method: 'get',
    headers: {'Authorization': 'Token ' + api_token},
    dataType: 'json',
    success: function(response, status){console.log(response);},
    error: function(response, status){console.log(response);}
});

// 3-----view all tasks in one project
$.ajax({
    url: 'http://localhost:8000/api/projects/2/',
    method: 'get',
    headers: {'Authorization': 'Token ' + api_token},
    dataType: 'json',
    success: function(response, status){console.log(response.project_tasks);},
    error: function(response, status){console.log(response);}
});


// 4------create task

let data = JSON.stringify({
    'summary': 'London Colney',
    'description': 'New manager needed',
    'status': 3,
    'type': 1,
    'project': 1,
    'created_by': 4,
    'assigned_to': 5
});

$.ajax({
    url: 'http://localhost:8000/api/tasks/',
    method: 'post',
    headers: {'Authorization': 'Token ' + api_token},
    data: data,
    dataType: 'json',
    contentType: 'application/json',
    success: function(response, status){console.log(response);},
    error: function(response, status){console.log(response);}
});

// 5-----delete task

$.ajax({
    url: 'http://localhost:8000/api/tasks/48/',
    method: 'delete',
    headers: {'Authorization': 'Token ' + api_token},
    dataType: 'json',
    contentType: 'application/json',
    success: function(response, status){console.log(response);},
    error: function(response, status){console.log(response);}
});
