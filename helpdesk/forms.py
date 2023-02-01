from django import forms
from .models import Ticket, Comment, Attachment, Vacation
from ckeditor.widgets import CKEditorWidget
class TicketForm(forms.ModelForm):
    department = forms.ChoiceField(required=True, choices=Ticket.DEPARTMENT_CHOICES)
    category = forms.ChoiceField(required=True, choices=Ticket.CATEGORY_CHOICES)
    description=forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Ticket
        fields = ('owner', 'agent', 'department', 'category', 'is_escalated', 'subject', 'description')
    #def __init(self, *args, **kwargs):
    #    self.fields['department'].required = true

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)

class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ('image', 'description')

class VacationRequestForm(forms.ModelForm):
    class Meta:
        model = Vacation
        fields = ('from_date', 'to_date')

class VacationDecisionForm(forms.ModelForm):
    class Meta:
        model = Vacation
        fields = ('status',)

class TicketDecisionForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('status',)

