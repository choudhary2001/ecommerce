from product.models import Product
from django.db.models import Min,Max
from vendor.models import Vendor
def get_filter(request):
	cats=Product.objects.distinct().values('category__title','category__id')
	brands=Product.objects.distinct().values('brand__title','brand__id')
	colors=Product.objects.distinct().values('color__title','color__id','color__color_code')
	sizes=Product.objects.distinct().values('size__title','size__id')
	vendor=Vendor.objects.distinct().values('shop_Name','user__id')
	minMaxPrice=Product.objects.aggregate(Min('price'),Max('price'))
	data={
		'cats':cats,
		'brands':brands,
		'colors':colors,
		'sizes':sizes,
		'minMaxPrice':minMaxPrice,
		'vendor':vendor,
		
	}
	return data