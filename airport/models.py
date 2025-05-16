from django.db import models

from config import settings


class Airport(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    closest_big_city = models.CharField(
        max_length=255, null=False, blank=False
    )

    def __str__(self):
        return (
            f"Airport - {self.name}, "
            f"closest big city - {self.closest_big_city}"
        )


class Route(models.Model):
    source = models.ForeignKey(
        Airport, on_delete=models.CASCADE, related_name="departing_routes"
    )
    destination = models.ForeignKey(
        Airport, on_delete=models.CASCADE, related_name="arriving_routes"
    )
    distance = models.PositiveIntegerField()

    def __str__(self):
        return (
            f"{self.source} -> {self.destination} "
            f"distance({self.distance}km)"
        )


class AirplaneType(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False, unique=True)

    def __str__(self):
        return self.name


class Airplane(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    rows = models.PositiveIntegerField()
    seats_in_row = models.PositiveIntegerField()
    airplane_type = models.ForeignKey(
        AirplaneType, on_delete=models.CASCADE, related_name="airplanes"
    )

    def __str__(self):
        return (
            f"{self.name} - {self.airplane_type} "
            f"seats in row: {self.seats_in_row}"
        )


class Crew(models.Model):
    first_name = models.CharField(max_length=255, null=False, blank=False)
    last_name = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Flight(models.Model):
    route = models.ForeignKey(
        Route, on_delete=models.CASCADE, related_name="flights"
    )
    airplane = models.ForeignKey(
        Airplane, on_delete=models.CASCADE, related_name="flights"
    )
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    crew = models.ManyToManyField(Crew, related_name="flights")

    def __str__(self):
        return (
            f"{self.airplane} - {self.route}. "
            f"Departure-Arrival: {self.departure_time}-{self.arrival_time}"
        )


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=False,
        on_delete=models.CASCADE,
        related_name="orders",
    )

    def __str__(self):
        return f"Order #{self.id} created at {self.created_at} by {self.user}"


class Ticket(models.Model):
    row = models.PositiveIntegerField()
    seat = models.PositiveIntegerField()
    flight = models.ForeignKey(
        Flight, on_delete=models.CASCADE, related_name="tickets"
    )
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="tickets"
    )

    def __str__(self):
        return (
            f"Flight: {self.flight.route.source.name}-"
            f"{self.flight.route.destination.name} ("
            f"{self.flight.departure_time.strftime('%Y-%m-%d %H:%M')}), "
            f"Row: {self.row}, Seat: {self.seat}, Order ID: {self.order.id}"
        )
