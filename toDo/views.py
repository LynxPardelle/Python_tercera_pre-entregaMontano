from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import ToDoList, ToDoCategory, ToDo
from .forms import CreateNewList, CreateNewCategory, CreateNewToDo
import json

# Create your views here.


def author(request):
    return HttpResponse("<p>This is app was made by <strong>Lynx Pardelle</strong>, you can watch my work on <a href='https://lynxpardelle.com' target='_blank' >lynxpardelle.com</a><p>")

# Create


def create_list(request, name):
    errStatus = 500
    try:
        if request.method == "GET":
            if ToDoList.objects.filter(name=name).exists():
                errStatus = 409
                raise Exception("TodoList already exist")
            else:
                if not name or name == "" or len(name) < 3:
                    errStatus = 400
                    raise Exception(
                        "TodoList name is required and need to be at least 3 characters")
                ToDoList.objects.create(name=name)
                todoList = ToDoList.objects.get(name=name)
                if not todoList:
                    errStatus = 404
                    raise Exception("TodoList not found")
                return JsonResponse({
                    'status': 200,
                    'statusMessage': 'Success',
                    'data': {
                        'id': todoList.id,
                        'name': todoList.name,
                    },
                    'message': "Success: TodoList with name %s created" % name,
                }, safe=False)
        else:
            errStatus = 405
            raise Exception("Method not allowed")
    except Exception as e:
        return JsonResponse({
            'status': errStatus,
            'statusMessage': 'Error',
            'data': {
                'method': request.method,
                'path': request.path,
                'body': request.body.decode('utf-8'),
                'headers': dict(request.headers),
            },
            'message': "Error: %s" % e}, safe=False)


def create_category(request):
    errStatus = 500
    try:
        if request.method == "POST":
            body = json.loads(request.body.decode('utf-8'))
            print(body)
            name = body.get('name')
            if not name:
                errStatus = 400
                raise Exception("ToDoCategory name is required")
            if ToDoCategory.objects.filter(name=name).exists():
                errStatus = 409
                raise Exception("ToDoCategory already exist")
            else:
                bg_color = body.get('bg_color') or "HASHffffff"
                text_color = body.get('text_color') or "HASH000000"
                bg_header_color = body.get(
                    'bg_header_color') or "HASH000000"
                title_color = body.get('title_color') or "HASHffffff"
                all_classes = body.get('all_classes') or ""
                header_classes = body.get('header_classes') or ""
                box_classes = body.get('box_classes') or ""
                ToDoCategory.objects.create(name=name, bg_color=bg_color, text_color=text_color, bg_header_color=bg_header_color,
                                            title_color=title_color, all_classes=all_classes, header_classes=header_classes, box_classes=box_classes)
                category = ToDoCategory.objects.get(name=name)
                if not category:
                    errStatus = 404
                    raise Exception("ToDoCategory not found")
                return JsonResponse({
                    'status': 200,
                    'statusMessage': 'Success',
                    'data': {
                        'id': category.id,
                        'name': category.name,
                        'bg_color': category.bg_color,
                        'text_color': category.text_color,
                        'bg_header_color': category.bg_header_color,
                        'title_color': category.title_color,
                        'all_classes': category.all_classes,
                        'header_classes': category.header_classes,
                        'box_classes': category.box_classes,
                    },
                    'message': "Success: ToDoCategory with name %s created" % name,
                }, safe=False)
        else:
            errStatus = 405
            raise Exception("Method not allowed")
    except Exception as e:
        print(e)
        print(request.body.decode('utf-8'))
        return JsonResponse({
            'status': errStatus,
            'statusMessage': 'Error',
            'data': {
                'method': request.method,
                'path': request.path,
                'body': request.body.decode('utf-8'),
                'headers': dict(request.headers),
            },
            'message': "Error: %s" % e}, safe=False)


