# from main.models import Shoes
# from .models import *
# # from django import forms
# from django.forms import ModelForm
#
# class ProductCreateForm(ModelForm):
#     class Meta:
#         model = Shoes
#         fields = '__all__'
#
#         def __init__(self, *args, **kwargs):
#             super().__init__(*args, **kwargs)
#             for field in self.fields.values():
#                 field.widget.attrs['class'] = 'form-control'
#
#
# # class ProductChangeForm(forms.ModelForm):
# #     password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
# #     password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
# #     class Meta:
# #         model = CustomUser
# #         fields = '__all__'
# #
# #     def __init__(self, *args, **kwargs):
# #         super().__init__(*args, **kwargs)
# #         for field in self.fields.values():
# #             field.widget.attrs['class'] = 'form-control'
# #             if not field.required:
# #                 field.required = False
