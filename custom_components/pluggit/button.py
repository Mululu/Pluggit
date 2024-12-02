"""Button integration."""

import logging

from homeassistant.components.button import ButtonEntity
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .device import PluggitEntity, Device
from .device_map import BUTTONS, PluggitButtonEntityDescription

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, config_entry, async_add_entities):
    """."""
    device = hass.data[DOMAIN][config_entry.entry_id]

    entities = []
    for description in BUTTONS:
        if await device.async_install_entity(description):
            button = PluggitButton(device, description)
            entities.append(button)

    async_add_entities(entities, update_before_add=True)
    return True


class PluggitButton(ButtonEntity, PluggitEntity):
    """Pluggit button."""

    def __init__(
        self,
        device: Device,
        description: PluggitButtonEntityDescription,
    ) -> None:
        """Init button."""
        super().__init__(device)
        self._device = device
        self._attr_has_entity_name = True
        self.entity_description: PluggitButtonEntityDescription = description

    async def async_press(self) -> None:
        """Handle the button press."""

        if self.entity_description.state_entity:
            value = self._device.data.get(self.key, None)
        else:
            value = self.entity_description.state

        if value:
            await self._device.write_holding_registers(
                description=self.entity_description, value=value
            )
