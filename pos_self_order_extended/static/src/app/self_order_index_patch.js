/** @odoo-module */
import {patch} from "@web/core/utils/patch";
import selfOrderModule from "@pos_self_order/app/self_order_index";
import {CategoryListPage} from "@pos_self_order_extended/app/pages/category_list_page/category_list_page";

const selfOrderIndex = selfOrderModule.selfOrderIndex;


patch(selfOrderIndex, {

    components: {
        ...selfOrderIndex.components,
        CategoryListPage,
    }

});
// patch(selfOrderIndex.prototype, {
//     setup() {
//         super.setup();
//         console.log("this.components", this.components);
//         // Agrega tu funcionalidad personalizada
//         console.log("selfOrderIndex sobrescrito correctamente");
//     },
//
//
// });
