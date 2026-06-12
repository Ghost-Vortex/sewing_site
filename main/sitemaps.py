from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .services_data import SERVICES
from .blog_data import POSTS


class BlogSitemap(Sitemap):
    protocol = "https"
    priority = 0.7
    changefreq = "monthly"

    def items(self):
        return list(POSTS.keys())

    def location(self, item):
        return reverse("blog_post", args=[item])

    def lastmod(self, item):
        from datetime import date
        return date.fromisoformat(POSTS[item]["date"])


class WorkSitemap(Sitemap):
    protocol = "https"
    priority = 0.6
    changefreq = "monthly"

    def items(self):
        from .models import Work
        return Work.objects.filter(is_active=True).exclude(slug=None)

    def location(self, obj):
        return reverse("work_detail", args=[obj.slug])

    def lastmod(self, obj):
        return obj.created_at


class ServiceSitemap(Sitemap):
    protocol = "https"
    priority = 0.85
    changefreq = "monthly"

    def items(self):
        return list(SERVICES.keys())

    def location(self, item):
        return reverse("service_detail", args=[item])


class StaticViewSitemap(Sitemap):
    protocol = "https"

    PAGES = {
        "home":     {"priority": 1.0, "changefreq": "weekly"},
        "services": {"priority": 0.9, "changefreq": "monthly"},
        "works":    {"priority": 0.8, "changefreq": "weekly"},
        "blog":     {"priority": 0.7, "changefreq": "weekly"},
        "about":    {"priority": 0.6, "changefreq": "monthly"},
        "contacts": {"priority": 0.7, "changefreq": "monthly"},
        "privacy":  {"priority": 0.2, "changefreq": "yearly"},
    }

    def items(self):
        return list(self.PAGES.keys())

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        return self.PAGES[item]["priority"]

    def changefreq(self, item):
        return self.PAGES[item]["changefreq"]