def create_toDo(request, category_id, group_id):
    errStatus = 500
    try:
        if request.method == "POST":
            body = json.loads(request.body.decode('utf-8'))
            print(body)
            if not body.get('title'):
                errStatus = 400
                raise Exception("TodoList title is required")
            else:
                title = body.get('title')
                description = body.get('description') or ""
                priority = body.get('priority') or 999
                complete = body.get('complete') or False
                if not ToDoCategory.objects.filter(id=category_id).exists():
                    errStatus = 404
                    raise Exception("ToDoCategory not exist")
                elif not ToDoList.objects.filter(id=group_id).exists():
                    errStatus = 404
                    raise Exception("TodoList not exist")
                else:
                    ToDo.objects.create(group_id=group_id, category_id=category_id, title=title,
                                        description=description, priority=priority, complete=complete)
                    todo = ToDo.objects.get(title=title)
                    if not todo:
                        errStatus = 404
                        raise Exception("Todo not found")
                    group = ToDoList.objects.get(id=group_id)
                    category = ToDoCategory.objects.get(id=category_id)
                    return JsonResponse({
                        'status': 200,
                        'statusMessage': 'Success',
                        'data': {
                            'id': todo.id,
                            'title': todo.title,
                            'group': {
                                'id': group.id,
                                'name': group.name
                            },
                            'category': {
                                'id': category.id,
                                'name': category.name,
                                'bg_color': category.bg_color,
                                'text_color': category.text_color,
                                'bg_header_color': category.bg_header_color,
                                'title_color': category.title_color,
                                'all_classes': category.all_classes,
                                'header_classes': category.header_classes,
                                'box_classes': category.box_classes,
                            },
                            'description': todo.description,
                            'priority': todo.priority,
                            'complete': todo.complete,
                            'date': todo.date.strftime("%Y-%m-%d %H:%M:%S")
                        },
                        'message': "Success: Todo with title %s created" % title,
                    }, safe=False)
        else:
            errStatus = 405
            raise Exception("Method not allowed")
    except Exception as e:
        return JsonResponse({
            'status': errStatus,
            'statusMessage': 'Error',
            'data': {
                'method': request.method,
                'path': request.path,
                'body': request.body.decode('utf-8'),
                'headers': dict(request.headers),
            },
            'message': "Error: %s" % e}, safe=False)

# Read


def read_list(request, name):
    errStatus = 500
    try:
        if request.method == "GET":
            if ToDoList.objects.filter(name=name).exists():
                todoList = ToDoList.objects.get(name=name)
                if not todoList:
                    errStatus = 404
                    raise Exception("TodoList not found")
                todos = list(ToDo.objects.filter(
                    group_id=todoList.id).values())
                todos = list(map(lambda todo: {**todo, 'category': ToDoCategory.objects.get(
                    id=todo['category_id']), 'group': {'id': todoList.id, 'name': todoList.name}}, todos))
                return JsonResponse({
                    'status': 200,
                    'statusMessage': 'Success',
                    'data': {
                        'id': todoList.id,
                        'name': todoList.name,
                        'todos': todos,
                    },
                    'message': "Success: TodoList with name %s found" % name,
                }, safe=False)
            else:
                errStatus = 404
                raise Exception("TodoList with name %s not exist" % name)
        else:
            errStatus = 405
            raise Exception("Method not allowed")
    except Exception as e:
        return JsonResponse({
            'status': errStatus,
            'statusMessage': 'Error',
            'data': {
                'method': request.method,
                'path': request.path,
                'body': request.body.decode('utf-8'),
                'headers': dict(request.headers),
            },
            'message': "Error: %s" % e}, safe=False)


def read_category(request, id):
    errStatus = 500
    try:
        if request.method == "GET":
            if ToDoCategory.objects.filter(id=id).exists():
                category = ToDoCategory.objects.get(id=id)
                if not category:
                    errStatus = 404
                    raise Exception("ToDoCategory not found")
                return JsonResponse({
                    'status': 200,
                    'statusMessage': 'Success',
                    'data': {
                        'id': category.id,
                        'name': category.name,
                        'bg_color': category.bg_color,
                        'text_color': category.text_color,
                        'bg_header_color': category.bg_header_color,
                        'title_color': category.title_color,
                        'all_classes': category.all_classes,
                        'header_classes': category.header_classes,
                        'box_classes': category.box_classes,
                    },
                    'message': "Success: ToDoCategory with id %s found" % id,
                }, safe=False)
            else:
                errStatus = 404
                raise Exception("ToDoCategory with id %s not exist" % id)
        else:
            errStatus = 405
            raise Exception("Method not allowed")
    except Exception as e:
        return JsonResponse({
            'status': errStatus,
            'statusMessage': 'Error',
            'data': {
                'method': request.method,
                'path': request.path,
                'body': request.body.decode('utf-8'),
                'headers': dict(request.headers),
            },
            'message': "Error: %s" % e}, safe=False)


