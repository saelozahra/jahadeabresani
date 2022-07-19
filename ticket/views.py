from django.shortcuts import render
from django.views.generic import TemplateView

import ticket.models
from django.db.models import Q

# Create your views here.


class Tickets(TemplateView):
    def get(self,request):
        all_tickets = ticket.models.Ticket.objects.filter(Q(User=self.request.user))
        context = {
            'tickets': all_tickets.values(),
        }
        return render(request, 'tickets.html', context)


class SingleTicket(TemplateView):
    def get(self, request, id):
        all_tickets  = ticket.models.Ticket.objects.filter(Q(id=id))
        all_messages = ticket.models.TicketMessage.objects.filter(Q(RelatedTicket_id=id))
        context = {
            'Ticket':   all_tickets.values(),
            'Messages': all_messages.values(),
        }
        return render(request, 'tickets.html', context)