from odoo import models, fields

class SaleOrderInheritShopifyOdooInventorySalesSynchronisation(models.Model):
  _inherit = 'sale.order'

  shopify_sale_order_id = fields.Char(string="Shopify Order ID") 
  metodo_de_pago = fields.Char(string="Shopify variant_id")
  metodo_de_envio_shopify = fields.Char(string="Shopify inventory_item_id")
