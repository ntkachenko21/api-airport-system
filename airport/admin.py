from django.contrib import admin

from airport.models import (
    Airplane,
    Airport,
    Route,
    Ticket,
    Crew,
    AirplaneType,
    Order,
    Flight
)

admin.site.register(Airplane)
admin.site.register(Airport)
admin.site.register(Route)
admin.site.register(Ticket)
admin.site.register(Crew)
admin.site.register(AirplaneType)
admin.site.register(Order)
admin.site.register(Flight)
