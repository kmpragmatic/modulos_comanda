/** @odoo-module */
import { register_payment_method } from "@point_of_sale/app/store/pos_store";
import { Payment } from "@point_of_sale/app/store/models";
import { patch } from "@web/core/utils/patch";


patch(Payment.prototype, {
    setup() {
        super.setup(...arguments);
    },
    init_from_JSON(json) {
        super.init_from_JSON(...arguments);
        this.custom_uuid = json.custom_uuid;
    },
    set_custom_uuid(custom_uuid) {
        this.custom_uuid = custom_uuid;
    },
});