def read_todo(request, id):
    errStatus = 500
    try:
        if request.method == "GET":
            if ToDo.objects.filter(id=id).exists():
                todo = ToDo.objects.get(id=id)
                if not todo:
                    errStatus = 404
                    raise Exception("Todo not found")
                group = ToDoList.objects.get(id=todo.group_id)
                category = ToDoCategory.objects.get(id=todo.category_id)
                return JsonResponse({
                    'status': 200,
                    'statusMessage': 'Success',
                    'data': {
                        'id': todo.id,
                        'title': todo.title,
                        'group': {
                            'id': group.id,
                            'name': group.name
                        },
                        'category': {
                            'id': category.id,
                            'name': category.name,
                            'bg_color': category.bg_color,
                            'text_color': category.text_color,
                            'bg_header_color': category.bg_header_color,
                            'title_color': category.title_color,
                            'all_classes': category.all_classes,
                            'header_classes': category.header_classes,
                            'box_classes': category.box_classes,
                        },
                        'description': todo.description,
                        'priority': todo.priority,
                        'complete': todo.complete,
                        'date': todo.date.strftime("%Y-%m-%d %H:%M:%S")
                    },
                    'message': "Success: Todo with id %s found" % id,
                }, safe=False)
            else:
                errStatus = 404
                raise Exception("Todo with id %s not exist" % id)
        else:
            errStatus = 405
            raise Exception("Method not allowed")
    except Exception as e:
        return JsonResponse({
            'status': errStatus,
            'statusMessage': 'Error',
            'message': "Error: %s" % e}, safe=False)


def get_lists(request):
    errStatus = 500
    try:
        if request.method == "GET":
            lists = list(ToDoList.objects.values())
            if not lists or len(lists) == 0:
                errStatus = 404
                raise Exception("TodoLists not found")
            return JsonResponse({
                'status': 200,
                'statusMessage': 'Success',
                'data': lists,
                'message': "Success: TodoLists found",
            }, safe=False)
        else:
            errStatus = 405
            raise Exception("Method not allowed")
    except Exception as e:
        return JsonResponse({
            'status': errStatus,
            'statusMessage': 'Error',
            'data': {
                'method': request.method,
                'path': request.path,
                'body': request.body.decode('utf-8'),
                'headers': dict(request.headers),
            },
            'message': "Error: %s" % e}, safe=False)


def get_categories(request):
    errStatus = 500
    try:
        if request.method == "GET":
            categories = list(ToDoCategory.objects.values())
            if not categories or len(categories) == 0:
                errStatus = 404
                raise Exception("ToDoCategories not found")
            return JsonResponse({
                'status': 200,
                'statusMessage': 'Success',
                'data': categories,
                'message': "Success: ToDoCategories found",
            }, safe=False)
        else:
            errStatus = 405
            raise Exception("Method not allowed")
    except Exception as e:
        return JsonResponse({
            'status': errStatus,
            'statusMessage': 'Error',
            'data': {
                'method': request.method,
                'path': request.path,
                'body': request.body.decode('utf-8'),
                'headers': dict(request.headers),
            },
            'message': "Error: %s" % e}, safe=False)


def get_todos(request):
    errStatus = 500
    try:
        if request.method == "GET":
            category_id = request.GET.get('category_id')
            group_id = request.GET.get('group_id')
            todos = list(ToDo.objects.filter(category_id=category_id, group_id=group_id).values() if category_id and group_id else ToDo.objects.filter(
                category_id=category_id).values() if category_id else ToDo.objects.filter(group_id=group_id).values() if group_id else ToDo.objects.values())
            if not todos or len(todos) == 0:
                errStatus = 404
                raise Exception("Todos not found")
            todos = list(map(lambda todo: {**todo, 'category': ToDoCategory.objects.get(
                id=todo['category_id']), 'group': {'id': todo['group_id'], 'name': ToDoList.objects.get(id=todo['group_id']).name}}, todos))
            return JsonResponse({
                'status': 200,
                'statusMessage': 'Success',
                'data': todos,
                'message': "Success: Todos found",
            }, safe=False)
        else:
            errStatus = 405
            raise Exception("Method not allowed")
    except Exception as e:
        return JsonResponse({
            'status': errStatus,
            'statusMessage': 'Error',
            'message': "Error: %s" % e}, safe=False)


