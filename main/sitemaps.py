from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    protocol = "https"

    PAGES = {
        "home":     {"priority": 1.0, "changefreq": "weekly"},
        "services": {"priority": 0.9, "changefreq": "monthly"},
        "works":    {"priority": 0.8, "changefreq": "weekly"},
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
