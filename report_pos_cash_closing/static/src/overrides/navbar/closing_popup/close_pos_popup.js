/** @odoo-module */
import {ClosePosPopup} from "@point_of_sale/app/navbar/closing_popup/closing_popup";
import {patch} from "@web/core/utils/patch";
import {useService} from "@web/core/utils/hooks";

patch(ClosePosPopup.prototype, {

    setup() {
        super.setup();
        this.actionService = useService("action");
    },



    async downloadSalesReport() {
        const action = await this.orm.call("pos.daily.sales.reports.wizard", "create_report_from_ui", [this.pos.pos_session.id]);
        this.actionService.doAction(action);
        // return this.create_report_close_custom();
        // console.log("downloadSalesReport", this);
        // let report_vals = await
        // console.log("report", report_vals);
        // var report = this.report.doAction("point_of_sale.sale_details_report", [this.pos.pos_session.id]);
        // console.log("report", report);
        // if (report.success) {
        //     return this.report.doAction("report_pos_cash_closing.paperformat_cash_closing_custom", [report.report_id]);
        // }
        // return this.report.doAction("point_of_sale.sale_details_report", [this.pos.pos_session.id]);

    },
});
