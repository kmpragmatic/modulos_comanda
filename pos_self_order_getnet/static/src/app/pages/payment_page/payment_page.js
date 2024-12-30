/** @odoo-module */
import {useService} from "@web/core/utils/hooks";
import {patch} from "@web/core/utils/patch";
import {PaymentPage} from "@pos_self_order/app/pages/payment_page/payment_page";

patch(PaymentPage.prototype, {
    setup() {
        super.setup();
        this.timeoutId = null;
        this.busService = this.env.services.bus_service;
        this.orm = useService("orm");
        this.notification = useService("notification");
        this.custom_uuid = null;
    },
    async startPayment() {
        var self = this;
        const paymentMethod = this.selfOrder.pos_payment_methods.find(
            (p) => p.id === this.state.paymentMethodId
        );
        if (paymentMethod.use_payment_terminal !== "getnet") {
            return await super.startPayment(...arguments);
        }
        this.selfOrder.paymentError = false;
        try {
            this.env.services.ui.block();
            const result = await this.rpc(`/kiosk/payment/${this.selfOrder.pos_config_id}/kiosk`, {
                order: this.selfOrder.currentOrder,
                access_token: this.selfOrder.access_token,
                payment_method_id: this.state.paymentMethodId,
            });
            console.log("result-result", result);
            this.env.services.ui.unblock();
            if (!result.payment_status.success) {
                this.notification.add(result.payment_status.error, {
                    type: "danger",
                });
                return;
            }
            self.order = result.order;
            self.custom_uuid = result.payment_status.custom_uuid;
            self.eventBusListener();
            self.executeWithTimeout(result.payment_status.validation_delay * 1000);
            const order = result.order;

        } catch (error) {
            this.selfOrder.handleErrorNotification(error);
            this.selfOrder.paymentError = true;
        }
    },
    eventBusListener() {
        const handlerTransactionCreation = async ({detail: notifications}) => {
            console.log("Evento recibido:", notifications);
        };

        console.log("agregamos el listener");
        // this.busService.addEventListener('notification', handlerTransactionCreation);
        // this.busService.addEventListener('PUSHY_NOTIFICATION_PAYMENT', handlerTransactionCreation);
        this.busService.addEventListener('SIMPLE_EVENT', (event) => {
            console.log("Evento SIMPLE recibido:", event);
        });

        // this.busService.startPolling();

    },
    async validateStatusPayment() {
        let statusvals = await this.getStatusPayment();
        console.log("statusvals", statusvals);
        if (statusvals.code === false) {
            return;
        }
        if (statusvals.code === '0') {
            this.notification.add('Pago realizado', {type: "success"});
            this.selfOrder.updateOrderFromServer(this.order);
            this.selfOrder.finalizeOrder();
        } else {
            this.notification.add('Pago no realizado', {
                type: "danger",
            });
        }

    },
    executeWithTimeout(delay) {
        var self = this;
        setInterval(() => self.validateStatusPayment(), 5000);
        // this.timeoutId = setTimeout(() => {
        //     try {
        //         self.validateStatusPayment();
        //         self.cancelTimeout();
        //     } catch (error) {
        //         console.error('Ocurrió un error al ejecutar el callback:', error);
        //         self.cancelTimeout();
        //     }
        // }, delay);
    },
    cancelTimeout() {
        // if (this.timeoutId) {
        //     clearTimeout(this.timeoutId);
        //     this.timeoutId = null;
        // }
    },
    async getStatusPayment() {
        console.log("this.custom_uuid", this.custom_uuid);
        return await this.orm.call("transaction.response", "get_payment_uuid_info", [this.custom_uuid]);
    }

});
