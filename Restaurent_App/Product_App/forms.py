from django import forms
from Product_App.models import Reservation
import datetime


class ReserveForm(forms.ModelForm):

    def __init__(self, restaurent_seat, *args, **kwargs):
        self.restaurent_seat = restaurent_seat
        super(ReserveForm, self).__init__(*args, **kwargs)

    booking_date = forms.DateField(widget=forms.DateInput(attrs=dict(type='date')))
    restaurents = forms.HiddenInput()
    class Meta:
        model = Reservation
        fields = ('person', 'booking_date', 'booking_time')
        widgets = {
            'restaurents': forms.HiddenInput(),
        }

    def clean_booking_date(self):
        date = self.cleaned_data.get('booking_date')
        if date < datetime.date.today():
            raise forms.ValidationError("The date cannot be in the past!")
        return date

    def clean_person(self):
        rest = self.restaurent_seat
        persons = self.cleaned_data.get('person')
        # print(rest.total_seat)
        if persons>rest:
            raise forms.ValidationError(f"Restaurent Capacity {rest}")
        return persons


