from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework import status
from .models import *
from accounts.models import CustomUser


# Create your views here.


class ChatList(TemplateView):

    def post(self, request, **kwargs):
        chat_id = kwargs.get("chat_id")
        print("chat_id: " + chat_id)
        text = request.POST["text"]
        print("text: " + text)

        try:
            # MyUser = CustomUser.objects
            print(self.request.user)
            chm = ChatMessage()
            chm.Text = text
            chm.Tarikh = datetime.now()
            chm.RelatedChat = Chat.objects.filter(Q(id=chat_id)).get()
            chm.Sender = self.request.user
            # chm.Attachments @TODO: save file
            chm.save()
            return HttpResponse("saved", status.HTTP_200_OK)

        except NameError:
            print(NameError)
            return HttpResponse(NameError, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, **kwargs):

        chat_id = kwargs.get("chat_id")
        show_messages = "ChatListPage"
        username = ""
        all_messages = []
        if chat_id is not None:
            all_messages = ChatMessage.objects.filter(Q(RelatedChat_id=chat_id)).order_by("Tarikh")
            show_messages = "SingleChatPage"
            for am in all_messages:
                am.Tarikh = self.time_diff(am.Tarikh)
        for_mobile = True
        login_detail = None

        if request.method == 'GET' and 'password' in request.GET and 'username' in request.GET:
            username = request.GET['username']
            password = request.GET['password']
            if password is not None and password != '':
                for_mobile = True
                from django.contrib.auth import authenticate
                login_detail = authenticate(username=username, password=password)
        elif self.request.session.get('for_mobile') is True:
            for_mobile = True
        else:
            for_mobile = False
            username = self.request.user.username

        if login_detail is None:
            if CustomUser.objects.filter(username=username):
                user_response = 'password is incorrect'
            else:
                user_response = 'username is incorrect'
        else:
            from django.contrib.auth import authenticate, login
            login(request, login_detail)
            user_response = login_detail

        if not self.request.user.is_authenticated:
            return HttpResponseRedirect('../signin')

        chat_list_all = Chat.objects.filter(Q(User1=self.request.user) | Q(User2=self.request.user))
        chat_list = []

        for C in chat_list_all:

            if C.User1 == self.request.user:
                to_user = C.User2
            else:
                to_user = C.User1

            avatar_url = ""
            print(to_user.avatar)
            if to_user.avatar is not None:
                avatar_url = to_user.avatar

            chat_list.append({
                "id": C.id,
                "title": C.__str__(),
                "name": to_user.first_name + " " + to_user.last_name,
                "username": to_user.username,
                "avatar": avatar_url,
                "lead": C.Lead,
                "zaman": self.time_diff(C.Zaman),
            })

        self.request.session.update({"for_mobile": for_mobile})

        context = {
            'ShowMessages': show_messages,
            'ForMobile': for_mobile,
            'ChatList': chat_list,
            'UserDetail': user_response,
            'Messages': all_messages,
        }

        return render(request, 'Chat.html', context)

    @staticmethod
    def time_diff(your_time, date_format="%Y-%m-%d %H:%M:%S.%f"):

        try:
            a = datetime.strptime(str(datetime.now()), date_format)
            b = datetime.strptime(str(your_time), date_format)
            delta = a - b
            if delta.days > 0:
                time = delta.days
                if time == 1:
                    time = ""
                    pasvande_time = " دیروز "
                elif time == 2:
                    time = ""
                    pasvande_time = " پریروز "
                else:
                    pasvande_time = " روز پیش "
                    time = delta.days

            elif delta.seconds < 60:
                time = delta.seconds
                pasvande_time = " ثانیه پیش "
            elif delta.seconds < 3600:
                time = int(delta.seconds / 60)
                pasvande_time = " دقیقه پیش "
            elif delta.seconds < 86400:
                time = int(delta.seconds / 3600)
                pasvande_time = " ساعت پیش "
            else:
                time = b
                pasvande_time = " "

            return str(time) + pasvande_time

        except NameError:
            print(NameError)
            try:
                return datetime.strptime(str(your_time), date_format)
            except:
                return your_time


class CreateNewChat(TemplateView):

    def get(self, request, **kwargs):
        my_slug = kwargs.get("my_slug")
        to_slug = kwargs.get("to_slug")

        my_user = CustomUser.objects.filter(username=my_slug)
        to_user = CustomUser.objects.filter(username=to_slug)

        print("Chat From: " + my_slug + " to: " + to_slug)

        our_chat = Chat.objects.filter(
            (Q(User1__username=my_slug) and Q(User2__username=to_slug))
            or
            (Q(User1__username=to_slug) and Q(User2__username=my_slug))
        )

        if our_chat.count() == 0:
            new_chat_id = Chat.objects.create(
                User1_id=my_user.get().id,
                User2_id=to_user.get().id,
                Zaman=datetime.now(),
                Lead="..."
            )

            print(new_chat_id)
            print(new_chat_id.id)
            print("Chat Created")

            # ch = Chat()
            # ch.User1 = my_user
            # ch.User2 = to_user
            # ch.Zaman = datetime.now()
            # ch.Lead = "..."
            # print_chat = ch.save()
            #
            # print(print_chat)
            # print(ch.User1)
            # print(ch.User2)
            # print("Chat 2 Created")

            our_chat = Chat.objects.filter(
                (Q(User1__username=my_slug) and Q(User2__username=to_slug))
                or
                (Q(User1__username=to_slug) and Q(User2__username=my_slug))
            )

        new_chat_id = our_chat.get()

        print(new_chat_id.encode("utf-8"))
        print(new_chat_id.id.encode("utf-8"))

        return HttpResponseRedirect('../../chat/' + str(new_chat_id.id))

        # return render(request, 'Chat.html')
