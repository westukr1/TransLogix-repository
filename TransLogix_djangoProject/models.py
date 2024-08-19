import self
from django.db import models

from django.contrib.auth.hashers import make_password, check_password
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

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.last_name = None
        self.first_name = None

    def set_password(self, raw_password):
        """Sets the user's password."""
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """Checks if the provided password matches the stored password."""
        return check_password(raw_password, self.password)

    def get_full_name(self):
        """Returns the user's full name."""
        return f"{self.first_name} {self.last_name}" if self.first_name and self.last_name else self.username


class Driver(models.Model):
    driver_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    license_number = models.CharField(max_length=50, unique=True)
    phone_number = models.CharField(max_length=20)

    self.name()

    def get_license_info(self):
        """Returns the driver's license number."""
        return f"License: {self.license_number}"

    def get_contact_info(self):
        """Returns the driver's contact information."""
        return f"Phone: {self.phone_number}, Email: {self.user.email if self.user else ''}"

    self.name()


class Vehicle(models.Model):
    vehicle_id = models.AutoField(primary_key=True)
    license_plate = models.CharField(max_length=20, unique=True)
    model = models.CharField(max_length=100)
    capacity = models.IntegerField()
    fuel_type = models.CharField(max_length=50)

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.status = None

    var = self.license_plate

    def is_available(self):
        """Checks if the vehicle is available."""
        return self.status == 'Available'

    def get_vehicle_info(self):
        """Returns the vehicle's information."""
        return f"{self.model} ({self.license_plate}), Capacity: {self.capacity}"

    var = self.license_plate

class Route(models.Model):
    route_id = models.AutoField(primary_key=True)
    start_location = models.CharField(max_length=255)
    end_location = models.CharField(max_length=255)
    distance = models.FloatField()
    estimated_time = models.DurationField()

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.license_plate = None
        self.model = None
        self.status = None

    def __str__(self):
        return f"{self.start_location} to {self.end_location}"

    def is_available(self):
        """Checks if the vehicle is available."""
        return self.status == 'Available'

    def get_vehicle_info(self):
        """Returns the vehicle's information."""
        return f"{self.model} ({self.license_plate}), Capacity: {self.capacity}"

    self.license_plate()

from django.db import models

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

    class Meta:
        ordering = ['-date']  # За замовчуванням сортування за датою (найновіші спочатку)
        verbose_name = "Trip"
        verbose_name_plural = "Trips"

    def is_completed(self):
        """Check if the trip is completed."""
        return self.status == 'completed'

    def complete_trip(self):
        """Mark the trip as completed."""
        self.status = 'completed'
        self.save()

    def get_trip_details(self):
        """Returns detailed information about the trip."""
        return f"Trip ID: {self.trip_id}, Route: {self.route}, Driver: {self.driver}, Vehicle: {self.vehicle}, Date: {self.date}"

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

    def get_total_cost(self):
        """Calculates the total cost of the fuel."""
        return self.fuel_amount * self.price

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

    def is_positive(self):
        """Check if the feedback is positive."""
        return self.rating >= 4

    def get_summary(self):
        """Returns a summary of the feedback."""
        return f"Rating: {self.rating}, Comments: {self.comments[:50]}..."  # First 50 characters

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

    def confirm(self):
        """Confirm the booking."""
        self.status = 'confirmed'
        self.save()

    def cancel(self):
        """Cancel the booking."""
        self.status = 'canceled'
        self.save()

    def is_pending(self):
        """Check if the booking is still pending."""
        return self.status == 'pending'

    def __str__(self):
        return f"Booking {self.booking_id} - {self.status}"