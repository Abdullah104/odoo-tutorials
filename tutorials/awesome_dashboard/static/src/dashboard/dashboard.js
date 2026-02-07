import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";
import { DashboardItem } from "./dashboard_item/dashboard_item";
import { browser } from "@web/core/browser/browser";
import { ConfigurationDialog } from "./configuration_dialog/configuration_dialog";

class AwesomeDashboard extends Component {
  static template = "awesome_dashboard.AwesomeDashboard";
  static components = { Layout, DashboardItem };

  setup() {
    this.action = useService("action");
    this.statistics = useState(useService("awesome_dashboard.statistics"));
    this.dialog = useService("dialog");
    this.items = registry.category("awesome_dashboard").getAll();
    this.state = useState({
      disabledItems:
        browser.localStorage.getItem("disabledDashboardItems")?.split(",") ||
        [],
    });
  }

  openCustomers() {
    this.action.doAction("base.action_partner_form");
  }

  openLeads(activity) {
    this.action.doAction({
      type: "ir.actions.act_window",
      name: _t("Leads"),
      target: "current",
      res_id: activity.res_id,
      res_model: "crm.lead",
      views: [[false, "form"]],
    });
  }

  updateConfiguration(newDisabledItems) {
    this.state.disabledItems = newDisabledItems;
  }

  openConfiguration() {
    this.dialog.add(ConfigurationDialog, {
      items: this.items,
      disabledItems: this.state.disabledItems,
      onUpdateConfiguration: this.updateConfiguration.bind(this),
    });
  }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