def show_lists(request):
    errStatus = 500
    try:
        if request.method == "GET":
            lists = list(ToDoList.objects.values())
            return render(request, 'toDoLists.html', {'lists': lists, 'form': CreateNewList()})
        else:
            errStatus = 405
            raise Exception("Method not allowed")
    except Exception as e:
        return render(request, 'error.html', {
            'status': errStatus,
            'statusMessage': 'Error',
            'data': {
                'method': request.method,
                'path': request.path,
                'body': request.body.decode('utf-8'),
                'headers': dict(request.headers),
            },
            'message': "Error: %s" % e})


def show_categories(request):
    errStatus = 500
    try:
        if request.method == "GET":
            categories = list(ToDoCategory.objects.values())
            return render(request, 'toDoCategories.html', {'categories': categories, 'form': CreateNewCategory()})
        else:
            errStatus = 405
            raise Exception("Method not allowed")
    except Exception as e:
        return render(request, 'error.html', {
            'status': errStatus,
            'statusMessage': 'Error',
            'data': {
                'method': request.method,
                'path': request.path,
                'body': request.body.decode('utf-8'),
                'headers': dict(request.headers),
            },
            'message': "Error: %s" % e})


def show_todos(request):
    errStatus = 500
    try:
        if request.method == "GET":
            category_id = request.GET.get('category_id')
            group_id = request.GET.get('group_id')
            todos = list(ToDo.objects.filter(category_id=category_id, group_id=group_id).values() if category_id and group_id else ToDo.objects.filter(
                category_id=category_id).values() if category_id else ToDo.objects.filter(group_id=group_id).values() if group_id else ToDo.objects.values())
            if not todos or len(todos) == 0:
                errStatus = 404
                raise Exception("Todos not found")
            todos = list(map(lambda todo: {**todo, 'category': ToDoCategory.objects.get(
                id=todo['category_id']), 'group': {'id': todo['group_id'], 'name': ToDoList.objects.get(id=todo['group_id']).name}}, todos))
            return render(request, 'toDos.html', {'todos': todos})
        else:
            errStatus = 405
            raise Exception("Method not allowed")
    except Exception as e:
        return render(request, 'error.html', {
            'status': errStatus,
            'statusMessage': 'Error',
            'data': {
                'method': request.method,
                'path': request.path,
                'body': request.body.decode('utf-8'),
                'headers': dict(request.headers),
            },
            'message': "Error: %s" % e})


def show_list(request, id):
    errStatus = 500
    try:
        if request.method == "GET":
            if ToDoList.objects.filter(id=id).exists():
                todoList = ToDoList.objects.get(id=id)
                print('todoList before edition:', todoList)
                print(todoList.id)
                todos = list(ToDo.objects.filter(
                    group_id=todoList.id).values())
                print('todos:')
                print(todos)
                if todos and len(todos) > 0:
                    todos = list(map(lambda todo: {**todo, 'category': ToDoCategory.objects.get(
                        id=todo['category_id']), 'group': {'id': todoList.id, 'name': todoList.name}}, todos))
                    print('todos after edition:')
                    print(todos)
                    todoList = {
                        'id': todoList.id,
                        'name': todoList.name,
                        'todos': todos
                    }
                    print('todoList edition:')
                print(todoList)
                return render(request, 'toDoList.html', {'list': todoList, 'form': CreateNewToDo()})
            else:
                return HttpResponse("Error: TodoList with id %s not exist" % id)
        else:
            errStatus = 405
            raise Exception("Method not allowed")
    except Exception as e:
        return render(request, 'error.html', {
            'status': errStatus,
            'statusMessage': 'Error',
            'data': {
                'method': request.method,
                'path': request.path,
                'body': request.body.decode('utf-8'),
                'headers': dict(request.headers),
            },
            'message': "Error: %s" % e})


