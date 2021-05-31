from odoo import models, fields

class SaleOrderInheritShopifyOdooInventorySalesSynchronisation(models.Model):
  _inherit = 'sale.order'

  shopify_sale_order_id = fields.Char(string="Shopify Order ID") 
