from django.contrib import admin
from .models import Template, TemplateStyle, TemplateSection, TemplateSectionType


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    model = Template

    list_display = (
        "id",
        "user__email",
        "name",
        "meta",
    )

    def user__email(self, obj):
        return obj.user.email if obj.user else None


@admin.register(TemplateStyle)
class TemplateStyleAdmin(admin.ModelAdmin):
    model = TemplateStyle

    list_display = (
        "id",
        "description",
    )


@admin.register(TemplateSection)
class TemplateSectionAdmin(admin.ModelAdmin):
    model = TemplateSection


@admin.register(TemplateSectionType)
class TemplateSectionTypeAdmin(admin.ModelAdmin):
    model = TemplateSectionType

    list_display = (
        "id",
        "description",
        "meta_placeholder",
    )