def show_category(request, id):
    errStatus = 500
    try:
        if request.method == "GET":
            if ToDoCategory.objects.filter(id=id).exists():
                category = ToDoCategory.objects.get(id=id)
                print('category before edition:', category)
                print(category.id)
                todos = list(ToDo.objects.filter(
                    category_id=category.id).values())
                print('todos:')
                print(todos)
                if todos and len(todos) > 0:
                    todos = list(map(lambda todo: {**todo, 'category': ToDoCategory.objects.get(
                        id=todo['category_id']), 'group': {'id': todo['group_id'], 'name': ToDoList.objects.get(id=todo['group_id']).name}}, todos))
                    print('todos after edition:')
                    print(todos)
                    category = {
                        'id': category.id,
                        'name': category.name,
                        'bg_color': category.bg_color,
                        'text_color': category.text_color,
                        'bg_header_color': category.bg_header_color,
                        'title_color': category.title_color,
                        'all_classes': category.all_classes,
                        'header_classes': category.header_classes,
                        'box_classes': category.box_classes,
                        'todos': todos}
                    print('category edition:')
                print(category)
                return render(request, 'toDoCategory.html', {'category': category})
            else:
                return HttpResponse("Error: ToDoCategory with id %s not exist" % id)
        else:
            errStatus = 405
            raise Exception("Method not allowed")
    except Exception as e:
        return render(request, 'error.html', {
            'status': errStatus,
            'statusMessage': 'Error',
            'data': {
                'method': request.method,
                'path': request.path,
                'body': request.body.decode('utf-8'),
                'headers': dict(request.headers),
            },
            'message': "Error: %s" % e})


def show_toDo(request, id):
    errStatus = 500
    try:
        if request.method == "GET":
            if ToDo.objects.filter(id=id).exists():
                todo = ToDo.objects.get(id=id)
                todo = {
                    'id': todo.id,
                    'title': todo.title,
                    'description': todo.description,
                    'priority': todo.priority,
                    'date': todo.date.strftime("%Y-%m-%d %H:%M:%S"),
                    'complete': todo.complete,
                    'group_id': todo.group_id,
                    'category_id': todo.category_id
                }
                group = ToDoList.objects.get(id=todo['group_id'])
                category = ToDoCategory.objects.get(id=todo['category_id'])
                todo = {
                    'title': todo.get('title'),
                    'description': todo.get('description'),
                    'priority': todo.get('priority'),
                    'date': todo.get('date'),
                    'complete': todo.get('complete'),
                    'category': {
                        'id': category.id,
                        'name': category.name,
                        'bg_color': category.bg_color,
                        'text_color': category.text_color,
                        'bg_header_color': category.bg_header_color,
                        'title_color': category.title_color,
                        'all_classes': category.all_classes,
                        'header_classes': category.header_classes,
                        'box_classes': category.box_classes,
                    }, 'group': {
                        'id': group.id,
                        'name': group.name,
                    }}
                return render(request, 'toDo.html', {'todo': todo})
            else:
                errStatus = 404
                raise Exception("Todo with id %s not exist" % id)
        else:
            errStatus = 405
            raise Exception("Method not allowed")
    except Exception as e:
        return render(request, 'error.html', {
            'status': errStatus,
            'statusMessage': 'Error',
            'message': "Error: %s" % e})


# Update


def update_list(request, name, newName):
    errStatus = 500
    try:
        if request.method == "GET":
            if ToDoList.objects.filter(name=name).exists():
                if (ToDoList.objects.filter(name=newName).exists()):
                    errStatus = 409
                    raise Exception(
                        "TodoList with name %s already exist" % newName)
                else:
                    ToDoList.objects.filter(name=name).update(name=newName)
                    todoList = ToDoList.objects.get(name=newName)
                    if not todoList:
                        errStatus = 404
                        raise Exception("TodoList not found")
                    return JsonResponse({
                        'status': 200,
                        'statusMessage': 'Success',
                        'data': {
                            'id': todoList.id,
                            'name': todoList.name,
                        },
                        'message': "Success: TodoList with name %s updated to %s" % (name, newName),
                    }, safe=False)
            else:
                errStatus = 404
                raise Exception("TodoList with name %s not exist" % name)
        else:
            errStatus = 405
            raise Exception("Method not allowed")
    except Exception as e:
        return JsonResponse({
            'status': errStatus,
            'statusMessage': 'Error',
            'data': {
                'method': request.method,
                'path': request.path,
                'body': request.body.decode('utf-8'),
                'headers': dict(request.headers),
            },
            'message': "Error: %s" % e}, safe=False)


