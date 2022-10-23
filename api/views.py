from datetime import datetime
import city.models
import main.models
from events.models import Events
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


# Create your views here.


class ApiSaveCityNote(APIView):

    def post(self, request, format=None):
        print(format)
        try:
            pid = self.request.POST['city']
            note = self.request.POST['text']
            print(pid)
            print(note)
            city.models.CityProject.objects.filter(slug=pid).update(note=note)
            register_event(self, pid, "ثبت یادداشت شهر",
                           "متن " + note + "به عنوان یادداشت جدید برای شهر " + pid + " ثبت شد. ")
            return Response({"response": "ok"}, status=status.HTTP_200_OK)
        except NameError:
            print(NameError)
            return Response({"response": NameError}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, format=None):
        try:
            projects_data = []
            all_projects = city.models.CityProject.objects.all()
            for pd in all_projects:
                projects_data.append({
                    'id': pd.id,
                    'city': pd.city,
                    'slug': pd.slug,
                    'miangin_pishraft': pd.miangin_pishraft,
                    'view_count': pd.view_count,
                    'note': pd.note,
                })

            return Response({"response": projects_data}, status=status.HTTP_200_OK)
        except NameError:
            return Response({"response": "error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ApiUpdateProject(APIView):

    def post(self, request, format=None):
        try:
            pid = self.request.POST['project']
            print(pid)
            if "note" in self.request.POST:
                note = self.request.POST['note']
                print(note)
                main.models.Project.objects.filter(id=pid).update(note=note)
                register_event(self, pid, "ثبت یادداشت پروژه", "متن " + note +
                               "به عنوان یادداشت جدید برای پروژه " + pid + " ثبت شد. ")
            elif "desc" in self.request.POST:
                text = self.request.POST['desc']
                level = self.request.POST['level']
                print(pid + ": " + level + ": " + text)
                lookup = "marhale%s" % level
                main.models.Project.objects.filter(id=pid).update(**{lookup: text})
                register_event(self, pid, "تغییر توضیحات مرحله", "ثبت " + text + "به عنوان توضیحات جدید مرحله " + level)

            elif "level" in self.request.POST:
                text = self.request.POST['text']
                level = self.request.POST['level']
                print(pid + ": " + level + ": " + text)
                lookup = "marhale%saccomplished" % level
                p = main.models.Project.objects.filter(id=pid)
                p.update(**{lookup: text})
                p.get().save()
                register_event(self, pid, "تغییر وضعیت مرحله",
                               "ثبت " + text + "به عنوان میزان کارکرد جدید مرحله " + level)

            return Response({"response": "ok"}, status=status.HTTP_200_OK)
        except NameError:
            return Response({"response": NameError.args}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, format=None):
        try:
            projects_data = []
            all_projects = main.models.Project.objects.all()
            for pd in all_projects:
                projects_data.append({
                    'id': pd.id,
                    'title': pd.title,
                    'slug': pd.slug,
                    'photo': pd.photo.url,
                    'city': pd.city,
                    'location': pd.location,
                    'miangin_pishraft': pd.miangin_pishraft,
                    'date_start': str(pd.date_start.year) + "/" + str(pd.date_start.month) + "/" + str(
                        pd.date_start.day),
                    'date_end': str(pd.date_end.year) + "/" + str(pd.date_end.month) + "/" + str(pd.date_end.day),
                    'mojavez': pd.mojavez.url,
                    'mostanadat': pd.mostanadat.url,
                    'file_ha': pd.file_ha.url,
                    'note': pd.note,
                    'view_count': pd.view_count,
                })
            return Response({"response": projects_data}, status=status.HTTP_200_OK)
        except:
            return Response({"response": "error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ApiProjectType(APIView):

    def get(self, request, pt_id, format=None):
        try:
            print("pt_id: " + pt_id)
            all_map_obj_types_data = []
            all_marahel_ejra_data = []
            all_map_obj_types = main.models.MapObjectTypes.objects.filter(id=pt_id)
            for pd in all_map_obj_types:
                mejr_all = pd.marhalel_ejra_s.all()
                for me in mejr_all:
                    all_marahel_ejra_data.append(me.marhale)
                all_map_obj_types_data = {
                    'id': pd.id,
                    'title': pd.title,
                    'icon': pd.icon.url,
                    'marahel': all_marahel_ejra_data,
                    'marahel_count': pd.marhalel_ejra_s.count(),
                }
            if all_map_obj_types.count() == 0:
                return Response({"response": "noting found any value"}, status=status.HTTP_200_OK)
            else:
                return Response(all_map_obj_types_data, status=status.HTTP_200_OK)
        except:
            return Response({"response": "error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ApiProjectMosatanadat(APIView):

    def post(self, request, pt_id, format=None):
        try:
            print("pt_id: " + pt_id)
            if "photo" in self.request.FILES:
                doc_name = self.request.POST["DocName"]
                doc_type = self.request.POST["DocType"]
                mdi_icon = self.request.POST["MDIIcon"]
                my_file = request.FILES['photo']

                pf_instance = main.models.ProjectFiles.objects.create(
                    DocName=doc_name,
                    DocType=doc_type,
                    MDIIcon=mdi_icon,
                    photo=my_file,
                    Uploader_id=self.request.user.id,
                )
                print("PFInstance:", pf_instance.id, pf_instance)

                main.models.Project.objects.filter(id=pt_id).get().Documents.add(pf_instance)

                register_event(self, pt_id, "بارگزاری مستندات",
                                "یک فایل با توضییحات " + doc_name + " در پروژه  " + pt_id + " بارگزاری شد. ")

                return Response(
                    {
                        "status": "ok",
                        "doc_name": doc_name,
                        "doc_type": doc_type,
                    }, status=status.HTTP_200_OK)
            else:
                return Response("تصویر را وارد کنید", status=status.HTTP_400_BAD_REQUEST)
        except NameError:
            return Response(NameError, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def register_event(self, pid, ev_type, text):
    print(datetime.now())
    ev1 = Events.objects.create(
        # do_time=datetime.now(),
        # day="25/12/1390",
        EventType=ev_type,
        description=text,
        # OwnerUser=accounts.models.CustomUser.abstract,
        OwnerUser=self.request.user,
        # OwnerUser_id=1,
        RelatedProject_id=pid,
    )
    print(ev1)

    ev = Events()
    ev.EventType = ev_type
    ev.description = text
    # ev.day = "2323232"
    ev.OwnerUser = self.request.user
    ev.RelatedProject = main.models.Project.objects.filter(id=pid).get()
    ev.save()
    print(ev)
