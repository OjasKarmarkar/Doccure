from django.db import models
# Create your models here.
STATUS_CHOICES = (
    ("UNREVIEWED", "Not Reviewed"),
    ("ACCEPTED", "Accept"),
    ("DECLINED", "Reject"),
)
class Appointment(models.Model):
  appointmentId = models.CharField(primary_key=True , max_length=100 , default='00')
  doctorMail = models.EmailField(null=False , primary_key=False , max_length=100 , default="doc@gmail.com")
  special = models.CharField(null=False , primary_key=False , max_length=100 , default="ortho")
  patientMail = models.EmailField(null=False , primary_key=False , max_length=100 , default="patient@gmail.com")
  patientName = models.CharField(null=False , primary_key=False , max_length=100 , default="patient 1")
  doctorName = models.CharField(null=False , primary_key=False , max_length=100 , default="doctor 1")
  doctorPhoto = models.CharField(null=False , primary_key=False , max_length=100 , default="patient 1")
  patientPhoto = models.CharField(null=False , primary_key=False , max_length=100 , default="patient 1")
  dateOfAppointment = models.DateTimeField()
  status = models.CharField(max_length=20,
                  choices=STATUS_CHOICES,
                  default="UNREVIEWED")
      
  def __str__(self):
        return self.appointmentId