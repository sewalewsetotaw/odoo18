from odoo import models,fields,api

class FeeStructure(models.Model):
    _name = 'fees.structure'
    _description = 'Fee Structure'

    name = fields.Char(string='Fee Name', required=True)
    code = fields.Char(string="Code", required=True)
    amount = fields.Float(string="Amount", required=True)

    company_id = fields.Many2one(
        'res.company',
        string="Company",
        default=lambda self: self.env.company
    )

    currency_id = fields.Many2one(
        'res.currency',
        string="Currency",
        related='company_id.currency_id',
        store=True,
        readonly=True
    )
    # income_account_id = fields.Many2one(
    #     'account.account',
    #     string="Income Account",
    #     domain="[('account_type', '=', 'income')]",
    #     # domain="[('internal_group', '=', 'income')]",
    #     required=True,
    #     help="Select the income account where this fee will be posted."
    # )