/** @odoo-module */
import {patch} from "@web/core/utils/patch";
import {CartPage} from "@pos_self_order/app/pages/cart_page/cart_page";

patch(CartPage.prototype, {
    setup() {
        super.setup();

        console.log("CartPage", this);
    }

});
