from django.db import models
from django.shortcuts import render
from django import forms

from wagtail.admin.edit_handlers import (
    FieldPanel,
    StreamFieldPanel,
    MultiFieldPanel,
    InlinePanel,
)
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.core.models import Page, Orderable
from wagtail.core.fields import StreamField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.snippets.models import register_snippet
from modelcluster.fields import ParentalKey, ParentalManyToManyField

from streams import blocks



class BlogAuthorsOderable(Orderable):
    """Allows us to select one of more blog authors"""

    page = ParentalKey('blog.BlogDetailPage', related_name= 'blog_authors')
    author = models.ForeignKey(
        "blog.BlogAuthor",
        on_delete=models.CASCADE,
    )

    panels = [
        SnippetChooserPanel('author'),

    ]
class BlogAuthor(models.Model):
    """Blog author for snippets"""

    name = models.CharField(max_length=100)
    website = models.URLField(blank=True, null=True)
    image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name="+",
    )

    panels=[
        MultiFieldPanel(
            [
            FieldPanel('name'),
            ImageChooserPanel('image'),
        ],
           heading="Name and Image",
        ),

        MultiFieldPanel(
            [
                FieldPanel("website"),
            ],
            heading="Links"
        )
    ]

    def __str__(self):
        """String repr of this class."""
        return self.name

    class Meta: #noqa
        verbose_name = "Blog Author"
        verbose_name_plural = "Blog Authors"

register_snippet(BlogAuthor)


class BlogCategory(models.Model):
    """Blog category for a snippet"""

    name = models.CharField(max_length=255)
    slug = models.SlugField(
        verbose_name="slug",
        allow_unicode=True,
        max_length=255,
        help_text='A slug to identify posts by this category'
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("slug"),
    ]


    class Meta: #noqa
        verbose_name = "Blog Category"
        verbose_name_plural = "Blog Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


register_snippet(BlogCategory)


class BlogListingPage(RoutablePageMixin, Page):
    """Listing all the blog detail pages"""

    template = "blog/blog_listing_page.html"
    custom_title = models.CharField(
        max_length=100, 
        blank = False, 
        null=False, 
        help_text="Overwrites default Title",
        )

    content_panels = Page.content_panels + [
        FieldPanel("custom_title"),
    ]

    def get_context(self, request, *args, **kwargs):
        context=super().get_context(request, *args, **kwargs)
        context["posts"] = BlogDetailPage.objects.live().public()
        context["category"]= BlogCategory.objects.all()
        context["authors"] = BlogAuthor.objects.all()
        return context

    @route(r'^latest/$', name="latest_posts")
    def latest_blog_posts(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["latest_posts"] = BlogDetailPage.objects.live().public()[:1]
        return render(request,"blog/latest_posts.html", context)

    def get_sitemap_urls(self, request):
        sitemap = super().get_sitemap_urls(request)
        sitemap.append({
            "location":self.full_url + self.reverse_subpage("latest_posts") ,
            "lastmod": (self.last_published_at or self.latest_revision_created_at),
        }
        )
        return sitemap


class BlogDetailPage(Page):
        """Blog detail pages"""
        
        custom_title = models.CharField(
            max_length=100, 
            blank = False, 
            null=False, 
            help_text="Overwrites default Title",
            )

        blog_image = models.ForeignKey(
            "wagtailimages.Image",
            blank = False, 
            null=True,
            related_name="+",
            on_delete="models.SET_NULL",
        )

        categories = ParentalManyToManyField("blog.BlogCategory", blank=True)
        content = StreamField(
        [
            ("title_and_text", blocks.TitleAndTextBlock()),
            ("full_richtext", blocks.RichtextBlock()),
            ("simple_richtext", blocks.SimpleRichtextBlock()),
            ("cards", blocks.CardBlock()),
            ("cta", blocks.CTABlock()),
        ],
        null=True,
        blank = True
        )

        content_panels = Page.content_panels + [
            FieldPanel("custom_title"),
            ImageChooserPanel("blog_image"),
            StreamFieldPanel("content"),
            MultiFieldPanel(
                [
                    InlinePanel("blog_authors", label='Author', min_num=1, max_num=4)
                ],
                heading="Author(s)"
            ),
            MultiFieldPanel(
                [
                    FieldPanel("categories", widget=forms.CheckboxSelectMultiple)
                ],
                heading="Categories"
            ),
        ]
