#!/usr/bin/env python3

import sys

sys.path.append("lib")

from ops.charm import CharmBase
from ops.main import main
from ops.model import (
    ActiveStatus,
    BlockedStatus,
    MaintenanceStatus,
    WaitingStatus,
    ModelError,
)

class VnfPolicyCharm(CharmBase):
    def __init__(self, *args):
        super().__init__(*args)

        # Register all of the events we want to observe
        for event in (
            # Charm events
            self.on.install,
            self.on.upgrade_charm,
            # Charm actions (primitives)
            self.on.set_policy_action,
        ):
            self.framework.observe(event, self)

    def on_install(self, event):
        """Called when the charm is being installed"""
        unit = self.model.unit

        unit.status = ActiveStatus()

    def on_upgrade_charm(self, event):
        """Upgrade the charm."""
        unit = self.model.unit

        # Mark the unit as under Maintenance.
        unit.status = MaintenanceStatus("Upgrading charm")

        self.on_install(event)

        # When maintenance is done, return to an Active state
        unit.status = ActiveStatus()

    ####################
    # NS Charm methods #
    ####################

    def on_set_policy_action(self, event):
        user_id = event.params["user_id"]
        bw = event.params["bw"]
        qos = event.params["qos"]

        # If this were a functional vnf, you would perform your operation here
        # and may return a value to indicate success or failure.
        event.set_results({"updated": True})


if __name__ == "__main__":
    main(VnfPolicyCharm)

