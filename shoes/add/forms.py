from main.models import Shoes, Orders, Order_status, Collection

from django import forms

class CollectionAddForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = ['c_name', 'c_description']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = Shoes
        fields = ['sh_name', 'sh_model', 'sh_size', 'sh_color', 'sh_manufacturer', 'sh_count', 'sh_price', 'sh_gender']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class OrderCreateForm(forms.ModelForm):
    o_status = forms.ChoiceField(
        choices=[(status.value, status.name) for status in Order_status],
        required=False,  # Робимо необов'язковим, якщо редагування обмежене
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Orders
        fields = [
            'o_recipient_first_name',
            'o_recipient_last_name',
            'o_email',
            'o_phone_number',
            'o_address',
            'o_comment',
            'o_count',
            'o_shoes'
        ]
        widgets = {
            'o_comment': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        # Отримуємо request із kwargs
        self.request = kwargs.get('request', None)
        super().__init__(*args, **kwargs)
        self.fields['o_comment'].required = False
        self.fields['o_comment'].widget.attrs['readonly'] = True

        initial = kwargs.get('initial', {})
        if 'o_shoes' in initial:
            self.base_fields['o_shoes'].widget.attrs['readonly'] = True

        self.fields['o_shoes'] = forms.ModelChoiceField(
            queryset=Shoes.objects.all(),
            empty_label="Select a shoe",  # Показуємо це як порожній вибір
            widget=forms.Select(attrs={'class': 'form-control'})
        )

    def user_is_admin(self):
        """Перевірка, чи користувач є адміністратором."""
        if self.request:
            return self.request.user.is_authenticated and self.request.user.user_role == 'admin'
        return False

    def save(self, commit=True):
        instance = super().save(commit=False)
        print(f"Saving status: {self.cleaned_data.get('o_status')}")
        if 'o_status' in self.cleaned_data:
            instance.o_status = self.cleaned_data['o_status']
        # Автоматичне обчислення o_sum
        if instance.o_shoes and instance.o_count:
            instance.o_sum = instance.o_shoes.sh_price * instance.o_count

        if commit:
            instance.save()
        return instance


