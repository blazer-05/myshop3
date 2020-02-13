# -*- coding: utf-8 -
"""
This file was generated with the cmlpipelines management command.
It contains the pipelines classes for that accept or send items for
import/export purposes.

To activate your pipelines add the following to your settings.py:
    CML_PROJECT_PIPELINES = 'myshop3.cml_pipelines'
"""

from django.core.files import File
from pytils.translit import slugify
from shop.models import Category, Product, Brand, Attribute, Value, Entry


class GroupPipeline(object):
    """
    Item fields:
    id
    name
    groups
    """
    def process_item(self, item):
        self.recursive_create(item)

    @classmethod
    def recursive_create(cls, item, parent=None):
        Category.objects.filter(name=item.name).update(id_cml=item.id)
        category, _ = Category.objects.update_or_create(
            id_cml=item.id,
            defaults={
                'name': item.name,
                'slug': slugify(item.name),
                'parent': parent,
            }
        )
        for child_group in item.groups:
            cls.recursive_create(child_group, category)


class PropertyPipeline(object):
    """
    Item fields:
    id
    name
    value_type
    for_products
    """
    def process_item(self, item):
        Attribute.objects.get_or_create(
            id_cml=item.id,
            defaults={
                'title': item.name
            }
        )


class PropertyVariantPipeline(object):
    """
    Item fields:
    id
    value
    property_id
    """
    def process_item(self, item):
        Value.objects.get_or_create(
            id_cml=item.id,
            defaults={
                'value': item.value,
                'attribute': Attribute.objects.get(id_cml=item.property_id)
            }
        )


class SkuPipeline(object):
    """
    Item fields:
    id
    name
    name_full
    international_abbr
    """
    def process_item(self, item):
        pass


class TaxPipeline(object):
    """
    Item fields:
    name
    value
    """
    def process_item(self, item):
        pass


class BrandPipeline(object):
    """
    Item fields:
    id
    name
    """
    def process_item(self, item):
        Brand.objects.filter(name=item.name).update(id_cml=item.id)
        Brand.objects.update_or_create(
            id_cml=item.id,
            defaults={
                'name': item.name,
                'slug': slugify(item.name),
            }
        )


class ProductPipeline(object):
    """
    Item fields:
    id
    name
    description
    brand_id
    sku_id
    group_ids
    properties
    tax_name
    image_path
    additional_fields
    """
    def process_item(self, item):
        obj, _ = Product.objects.update_or_create(
            id_cml=item.id,
            defaults={
                'title': item.name,
                'slug': slugify(item.name),
                'descriptions': item.description,
                'brand': Brand.objects.filter(id_cml=item.brand_id).first(),
                'category': Category.objects.filter(id_cml__in=item.group_ids).first(),
            }
        )
        for attr_id_cml, value_id_cml in item.properties:
            Entry.objects.get_or_create(
                product=obj,
                attribute=Attribute.objects.get(id_cml=attr_id_cml),
                value=Value.objects.get(id_cml=value_id_cml),
            )
            category = Category.objects.filter(id_cml__in=item.group_ids).first()
            category.attributes.add(
                Attribute.objects.get(id_cml=attr_id_cml)
            )
        if item.image_path:
            import os
            with open(item.image_path, 'rb') as f:
                file_name = os.path.basename(item.image_path)
                image = File(f)
                obj.images.save(file_name, image)
                obj.save()

        print(obj.pk)


class PriceTypePipeline(object):
    """
    Item fields:
    id
    name
    currency
    tax_name
    tax_in_sum
    """
    def process_item(self, item):
        pass


class OfferPipeline(object):
    """
    Item fields:
    id
    name
    sku_id
    prices
    """
    def process_item(self, item):
        Product.objects.filter(
            title=item.name
        ).update(
            price=item.prices[0].price_for_sku,
            stock=item.quantity,

        )


class OrderPipeline(object):
    """
    Item fields:
    id
    number
    date
    currency_name
    currency_rate
    operation
    role
    sum
    client
    time
    comment
    items
    additional_fields
    """
    def process_item(self, item):
        pass

    def yield_item(self):
        pass

    def flush(self):
        pass
