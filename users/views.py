from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.shortcuts import render, redirect, reverse
from django.views.generic import View


class SignOutView(View):

    def get(self, request):
        logout(request)
        return redirect(reverse("core:main"))


class SignInView(View):

    def get(self, request):

        # next 있는지 확인.
        next = request.GET.get("next", None)

        if next:
            return render(request, "users/sign_in.html", {"next": next, })
        else:
            return render(request, "users/sign_in.html")

    def post(self, request):

        id = request.POST.get("id", "")
        pw = request.POST.get("pw", "")

        user = authenticate(self.request, username=id, password=pw)

        if user is not None:

            login(request, user)

            settings.SESSION_EXPIRE_AT_BROWSER_CLOSE = False    # 브라우저 종료해도 세션 유지
            settings.SESSION_COOKIE_AGE = 7 * 24 * 60 * 60    # 유지 기간 7일
            settings.SESSION_SAVE_EVERY_REQUEST = True          # 리퀘스트 오면 다시 7일 연장

            return JsonResponse({
                "result": True,
                "message": "로그인 성공",
            })
        else:
            return JsonResponse({
                "result": False,
                "message": "로그인 실패",
            })
