from django.db import models
from ..users.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from .custom_fields import OrderField


# Create your models here.
class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating
    ``created`` and ``modified`` fields.
    """
    created = models.DateTimeField(
        auto_now_add=True, verbose_name="Created",
        help_text="Date and time of creation")
    modified_at = models.DateTimeField(
        auto_now=True, verbose_name="Modified",
        help_text="Date and time of modification")

    class Meta:
        abstract = True


class Subject(TimeStampedModel):
    title = models.CharField(
        max_length=200,
        verbose_name="Title",
        help_text="Title of the subject"
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name="Slug",
        help_text="Slug of the subject"
    )
    description = models.TextField(
        verbose_name="Description",
        help_text="Description of the subject",
        blank=True, null=True
    )

    class Meta:
        verbose_name = "Subject"
        verbose_name_plural = "Subjects"

    def __str__(self):
        return self.title


class Course(TimeStampedModel):
    """
    Course model
    """
    title = models.CharField(
        max_length=200,
        verbose_name="Title",
        help_text="Title of the course"
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="courses_created",
        verbose_name="owner",
        help_text="Instructor of the course"
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name="courses",
        verbose_name="Subject",
        help_text="Subject of the course"
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name="Slug",
        help_text="Slug of the course"
    )
    overview = models.TextField(
        verbose_name="Overview",
        help_text="Course overview"
    )

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"
        db_table = "courses"
        ordering = ["-created"]

    def __str__(self):
        return self.title


class Module(TimeStampedModel):
    """
    Module model
    """
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="modules",
        verbose_name="Course",
        help_text="Course linked to the module"
    )
    title = models.CharField(
        max_length=200,
        verbose_name="Title",
        help_text="Title of the module"
    )
    description = models.TextField(
        verbose_name="Description",
        help_text="Description of the module"
    )
    order = OrderField(
        blank=True,
        for_fields=["course"],
        help_text="Order of the module"
    )

    class Meta:
        verbose_name = "Module"
        verbose_name_plural = "Modules"
        db_table = "modules"
        ordering = ["order"]

    def __str__(self):
        return f"{self.order}. {self.title}"


class Content(models.Model):
    """
    Content model
    content_type: The type of the content
    object_id: The id of the related object
    item: A generic foreign key to the related object, combining the two previous fields
    """
    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        related_name="contents",
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={"model__in": ("text", "video", "image", "file")},
    )
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    order = OrderField(
        blank=True,
        for_fields=["module"],
        help_text="Order of the content"
    )

    class Meta:
        ordering = ["order"]
        verbose_name = "Content"
        verbose_name_plural = "Contents"
        db_table = "contents"

    def __str__(self):
        return self.item.__str__()


class BaseItem(TimeStampedModel):
    """
    BaseItem model
    """
    title = models.CharField(
        max_length=200,
        verbose_name="Title",
        help_text="Title of the item"
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_related',
        verbose_name="Owner",
        help_text="User who created the content"
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


class Text(BaseItem):
    """
    Text model to store text content
    """
    content = models.TextField(
        verbose_name="Content",
        help_text="Content of the text"
    )

    class Meta:
        verbose_name = "Text"
        verbose_name_plural = "Texts"
        db_table = "texts"

    def __str__(self):
        return self.title


class File(BaseItem):
    """
    File model to store files such as PDFs
    """
    file = models.FileField(
        upload_to="files",
        verbose_name="File",
        help_text="File"
    )

    class Meta:
        verbose_name = "File"
        verbose_name_plural = "Files"
        db_table = "files"

    def __str__(self):
        return self.title


class Image(BaseItem):
    """
    Image model to store images
    """
    image = models.FileField(
        upload_to="images",
        verbose_name="Image",
        help_text="Image"
    )

    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"
        db_table = "images"

    def __str__(self):
        return self.title


class Video(BaseItem):
    """
    Video model to store videos
    """
    url = models.URLField(verbose_name="URL", help_text="URL of the video")

    class Meta:
        verbose_name = "Video"
        verbose_name_plural = "Videos"
        db_table = "videos"

    def __str__(self):
        return self.title