def update_category(request, id):
    errStatus = 500
    try:
        if request.method == "POST":
            if ToDoCategory.objects.filter(id=id).exists():
                if (ToDoCategory.objects.filter(name=name).exists()):
                    errStatus = 409
                    raise Exception(
                        "ToDoCategory with name %s already exist" % name)
                else:
                    body = json.loads(request.body.decode('utf-8'))
                    print(body)
                    oldCategory = ToDoCategory.objects.get(id=id)
                    name = body.get('name') or oldCategory.name or ""
                    bg_color = body.get(
                        'bg_color') or oldCategory.bg_color or "HASHffffff"
                    text_color = body.get(
                        'text_color') or oldCategory.text_color or "HASH000000"
                    bg_header_color = body.get(
                        'bg_header_color') or oldCategory.bg_header_color or "HASH000000"
                    title_color = body.get(
                        'title_color') or oldCategory.title_color or "HASHffffff"
                    all_classes = body.get(
                        'all_classes') or oldCategory.all_classes or ""
                    header_classes = body.get(
                        'header_classes') or oldCategory.header_classes or ""
                    box_classes = body.get(
                        'box_classes') or oldCategory.box_classes or ""
                    ToDoCategory.objects.filter(name=name).update(name=name, bg_color=bg_color, text_color=text_color, bg_header_color=bg_header_color,
                                                                  title_color=title_color, all_classes=all_classes, header_classes=header_classes, box_classes=box_classes)
                    category = ToDoCategory.objects.get(id=id)
                    if not category:
                        errStatus = 404
                        raise Exception("ToDoCategory not found")
                    return JsonResponse({
                        'status': 200,
                        'statusMessage': 'Success',
                        'data': {
                            'id': category.id,
                            'name': category.name,
                            'bg_color': category.bg_color,
                            'text_color': category.text_color,
                            'bg_header_color': category.bg_header_color,
                            'title_color': category.title_color,
                            'all_classes': category.all_classes,
                            'header_classes': category.header_classes,
                            'box_classes': category.box_classes,
                        },
                        'message': "Success: ToDoCategory with name %s updated to %s" % (name, name),
                    }, safe=False)
            else:
                errStatus = 404
                raise Exception("ToDoCategory with name %s not exist" % name)
        else:
            errStatus = 405
            raise Exception("Method not allowed")
    except Exception as e:
        return JsonResponse({
            'status': errStatus,
            'statusMessage': 'Error',
            'data': {
                'method': request.method,
                'path': request.path,
                'body': request.body.decode('utf-8'),
                'headers': dict(request.headers),
            },
            'message': "Error: %s" % e}, safe=False)


def update_toDo(request, id):
    errStatus = 500
    try:
        if request.method == "POST":
            if ToDo.objects.filter(id=id).exists():
                body = json.loads(request.body.decode('utf-8'))
                print(body)
                oldTodo = ToDo.objects.get(id=id)
                title = body.get('title') or oldTodo.title or ""
                description = body.get(
                    'description') or oldTodo.description or ""
                priority = body.get(
                    'priority') or oldTodo.priority or 999
                complete = body.get(
                    'complete') or oldTodo.complete or False
                ToDo.objects.filter(id=id).update(
                    title=title, description=description, priority=priority, complete=complete)
                todo = ToDo.objects.get(id=id)
                if not todo:
                    errStatus = 404
                    raise Exception("Todo not found")
                group = ToDoList.objects.get(id=todo.group_id)
                category = ToDoCategory.objects.get(id=todo.category_id)
                return JsonResponse({
                    'status': 200,
                    'statusMessage': 'Success',
                    'data': {
                        'id': todo.id,
                        'title': todo.title,
                        'group': {
                            'id': group.id,
                            'name': group.name
                        },
                        'category': {
                            'id': category.id,
                            'name': category.name,
                            'bg_color': category.bg_color,
                            'text_color': category.text_color,
                            'bg_header_color': category.bg_header_color,
                            'title_color': category.title_color,
                            'all_classes': category.all_classes,
                            'header_classes': category.header_classes,
                            'box_classes': category.box_classes,
                        },
                        'description': todo.description,
                        'priority': todo.priority,
                        'complete': todo.complete,
                        'date': todo.date.strftime("%Y-%m-%d %H:%M:%S")
                    },
                    'message': "Success: Todo with id %s updated" % id,
                }, safe=False)
            else:
                errStatus = 404
                raise Exception("Todo with id %s not exist" % id)
        else:
            errStatus = 405
            raise Exception("Method not allowed")
    except Exception as e:
        return JsonResponse({
            'status': errStatus,
            'statusMessage': 'Error',
            'data': {
                'method': request.method,
                'path': request.path,
                'body': request.body.decode('utf-8'),
                'headers': dict(request.headers),
            },
            'message': "Error: %s" % e}, safe=False)

