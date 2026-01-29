from django import forms
from .models import Community


class CreateCommunityForm(forms.ModelForm):
    class Meta:
        model = Community
        fields = ["name", "description", "category", "image"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "Community name",
                    "class": "form-input",
                    "style": "width: 100%; padding: 0.75rem; margin-bottom: 1rem; border: 1px solid #e2e8f0; border-radius: 0.5rem;",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "placeholder": "Describe your community",
                    "rows": 5,
                    "class": "form-textarea",
                    "style": "width: 100%; padding: 0.75rem; margin-bottom: 1rem; border: 1px solid #e2e8f0; border-radius: 0.5rem;",
                }
            ),
            "category": forms.Select(
                attrs={
                    "class": "form-select",
                    "style": "width: 100%; padding: 0.75rem; margin-bottom: 1rem; border: 1px solid #e2e8f0; border-radius: 0.5rem;",
                }
            ),
            "image": forms.FileInput(
                attrs={
                    "class": "form-file",
                    "accept": "image/*",
                    "style": "margin-bottom: 1rem;",
                }
            ),
        }

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if len(name) < 3:
            raise forms.ValidationError("Community name must be at least 3 characters long")
        return name

    def clean_description(self):
        description = self.cleaned_data.get("description")
        if len(description) < 10:
            raise forms.ValidationError(
                "Description must be at least 10 characters long"
            )
        return description
