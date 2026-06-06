from django import forms
from .models import Product


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['name', 'price', 'category', 'description', 'image', 'image_url']

        labels = {
            'name': 'Product Name',
            'price': 'Price',
            'category': 'Category',
            'description': 'Product Description',
            'image': 'Product Image',
            'image_url': 'Product Image URL'
        }

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Enter product name'
            }),

            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter price',
                'min': '1'
            }),

            'category': forms.Select(attrs={
                'class': 'form-control'
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter product description',
                'rows': 4
            }),

            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
            
            'image_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://example.com/image.jpg'
            })
            
        }    

    # 🔥 VALIDATION


    
    def clean(self):

        cleaned_data = super().clean()

        image = cleaned_data.get('image')
        image_url = cleaned_data.get('image_url')

        if not image and not image_url:
            raise forms.ValidationError(
                "Upload image or enter image URL"
            )

        return cleaned_data