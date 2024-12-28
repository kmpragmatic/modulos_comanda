/** @odoo-module */
import {patch} from "@web/core/utils/patch";
import {ProductListPage} from "@pos_self_order/app/pages/product_list_page/product_list_page";

patch(ProductListPage.prototype, {
    setup() {
        super.setup();

        if (!this.selfOrder.selectedCategoryId) {
            this.selfOrder.selectedCategoryId = 0;
        }
    },
    review() {
        this.router.navigate("product_list");
    }

});
