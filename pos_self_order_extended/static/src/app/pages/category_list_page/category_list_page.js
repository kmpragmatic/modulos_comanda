/** @odoo-module */
import {Component, useEffect, useRef, useState} from "@odoo/owl";
import {useSelfOrder} from "@pos_self_order/app/self_order_service";
import {useService, useChildRef} from "@web/core/utils/hooks";
import {CancelPopup} from "@pos_self_order/app/components/cancel_popup/cancel_popup";
import {_t} from "@web/core/l10n/translation";
import {OrderWidget} from "@pos_self_order/app/components/order_widget/order_widget";

export class CategoryListPage extends Component {
    static template = "pos_self_order_extended.CategoryListPage";
    static components = {OrderWidget};

    setup() {

        this.selfOrder = useSelfOrder();
        this.categoryList = useRef("categoryList");
        this.router = useService("router");
    }

    selectCategory(categoryId) {
        this.selfOrder.selectedCategoryId = categoryId;
        this.router.navigate("product_list_by_category");
    }

    review() {
        this.router.navigate("cart");
    }


    goBack() {
        if (this.selfOrder.config.self_ordering_mode !== "kiosk") {
            this.router.navigate("default");
            return;
        }

        this.dialog.add(CancelPopup, {
            title: _t("Cancel order"),
            confirm: () => {
                this.router.navigate("default");
            },
        });
    }
}
