from django.urls import path
from webapp.views import IndexView, TaskView, TaskCreateView, TaskUpdateView, \
    TaskDeleteView, StatusesView, StatusCreateView, StatusUpdateView, StatusDeleteView, TypesView, TypeCreateView, \
    TypeUpdateView, TypeDeleteView, ProjectsView, ProjectView, ProjectCreateView, ProjectUpdateView, ProjectDeleteView

urlpatterns = [
    path('', ProjectsView.as_view(), name='index'),
    path('tasks/', IndexView),
    path('task/<int:pk>/', TaskView.as_view(), name='task_view'),
    path('task/add-project/<int:pk>/', TaskCreateView.as_view(), name='task_add'),
    path('task/<int:pk>/update/', TaskUpdateView.as_view(), name='task_update'),
    path('task/<int:pk>/delete/', TaskDeleteView.as_view(), name='task_delete'),
    path('status/', StatusesView.as_view(), name='statuses_view'),
    path('status/add/', StatusCreateView.as_view(), name='status_add'),
    path('status/<int:pk>/update/', StatusUpdateView.as_view(), name='status_update'),
    path('status/<int:pk>/delete/', StatusDeleteView.as_view(), name='status_delete'),
    path('type/', TypesView.as_view(), name='types_view'),
    path('type/add/', TypeCreateView.as_view(), name='type_add'),
    path('type/<int:pk>/update/', TypeUpdateView.as_view(), name='type_update'),
    path('type/<int:pk>/delete/', TypeDeleteView.as_view(), name='type_delete'),
    path('projects/', ProjectsView.as_view(), name='projects_view'),
    path('project/<int:pk>/', ProjectView.as_view(), name='project_view'),
    path('project/add/', ProjectCreateView.as_view(), name='project_add'),
    path('project/<int:pk>/update/', ProjectUpdateView.as_view(), name='project_update'),
    path('project/<int:pk>/delete/', ProjectDeleteView.as_view(), name='project_delete'),
]


app_name = 'webapp'