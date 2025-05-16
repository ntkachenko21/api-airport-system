from rest_framework import serializers

from airport.models import (
    Airport,
    Route,
    AirplaneType,
    Airplane,
    Crew,
    Flight,
    Order,
    Ticket,
)
from user.serializers import UserSerializer


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ("id", "name", "closest_big_city",)


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance",)


class RouteListSerializer(serializers.ModelSerializer):
    source = serializers.SlugRelatedField(slug_field="name", many=False, read_only=True)
    destination = serializers.SlugRelatedField(slug_field="name", many=False, read_only=True)

    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance",)


class RouteRetrieveSerializer(RouteSerializer):
    source = AirportSerializer(read_only=True)
    destination = AirportSerializer(read_only=True)


class AirplaneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneType
        fields = ("id", "name",)


class AirplaneTypeRetrieveSerializer(AirplaneTypeSerializer):
    pass


class AirplaneSerializer(serializers.ModelSerializer):
    airplane_type = serializers.PrimaryKeyRelatedField(
        queryset=AirplaneType.objects.all(),
    )

    class Meta:
        model = Airplane
        fields = ("id", "name", "rows", "seats_in_row", "airplane_type",)


class AirplaneListSerializer(serializers.ModelSerializer):
    airplane_type = serializers.SlugRelatedField(
        slug_field="name",
        read_only=True,
    )

    class Meta:
        model = Airplane
        fields = ("id", "name", "rows", "seats_in_row", "airplane_type",)


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = ("id", "first_name", "last_name",)


class FlightSerializer(serializers.ModelSerializer):
    route = RouteSerializer(many=False)
    airplane = AirplaneSerializer(many=False)

    class Meta:
        model = Flight
        fields = ("id", "route", "airplane", "departure_time", "arrival_time", "crew",)


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Order
        fields = ("id", "created_at", "user",)


class TicketSerializer(serializers.ModelSerializer):
    flight = FlightSerializer(many=False)
    order = OrderSerializer(many=True)

    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "flight", "order",)
