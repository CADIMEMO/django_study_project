from django.contrib.sitemaps import Sitemap

from .models import Product

class ShopSitemap(Sitemap):

    changefreq = 'never'
    priority = 0.5

    def items(self):
        return Product.objects.all()

    def lastmod(self, obj: Product):
        return obj.create_at

