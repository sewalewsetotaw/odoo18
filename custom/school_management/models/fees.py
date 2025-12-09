from odoo import models, fields, api
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class Fees(models.Model):
    _name = 'fees.fees'
    _description = 'Fees'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    payment_reference = fields.Char(string="Payment Reference", compute="_compute_payment_reference")
    student_id = fields.Many2one('student.management', string="Student")
    fee_structure_id = fields.Many2one('fees.structure', string="Fee Structure")
    total_amount = fields.Float(string="Total Amount", compute="_compute_total_amount", store=True)
    amount_paid = fields.Float(string="Amount Paid")
    amount_remaining = fields.Float(string="Amount Remaining", compute="_compute_remaining", store=True)
    reference_number = fields.Char(string="Reference Number")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('paid', 'Paid'),
        ('partially_paid', 'Partially Paid'),
        ('unpaid', 'Unpaid')
    ], string="Status", default='draft')
    payment_method = fields.Selection(
        [('cash', 'Cash'), ('bank_transfer', 'Bank Transfer'), ('cheque', 'Cheque'), ('telebirr', 'TeleBirr')],
        string="Payment Method")
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

    payment_date = fields.Date(string="Payment Date", default=fields.Date.context_today)

    has_discount = fields.Boolean(string="Has Discount")
    discount_percent = fields.Float(string="Discount %")
    discounted_amount = fields.Float(string="Discount Amount")

    has_scholarship = fields.Boolean(string="Has Scholarship")
    half_scholarship = fields.Boolean(string="Half Scholarship")
    full_scholarship = fields.Boolean(string="Full Scholarship")

    # invoice_id = fields.Many2one('account.move', string="Invoice", readonly=True)
    # payment_ids = fields.One2many('account.payment', 'fee_id', string="Payments")
    # invoice_state = fields.Selection(related='invoice_id.state', string="Invoice Status", readonly=True)

    @api.depends("student_id.name", "reference_number")
    def _compute_payment_reference(self):
        for rec in self:
            rec.payment_reference = f"{rec.student_id.name} - {rec.reference_number}" if rec.student_id and rec.reference_number else "New"

    # Apply Fee Structure
    @api.depends('fee_structure_id')
    def _compute_total_amount(self):
        for rec in self:
            if rec.fee_structure_id:
                # rec.fee_type = rec.fee_structure_id.name
                rec.total_amount = rec.fee_structure_id.amount

    @api.onchange('amount_paid')
    def _check_amount_paid(self):
        for rec in self:
            if rec.amount_paid > rec.total_amount:
                raise ValidationError('Amount paid cannot be greater than total amount.')

    # Apply discount
    @api.onchange('discount_percent', 'total_amount')
    def _onchange_discount_percent(self):
        for rec in self:
            if rec.discount_percent < 0 or rec.discount_percent > 100:
                return {
                    'warning': {
                        'title': 'Invalid Discount',
                        'message': 'Discount percent must be between 0 and 100.'
                    }
                }
            rec.discounted_amount = rec.total_amount * (1 - rec.discount_percent / 100) if rec.total_amount else 0

    # Compute remaining amount
    @api.depends('total_amount', 'amount_paid', 'has_discount', 'discounted_amount', 'half_scholarship',
                 'full_scholarship')
    def _compute_remaining(self):
        for rec in self:
            amount_due = rec.total_amount
            # Apply scholarship logic
            if rec.full_scholarship:
                amount_due = 0
            elif rec.half_scholarship:
                amount_due = rec.total_amount / 2

            # Apply discount (if exists)
            if rec.has_discount and rec.discount_percent > 0 and not rec.full_scholarship:
                amount_due = amount_due - (amount_due * rec.discount_percent / 100)

            # rec.amount_remaining = max(amount_due - (rec.amount_paid or 0.0), 0.0)
            rec.amount_remaining = amount_due - rec.amount_paid if amount_due > 0 else 0
            # Update state automatically
            # amount_due = total_amount after scholarship/discount
            if rec.amount_paid == amount_due and rec.total_amount > 0:
                rec.state = 'paid'
            elif 0 < rec.amount_paid < amount_due:
                rec.state = 'partially_paid'
            elif rec.amount_paid == 0 and amount_due > 0:
                rec.state = 'unpaid'
            else:
                rec.state = 'draft'

    def action_set_paid(self):
        self.write({'state': 'paid'})

    def action_set_partial(self):
        self.write({'state': 'partially_paid'})

    def action_set_unpaid(self):
        self.write({'state': 'unpaid'})

    def action_reset_draft(self):
        self.write({'state': 'draft'})
    #
    # def action_create_invoice(self):
    #     for rec in self:
    #         if not rec.fee_structure_id:
    #             raise ValidationError("Please select a Fee Structure before creating an invoice.")
    #
    #         # pick first linked parent with partner
    #         guardian = rec.student_id.parent_ids[:1]  # Take first parent
    #         if not guardian or not guardian.partner_id:
    #             raise ValidationError("The student has no guardian linked to a Partner for invoicing.")
    #
    #         # --- get income account ---
    #         account_id = rec.fee_structure_id.income_account_id.id
    #         if not account_id:
    #             account_id = rec.company_id.account_income_id.id
    #         _logger.info("Creating invoice line with account_id=%s for fee=%s", account_id, rec.payment_reference)
    #
    #         # Ensure there is a Product to use for invoicing
    #         school_fee_product = self.env['product.product'].search([('name', '=', 'School Fee')], limit=1)
    #         if not school_fee_product:
    #             school_fee_product = self.env['product.product'].create({
    #                 'name': 'School Fee',
    #                 'type': 'service',
    #                 'sale_ok': True,
    #                 'purchase_ok': False,
    #                 'invoice_policy': 'order',
    #             })
    #         if not account_id:
    #             raise ValidationError(
    #                 "No Income Account found. Please configure one in the Fee Structure or Company settings.")
    #
    #         move = self.env['account.move'].create({
    #             'move_type': 'out_invoice',
    #             'partner_id': guardian.partner_id.id,
    #             'invoice_date': fields.Date.context_today(self),
    #             'currency_id': rec.currency_id.id,
    #             'invoice_line_ids': [(0, 0, {
    #                 'name': rec.fee_structure_id.name,
    #                 'quantity': 1,
    #                 'price_unit': rec.total_amount,
    #                 'currency_id': rec.currency_id.id,
    #                 'account_id': account_id,
    #                 'product_id': school_fee_product.id,
    #                 'product_uom_id': school_fee_product.uom_id.id,
    #             })]
    #         })
    #
    #         rec.invoice_id = move.id
    #         rec.reference_number = move.name
    #         rec.message_post(body=f"Invoice {move.name} created for this fee.")
    #
    #         return {
    #             'type': 'ir.actions.act_window',
    #             'res_model': 'account.move',
    #             'view_mode': 'form',
    #             'res_id': move.id,
    #         }
    #
    # def action_view_invoice(self):
    #     self.ensure_one()
    #     if not self.invoice_id:
    #         raise ValidationError("No invoice linked to this fee.")
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'res_model': 'account.move',
    #         'view_mode': 'form',
    #         'res_id': self.invoice_id.id,
    #         'target': 'current',
    #     }

    # class AccountPayment(models.Model):
    #     _inherit = 'account.payment'
    #
    #     fee_id = fields.Many2one('fees.fees', string="Related Fee")
