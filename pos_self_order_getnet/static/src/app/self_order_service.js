/** @odoo-module */
import { patch } from "@web/core/utils/patch";
import { SelfOrder } from "@pos_self_order/app/self_order_service";
import { Stripe, StripeError } from "@pos_self_order_stripe/app/stripe";

patch(SelfOrder.prototype, {
    async setup() {
        await super.setup(...arguments);

    },
});
