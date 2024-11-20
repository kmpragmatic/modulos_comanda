/** @odoo-module */
import {patch} from "@web/core/utils/patch";
import {PosBus} from "@point_of_sale/app/bus/pos_bus_service";

patch(PosBus.prototype, {
    dispatch(message) {
        super.dispatch(...arguments);
        if (message.type === "PUSHY_NOTIFICATION_PAYMENT") {
            const order = this.pos.get_order();
            console.log("order", order);
            console.log("THIS", this);
            console.log("PUSHY_NOTIFICATION_PAYMENT", message);
            alert(message.payload.response);
            this.pos.env.services.ui.unblock();
        }
    },
});
