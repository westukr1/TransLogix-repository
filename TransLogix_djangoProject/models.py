from django.db import models

class User(models.Model):
    USER_ROLES = [
        ('driver', 'Driver'),
        ('operator', 'Operator'),
        ('financial_manager', 'Financial Manager'),
        ('admin', 'Administrator'),
    ]

    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=USER_ROLES)

    def __str__(self):
        return self.username


class Driver(models.Model):
    driver_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    license_number = models.CharField(max_length=50, unique=True)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Vehicle(models.Model):
    vehicle_id = models.AutoField(primary_key=True)
    license_plate = models.CharField(max_length=20, unique=True)
    model = models.CharField(max_length=100)
    capacity = models.IntegerField()
    fuel_type = models.CharField(max_length=50)

    def __str__(self):
        return self.license_plate


class Route(models.Model):
    route_id = models.AutoField(primary_key=True)
    start_location = models.CharField(max_length=255)
    end_location = models.CharField(max_length=255)
    distance = models.FloatField()
    estimated_time = models.DurationField()

    def __str__(self):
        return f"{self.start_location} to {self.end_location}"


class Trip(models.Model):
    TRIP_STATUS = [
        ('scheduled', 'Scheduled'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
    ]

    trip_id = models.AutoField(primary_key=True)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=20, choices=TRIP_STATUS)

    def __str__(self):
        return f"Trip {self.trip_id} - {self.status}"


class FuelLog(models.Model):
    fuel_log_id = models.AutoField(primary_key=True)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    fuel_amount = models.FloatField()
    price = models.FloatField()
    date = models.DateField()
    station_name = models.CharField(max_length=255)

    def __str__(self):
        return f"Fuel Log {self.fuel_log_id} - {self.trip}"


class Feedback(models.Model):
    feedback_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    comments = models.TextField()
    rating = models.IntegerField()

    def __str__(self):
        return f"Feedback {self.feedback_id} - {self.rating}"


class BookingRequest(models.Model):
    BOOKING_STATUS = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('canceled', 'Canceled'),
    ]

    booking_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=20, choices=BOOKING_STATUS)

    def __str__(self):
        return f"Booking {self.booking_id} - {self.status}"
