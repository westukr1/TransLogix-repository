
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Trip, Vehicle, Driver

@receiver(post_save, sender=Trip)
def update_vehicle_status(sender, instance, **kwargs):
    if instance.status == 'completed':
        instance.vehicle.status = 'Available'
        instance.vehicle.save()

@receiver(post_save, sender=Trip)
def update_driver_status(sender, instance, **kwargs):
    if instance.status == 'completed':
        instance.driver.status = 'Available'
        instance.driver.save()

@receiver(post_delete, sender=Trip)
def cleanup_vehicle_and_driver(sender, instance, **kwargs):
    # Set vehicle and driver statuses to 'Available' when a trip is deleted
    instance.vehicle.status = 'Available'
    instance.vehicle.save()
    instance.driver.status = 'Available'
    instance.driver.save()

@receiver(post_save, sender=Vehicle)
def log_vehicle_update(sender, instance, **kwargs):
    # Example signal to log when a vehicle is updated
    print(f"Vehicle {instance.license_plate} has been updated.")
