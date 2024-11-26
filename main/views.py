from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from .models import User, Project, Task
from .serializer import (
    Registration,
    Login,
    UserSerializeer,
    ProjectSerializer,
    TaskSerializer,
)

# -------------------------------------------------------------------------------------
# USERS


@api_view(["POST"])
def sign_up_user(request):
    """
    Регистрация нового пользователя.

    Параметры:
    - request (HttpRequest): Объект запроса, содержащий данные пользователя для регистрации.

    Возвращает:
    - Response: Объект ответа с токеном пользователя и статусом 201 (Создано) при успешной регистрации.
    """
    serializer = Registration(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    token = Token.objects.create(user=user)
    return Response({"data": {"user_token": token.key}},
                        status=status.HTTP_201_CREATED)


@api_view(["POST"])
def log_in_user(request):
    """
    Аутентификация пользователя.

    Параметры:
    - request (HttpRequest): Объект запроса, содержащий данные для входа (логин и пароль).

    Возвращает:
    - Response: Объект ответа с токеном пользователя и статусом 200 (Успешно) при успешной аутентификации.
    - Response: Объект ответа с ошибкой и статусом 401 (Неавторизован) или 422 (Ошибка валидации) при неудаче.
    """
    serializer = Login(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data["user"]
        if not user:
            return Response(
                {
                    "error": {
                        "code": status.HTTP_401_UNAUTHORIZED,
                        "message": "Authentication failed",
                    }
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )
        token, created = Token.objects.get_or_create(user=user)
        return Response({"data": {"user_token": token.key}},
                            status=status.HTTP_200_OK)
    return Response(
        {
            "error": {
                "code": status.HTTP_422_UNPROCESSABLE_ENTITY,
                "message": "Validation error",
            }
        },
        status=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )


@api_view(["POST"])
def log_out_user(request):
    """
    Выход пользователя из системы.

    Параметры:
    - request (HttpRequest): Объект запроса.

    Возвращает:
    - Response: Объект ответа с сообщением об успешном выходе и статусом 200 (Успешно).
    - Response: Объект ответа с ошибкой и статусом 403 (Запрещено) при неудаче.
    """
    if not request.user.is_active:
        return Response(
            {"error": {"code": status.HTTP_403_FORBIDDEN,
                        "message": "Login failed"}},
                    status=status.HTTP_403_FORBIDDEN,)
    request.user.auth_token.delete()
    return Response(
        {"data": {"message": "log out successfully"}},
            status=status.HTTP_200_OK)


@api_view(["GET"])
def user_list(request):
    """
    Получение списка всех пользователей.

    Параметры:
    - request (HttpRequest): Объект запроса.

    Возвращает:
    - JsonResponse: Объект ответа с данными пользователей и статусом 200 (Успешно).
    """
    if request.method == "GET":
        users = User.objects.all()
        serializer = UserSerializeer(users, many=True)
        return JsonResponse(serializer.data, safe=False,
                                status=status.HTTP_200_OK)


# -------------------------------------------------------------------------------------
# PROJECTS


@api_view(["GET", "POST"])
def project_list(request):
    """
    Получение списка всех проектов или создание нового проекта.

    Параметры:
    - request (HttpRequest): Объект запроса, содержащий данные для создания нового проекта (при POST-запросе).

    Возвращает:
    - JsonResponse: Объект ответа с данными всех проектов и статусом 200 (Успешно) при GET-запросе.
    - Response: Объект ответа с данными нового проекта и статусом 201 (Создано) при успешном POST-запросе.
    """
    if request.method == "GET":
        project = Project.objects.all()
        serializer = ProjectSerializer(project, many=True)
        return JsonResponse(serializer.data, safe=False,
                                status=status.HTTP_200_OK)
    elif request.method == "POST":
        serializer = ProjectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["PATCH", "DELETE", "GET"])
def update_project(request, pk: int):
    """
    Получение, обновление или удаление проекта по его идентификатору.

    Параметры:
    - request (HttpRequest): Объект запроса.
    - pk (int): Идентификатор проекта, который нужно обновить или удалить.

    Возвращает:
    - JsonResponse: Объект ответа с данными проекта и статусом 200 (Успешно) при GET-запросе.
    - Response: Объект ответа с обновленными данными проекта и статусом 200 (Успешно) при успешном PATCH-запросе.
    - Response: Объект ответа с пустым содержимым и статусом 204 (Нет содержимого) при успешном DELETE-запросе.
    - Response: Объект ответа с ошибкой 404 (Не найдено), если проект с указанным идентификатором не существует.
    """
    project = get_object_or_404(Project, id=pk)
    if request.method == "GET":
        serializer = ProjectSerializer(project)
        return JsonResponse(serializer.data, safe=False,
                                status=status.HTTP_200_OK)
    elif request.method == "PATCH":
        serializer = ProjectSerializer(project, data=request.data,
                                        partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == "DELETE":
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# -------------------------------------------------------------------------------------
# TASK


@api_view(["GET", "POST"])
def task_list(request):
    """
    Получение списка всех задач или создание новой задачи.

    Параметры:
    - request (HttpRequest): Объект запроса, содержащий данные для создания новой задачи (при POST-запросе).

    Возвращает:
    - JsonResponse: Объект ответа с данными всех задач и статусом 200 (Успешно) при GET-запросе.
    - Response: Объект ответа с данными новой задачи и статусом 201 (Создано) при успешном POST-запросе.
    """
    if request.method == "GET":
        task = Task.objects.all()
        serializer = TaskSerializer(task, many=True)
        return JsonResponse(serializer.data, safe=False,
                                status=status.HTTP_200_OK)
    elif request.method == "POST":
        serializer = TaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["PATCH", "DELETE", "GET"])
def update_task(request, pk: int):
    """
    Получение, обновление или удаление задачи по её идентификатору.

    Параметры:
    - request (HttpRequest): Объект запроса.
    - pk (int): Идентификатор задачи, которую нужно обновить или удалить.

    Возвращает:
    - JsonResponse: Объект ответа с данными задачи и статусом 200 (Успешно) при GET-запросе.
    - Response: Объект ответа с обновленными данными задачи и статусом 200 (Успешно) при успешном PATCH-запросе.
    - Response: Объект ответа с пустым содержимым и статусом 204 (Нет содержимого) при успешном DELETE-запросе.
    - Response: Объект ответа с ошибкой 404 (Не найдено), если задача с указанным идентификатором не существует.
    """
    task = get_object_or_404(Task, id=pk)
    if request.method == "GET":
        serializer = TaskSerializer(task)
        return JsonResponse(serializer.data,
                                safe=False, status=status.HTTP_200_OK)
    elif request.method == "PATCH":
        serializer = TaskSerializer(task, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == "DELETE":
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
