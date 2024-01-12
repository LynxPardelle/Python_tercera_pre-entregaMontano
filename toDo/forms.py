from django import forms


class CreateNewList(forms.Form):
    name = forms.CharField(label="Name", max_length=140, widget=forms.TextInput(
        attrs={'class': 'form-control bef bef-bg-moccasin bef-text-mystic', 'id': 'list_name', 'name': 'name', 'placeholder': 'Enter New list name'}))


class CreateNewToDo(forms.Form):
    title = forms.CharField(label="Title", max_length=140, widget=forms.TextInput(
        attrs={'class': 'form-control bef bef-bg-moccasin bef-text-mystic', 'id': 'title', 'name': 'title', 'placeholder': 'Enter New toDo title'}))
    description = forms.CharField(label="Description", max_length=500, widget=forms.Textarea(
        attrs={'class': 'form-control bef bef-bg-moccasin bef-text-mystic', 'rows': '2', 'cols': '30', 'id': 'description', 'name': 'description', 'placeholder': 'Enter New toDo description'}))
    priority = forms.IntegerField(label="Priority", widget=forms.NumberInput(
        attrs={'class': 'form-control bef bef-bg-moccasin bef-text-mystic', 'id': 'priority', 'name': 'priority', 'placeholder': 'Enter New toDo priority'}))


class CreateNewCategory(forms.Form):
    name = forms.CharField(label="Name", max_length=140, widget=forms.TextInput(
        attrs={'class': 'form-control bef bef-bg-moccasin bef-text-mystic', 'id': 'name', 'name': 'name', 'placeholder': 'Enter New category name'}))
    all_classes = forms.CharField(label="All Clases", max_length=200, required=False, widget=forms.Textarea(
        attrs={'class': 'form-control bef bef-bg-moccasin bef-text-mystic', 'rows': '2', 'cols': '30', 'id': 'all_classes', 'name': 'all_classes', 'placeholder': 'Enter New custom category clases'}))
    header_classes = forms.CharField(
        label="Header Classes", max_length=255, required=False, widget=forms.Textarea(attrs={'class': 'form-control bef bef-bg-moccasin bef-text-mystic', 'rows': '2', 'cols': '30', 'id': 'header_classes', 'name': 'header_classes', 'placeholder': 'Enter New custom header clases'}))
    box_classes = forms.CharField(
        label="Box Classes", max_length=255, required=False, widget=forms.Textarea(attrs={'class': 'form-control bef bef-bg-moccasin bef-text-mystic', 'rows': '2', 'cols': '30', 'id': 'box_classes', 'name': 'box_classes', 'placeholder': 'Enter New custom box clases'}))