# Delete


def delete_list(request, name):
    errStatus = 500
    try:
        if request.method == "GET":
            if ToDoList.objects.filter(name=name).exists():
                todoList = ToDoList.objects.get(name=name)
                ToDoList.objects.filter(name=name).delete()
                return JsonResponse({
                    'status': 200,
                    'statusMessage': 'Success',
                    'data': {
                        'id': todoList.id,
                        'name': todoList.name,
                    },
                    'message': "Success: TodoList with name %s deleted" % name,
                }, safe=False)
            else:
                errStatus = 404
                raise Exception("TodoList with name %s not exist" % name)
        else:
            errStatus = 405
            raise Exception("Method not allowed")
    except Exception as e:
        return JsonResponse({
            'status': errStatus,
            'statusMessage': 'Error',
            'data': {
                'method': request.method,
                'path': request.path,
                'body': request.body.decode('utf-8'),
                'headers': dict(request.headers),
            },
            'message': "Error: %s" % e}, safe=False)


def delete_category(request, id):
    errStatus = 500
    try:
        if request.method == "DELETE":
            if ToDoCategory.objects.filter(id=id).exists():
                category = ToDoCategory.objects.get(id=id)
                ToDoCategory.objects.filter(id=id).delete()
                return JsonResponse({
                    'status': 200,
                    'statusMessage': 'Success',
                    'data': {
                        'id': category.id,
                        'name': category.name,
                        'bg_color': category.bg_color,
                        'text_color': category.text_color,
                        'bg_header_color': category.bg_header_color,
                        'title_color': category.title_color,
                        'all_classes': category.all_classes,
                        'header_classes': category.header_classes,
                        'box_classes': category.box_classes,
                    },
                    'message': "Success: ToDoCategory with id %s deleted" % id,
                }, safe=False)
            else:
                errStatus = 404
                raise Exception("ToDoCategory with id %s not exist" % id)
        else:
            errStatus = 405
            raise Exception("Method not allowed")
    except Exception as e:
        return JsonResponse({
            'status': errStatus,
            'statusMessage': 'Error',
            'data': {
                'method': request.method,
                'path': request.path,
                'body': request.body.decode('utf-8'),
                'headers': dict(request.headers),
            },
            'message': "Error: %s" % e}, safe=False)


def delete_toDo(request, id):
    errStatus = 500
    try:
        if request.method == "DELETE":
            if ToDo.objects.filter(id=id).exists():
                todo = ToDo.objects.get(id=id)
                ToDo.objects.filter(id=id).delete()
                return JsonResponse({
                    'status': 200,
                    'statusMessage': 'Success',
                    'data': {
                        'id': todo.id,
                        'title': todo.title,
                        'group': {
                            'id': todo.group_id,
                            'name': ToDoList.objects.get(id=todo.group_id).name
                        },
                        'category': {
                            'id': todo.category_id,
                            'name': ToDoCategory.objects.get(id=todo.category_id).name,
                            'bg_color': ToDoCategory.objects.get(id=todo.category_id).bg_color,
                            'text_color': ToDoCategory.objects.get(id=todo.category_id).text_color,
                            'bg_header_color': ToDoCategory.objects.get(id=todo.category_id).bg_header_color,
                            'title_color': ToDoCategory.objects.get(id=todo.category_id).title_color,
                            'all_classes': ToDoCategory.objects.get(id=todo.category_id).all_classes,
                            'header_classes': ToDoCategory.objects.get(id=todo.category_id).header_classes,
                            'box_classes': ToDoCategory.objects.get(id=todo.category_id).box_classes,
                        },
                        'description': todo.description,
                        'priority': todo.priority,
                        'complete': todo.complete,
                        'date': todo.date.strftime("%Y-%m-%d %H:%M:%S")
                    },
                    'message': "Success: Todo with id %s deleted" % id,
                }, safe=False)
            else:
                errStatus = 404
                raise Exception("Todo with id %s not exist" % id)
        else:
            errStatus = 405
            raise Exception("Method not allowed")
    except Exception as e:
        return JsonResponse({
            'status': errStatus,
            'statusMessage': 'Error',
            'data': {
                'method': request.method,
                'path': request.path,
                'body': request.body.decode('utf-8'),
                'headers': dict(request.headers),
            },
            'message': "Error: %s" % e}, safe=False)
