// 1-----view all projects
$.ajax({
    url: 'http://localhost:8000/api/projects/',
    method: 'get',
    dataType: 'json',
    success: function(response, status){console.log(response);},
    error: function(response, status){console.log(response);}
});


// 2-----view all tasks
$.ajax({
    url: 'http://localhost:8000/api/tasks/',
    method: 'get',
    dataType: 'json',
    success: function(response, status){console.log(response);},
    error: function(response, status){console.log(response);}
});

// 3-----view all tasks in one project
$.ajax({
    url: 'http://localhost:8000/api/projects/2/',
    method: 'get',
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
    dataType: 'json',
    contentType: 'application/json',
    success: function(response, status){console.log(response);},
    error: function(response, status){console.log(response);}
});
