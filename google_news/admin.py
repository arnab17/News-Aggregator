from django.contrib import admin
from .models import News
from .models import Category
from .models import Country
from .models import Rsslinks1
from .models import Rsslinks2
from .models import Rsslinks3
from .models import Rsslinks4
from .models import Rsslinks5

# Register your models here.

admin.site.register(News)
admin.site.register(Country)
admin.site.register(Category)
admin.site.register(Rsslinks1)
admin.site.register(Rsslinks2)
admin.site.register(Rsslinks3)
admin.site.register(Rsslinks4)
admin.site.register(Rsslinks5)
