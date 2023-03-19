from django.db import models
from api.models import RootModel
from ..accounts.models import CustomUser


class TemplateStyle(RootModel):
    description = models.CharField(max_length=255)
    meta_required = models.BooleanField(default=False)
    meta_placeholder = models.CharField(max_length=255)


class TemplateSectionType(RootModel):
    description = models.CharField(max_length=255)
    meta_required = models.BooleanField(default=False)
    meta_placeholder = models.CharField(max_length=255)


class Template(RootModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    style = models.ForeignKey(TemplateStyle, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    meta = models.CharField(max_length=255, null=True, blank=True)

    def parse_style(self):
        if self.style.description.lower() == "custom":
            return self.meta
        if self.meta is not None:
            return "{} ({})".format(self.style.description, self.meta)
        return self.style.description

    def parse_sections(self):
        sections = self.sections.order_by("order")
        if not sections.count():
            return ""
        return "\n".join(
            [
                "The message should have the following sections (1-2 sentences each):"
            ] +
            [
                '{}. {}'.format(
                    i + 1,
                    s.parse(),
                ) for i, s in enumerate(self.sections.order_by("order"))
            ])


class TemplateSection(RootModel):
    type = models.ForeignKey(TemplateSectionType, on_delete=models.CASCADE)
    order = models.IntegerField()
    meta = models.CharField(max_length=255, null=True, blank=True)
    template = models.ForeignKey(Template, on_delete=models.CASCADE, related_name="sections")

    def parse(self):
        if self.type.description.lower() == "custom":
            return self.meta
        if self.meta is not None:
            return "{} ({})".format(self.type.description, self.meta)
        return self.type.description
