import { rpc } from "@web/core/network/rpc";
import { registry } from "@web/core/registry";
import { memoize } from "@web/core/utils/functions";
import { reactive } from "@odoo/owl";

const statisticsService = {
  start() {
    const statistics = reactive({ isReady: false });

    async function loadData() {
      const updates = await rpc("/awesome_dashboard/statistics");
      Object.assign(statistics, updates, { isReady: true });
    }

    setInterval(loadData, 5 * 1000);

    return statistics;
  },
};

registry
  .category("services")
  .add("awesome_dashboard.statistics", statisticsService);
