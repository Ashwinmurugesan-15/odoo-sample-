
    @api.depends('type')
    def _compute_is_partner_visible(self):
        for lead in self:
            lead.is_partner_visible = True
