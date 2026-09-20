from django.shortcuts import render


def home(request):
    """Отображает главную страницу каталога."""
    return render(request, "catalog/home.html")


def contacts(request):
    """Отображает страницу контактов и принимает форму."""
    context = {"success": False}

    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")

        print("Получены данные формы:", flush=True)
        print(f"Имя: {name}", flush=True)
        print(f"Телефон: {phone}", flush=True)
        print(f"Сообщение: {message}", flush=True)

        context["success"] = True

    return render(request, "catalog/contacts.html", context)
