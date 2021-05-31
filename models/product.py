from odoo import models, fields, api, _
import requests
import json
import logging

_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    shopify_product_id = fields.Char()

    def get_product_parent_tags(self):
        res_categ = []
        for categs in self.public_categ_ids:
            res_categ.append(categs.display_name.split('/'))
        if res_categ:
            if len(res_categ) <= 1:
                res_categ = res_categ[0]

        return res_categ

    def get_shopify_data_upload(self):
        _logger.info(_("Started getting data of the product %s") % self.name)
        variants = self.product_variant_ids
        product_image = ''
        table_image = ''
        additional_images = []
        if self.image:
            product_image = self.image.decode('utf-8')
        if self.x_studio_image_shopify:
            table_image = self.x_studio_image_shopify.decode('utf-8')
        for image_data in self.product_image_ids:
            additional_images.append( image_data.image.decode('utf-8') )
        shopify_data_post = {
            "title": self.name,
            "vendor": self.marca_ids.mapped('display_name'),
            "shopify_product_id": self.shopify_product_id,
            "description": self.website_description,
            "tags": self.get_product_parent_tags(),
            "images": product_image,
            "table_image": table_image,
            "additional_images": additional_images,
            "is_published": self.x_studio_website_shopify,
            "variants": [
                {
                    "sku": variant.default_code,
                    "variant_data": [{variant_attribute.attribute_id.display_name: variant_attribute.name} for
                                     variant_attribute in
                                     variant.attribute_value_ids],

                    "stock": variant.qty_available,
                    "sales_price": variant.list_price,
                    "barcode": variant.barcode,
                    "taxable": bool(variant.taxes_id),
                    "shopify_variant_id": variant.shopify_variant_id,
                    "inventory_item_id": variant.shopify_inventory_item_id
                } for variant in variants
            ]
        }
        return shopify_data_post

    def upload_product_to_shopify(self):
        for line in self:
            upload_data = line.get_shopify_data_upload()
            if upload_data:
                headers = {'Content-Type': 'application/json'}
                data_json = json.dumps({'params': upload_data})

                try:
                    shopify_product_upload_url = self.env.user.company_id.shopify_product_upload_url
                    requests.post(url=shopify_product_upload_url, data=data_json, headers=headers)
                except Exception as e:
                    _logger.error(
                        "Failed to send post request to shopify for upload the product %s, reason : %s" % (
                            self.name, e))
            else:
                _logger.error(_("The upload data is empty for the product %s") % (self.name))


class ProductProduct(models.Model):
    _inherit = 'product.product'

    shopify_variant_id = fields.Char(string="Shopify variant_id")
    shopify_inventory_item_id = fields.Char(string="Shopify inventory_item_id")
