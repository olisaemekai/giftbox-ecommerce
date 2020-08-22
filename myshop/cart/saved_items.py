from django.conf import settings
from shop.models import Product
from django.contrib import messages


class SavedItem(object):
    def __init__(self, request):
        """
        Initialize the saved_item.
        """
        self.session = request.session
        saved_items = self.session.get(settings.SAVED_SESSION_ID)
        if not saved_items:
            # save an empty cart in the session
            saved_items = self.session[settings.SAVED_SESSION_ID] = {}
        self.saved_items = saved_items
    
    def add_or_remove(self, product):
        """
        Add a product to saved_items
        """
        product_id = str(product.id)
        if product_id in self.saved_items:
            del self.saved_items[product_id]
        else:
            self.saved_items[product_id] = product.id
        self.save()
    
    def save(self):
        self.session.modified = True

    def __iter__(self):
        product_ids = self.saved_items.keys()
        # get the product objects and add them to saved_items
        products = Product.objects.filter(id__in=product_ids)
        saved_items = self.saved_items.copy()

        for product in products:
            yield product