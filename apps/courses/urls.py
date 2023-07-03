from django.urls import path
from .views import (
    ManageCourseListView, CreateCourseView,
    UpdateCourseView, DeleteCourseView,
    CourseModuleUpdateView, ContentCreateUpdateView,
    ContentDeleteView, ModuleContentListView,
    ModuleOrderView, ContentOrderView, CourseListView, CourseDetailView
)

app_name = "courses"

urlpatterns = [
    path(
        '',
        CourseListView.as_view(),
        name='course_list'
    ),
    path(
        "mine/",
        ManageCourseListView.as_view(),
        name="manage_course_list"
    ),
    path(
        "create/",
        CreateCourseView.as_view(),
        name="create_course"
    ),
    path(
        "<pk>/edit/",
        UpdateCourseView.as_view(),
        name="edit_course"
    ),
    path(
        "<pk>/delete/",
        DeleteCourseView.as_view(),
        name="delete_course"
    ),
    path(
        '<pk>/module/',
        CourseModuleUpdateView.as_view(),
        name='course_module_update'
    ),
    path(
        'module/<int:module_id>/content/<model_name>/create/',
        ContentCreateUpdateView.as_view(),
        name='module_content_create'
    ),
    path(
        'module/<int:module_id>/content/<model_name>/<id>/',
        ContentCreateUpdateView.as_view(),
        name='module_content_update'
    ),
    path(
        'content/<int:id>/delete/',
        ContentDeleteView.as_view(),
        name='module_content_delete'
    ),
    path(
        'module/<int:module_id>/',
        ModuleContentListView.as_view(),
        name='module_content_list'
    ),
    path(
        'module/order/',
        ModuleOrderView.as_view(),
        name='module_order'
    ),
    path(
        'content/order/',
        ContentOrderView.as_view(),
        name='content_order'
    ),
    path(
        'subject/<slug:subject>/',
        CourseListView.as_view(),
        name='course_list_subject'
    ),
    path(
        '<slug:slug>/',
        CourseDetailView.as_view(),
        name='course_detail'
    ),
]
