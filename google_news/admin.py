from django.contrib import admin
from .models import News
from .models import Category
from .models import Country
from .models import Cluster
from .models import Keyword
from .models import Cached_Keyword
from .models import Rsslinks1
from .models import Rsslinks2
from .models import Rsslinks3
from .models import Rsslinks4
from .models import Rsslinks5
from .models import Rsslinks6
from .models import Rsslinks7
from .models import Location

# Register your models here.

admin.site.register(News)
admin.site.register(Location)
admin.site.register(Country)
admin.site.register(Category)
admin.site.register(Cluster)
admin.site.register(Keyword)
admin.site.register(Rsslinks1)
admin.site.register(Rsslinks2)
admin.site.register(Rsslinks3)
admin.site.register(Rsslinks4)
admin.site.register(Rsslinks5)
admin.site.register(Rsslinks6)
admin.site.register(Rsslinks7)
admin.site.register(Cached_Keyword)
