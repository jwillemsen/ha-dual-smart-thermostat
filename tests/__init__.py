"""dual_smart_thermostat tests."""

import datetime
import logging

from homeassistant.components.climate import (
    DOMAIN as CLIMATE,
    PRESET_ACTIVITY,
    PRESET_AWAY,
    PRESET_BOOST,
    PRESET_COMFORT,
    PRESET_ECO,
    PRESET_HOME,
    PRESET_SLEEP,
    STATE_OFF,
    STATE_ON,
    HVACMode,
)
from homeassistant.const import SERVICE_TURN_OFF, SERVICE_TURN_ON, UnitOfTemperature
import homeassistant.core as ha
from homeassistant.core import HomeAssistant, callback
from homeassistant.setup import async_setup_component
from homeassistant.util.unit_system import METRIC_SYSTEM
import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.dual_smart_thermostat.const import DOMAIN

from . import common

_LOGGER = logging.getLogger(__name__)


@pytest.fixture
async def setup_comp_1(hass: HomeAssistant):
    """Initialize components."""
    hass.config.units = METRIC_SYSTEM
    assert await async_setup_component(hass, "homeassistant", {})
    await hass.async_block_till_done()


@pytest.fixture
async def setup_comp_heat(hass):
    """Initialize components."""
    hass.config.units = METRIC_SYSTEM
    assert await async_setup_component(
        hass,
        CLIMATE,
        {
            "climate": {
                "platform": DOMAIN,
                "name": "test",
                "cold_tolerance": 2,
                "hot_tolerance": 4,
                "heater": common.ENT_SWITCH,
                "target_sensor": common.ENT_SENSOR,
                "initial_hvac_mode": HVACMode.HEAT,
            }
        },
    )
    await hass.async_block_till_done()


@pytest.fixture
async def setup_comp_heat_floor_sensor(hass):
    """Initialize components."""
    hass.config.units = METRIC_SYSTEM
    assert await async_setup_component(
        hass,
        CLIMATE,
        {
            "climate": {
                "platform": DOMAIN,
                "name": "test",
                "cold_tolerance": 2,
                "hot_tolerance": 4,
                "heater": common.ENT_SWITCH,
                "target_sensor": common.ENT_SENSOR,
                "floor_sensor": common.ENT_FLOOR_SENSOR,
                "initial_hvac_mode": HVACMode.HEAT,
            }
        },
    )
    await hass.async_block_till_done()


@pytest.fixture
async def setup_comp_heat_cycle(hass):
    """Initialize components."""
    hass.config.units = METRIC_SYSTEM
    assert await async_setup_component(
        hass,
        CLIMATE,
        {
            "climate": {
                "platform": DOMAIN,
                "name": "test",
                "cold_tolerance": 2,
                "hot_tolerance": 4,
                "heater": common.ENT_SWITCH,
                "target_sensor": common.ENT_SENSOR,
                "min_cycle_duration": datetime.timedelta(minutes=10),
                "initial_hvac_mode": HVACMode.HEAT,
            }
        },
    )
    await hass.async_block_till_done()


@pytest.fixture
async def setup_comp_heat_cycle_precision(hass):
    """Initialize components."""
    hass.config.units = METRIC_SYSTEM
    assert await async_setup_component(
        hass,
        CLIMATE,
        {
            "climate": {
                "platform": DOMAIN,
                "name": "test",
                "cold_tolerance": 2,
                "hot_tolerance": 4,
                "heater": common.ENT_SWITCH,
                "target_sensor": common.ENT_SENSOR,
                "min_cycle_duration": datetime.timedelta(minutes=10),
                "keep_alive": datetime.timedelta(minutes=10),
                "initial_hvac_mode": HVACMode.HEAT,
                "precision": 0.1,
            }
        },
    )
    await hass.async_block_till_done()


@pytest.fixture
async def setup_comp_heat_ac_cool(hass):
    """Initialize components."""
    hass.config.units = METRIC_SYSTEM
    assert await async_setup_component(
        hass,
        CLIMATE,
        {
            "climate": {
                "platform": DOMAIN,
                "name": "test",
                "cold_tolerance": 2,
                "hot_tolerance": 4,
                "ac_mode": True,
                "heater": common.ENT_SWITCH,
                "target_sensor": common.ENT_SENSOR,
                "initial_hvac_mode": HVACMode.COOL,
                PRESET_AWAY: {"temperature": 30},
            }
        },
    )
    await hass.async_block_till_done()


@pytest.fixture
async def setup_comp_heat_ac_cool_presets(hass):
    """Initialize components."""
    hass.config.units = METRIC_SYSTEM
    assert await async_setup_component(
        hass,
        CLIMATE,
        {
            "climate": {
                "platform": DOMAIN,
                "name": "test",
                "cold_tolerance": 2,
                "hot_tolerance": 4,
                "ac_mode": True,
                "heater": common.ENT_SWITCH,
                "target_sensor": common.ENT_SENSOR,
                "initial_hvac_mode": HVACMode.COOL,
                PRESET_AWAY: {"temperature": 16},
                PRESET_ACTIVITY: {"temperature": 21},
                PRESET_COMFORT: {"temperature": 20},
                PRESET_ECO: {"temperature": 18},
                PRESET_HOME: {"temperature": 19},
                PRESET_SLEEP: {"temperature": 17},
                PRESET_BOOST: {"temperature": 10},
                "anti_freeze": {"temperature": 5},
            }
        },
    )
    await hass.async_block_till_done()


@pytest.fixture
async def setup_comp_heat_ac_cool_cycle(hass):
    """Initialize components."""
    hass.config.units = METRIC_SYSTEM
    hass.config.temperature_unit = UnitOfTemperature.CELSIUS
    assert await async_setup_component(
        hass,
        CLIMATE,
        {
            "climate": {
                "platform": DOMAIN,
                "name": "test",
                "cold_tolerance": 0.3,
                "hot_tolerance": 0.3,
                "ac_mode": True,
                "heater": common.ENT_SWITCH,
                "target_sensor": common.ENT_SENSOR,
                "initial_hvac_mode": HVACMode.COOL,
                "min_cycle_duration": datetime.timedelta(minutes=10),
                PRESET_AWAY: {"temperature": 30},
            }
        },
    )
    await hass.async_block_till_done()


@pytest.fixture
async def setup_comp_heat_ac_cool_cycle_kepp_alive(hass):
    """Initialize components."""
    hass.config.units = METRIC_SYSTEM
    hass.config.temperature_unit = UnitOfTemperature.CELSIUS
    assert await async_setup_component(
        hass,
        CLIMATE,
        {
            "climate": {
                "platform": DOMAIN,
                "name": "test",
                "cold_tolerance": 0.3,
                "hot_tolerance": 0.3,
                "ac_mode": True,
                "heater": common.ENT_SWITCH,
                "target_sensor": common.ENT_SENSOR,
                "initial_hvac_mode": HVACMode.COOL,
                "min_cycle_duration": datetime.timedelta(minutes=10),
                "keep_alive": datetime.timedelta(minutes=10),
                PRESET_AWAY: {"temperature": 30},
            }
        },
    )
    await hass.async_block_till_done()


@pytest.fixture
async def setup_comp_heat_presets(hass):
    """Initialize components."""
    hass.config.units = METRIC_SYSTEM
    assert await async_setup_component(
        hass,
        CLIMATE,
        {
            "climate": {
                "platform": DOMAIN,
                "name": "test",
                "cold_tolerance": 2,
                "hot_tolerance": 4,
                "heater": common.ENT_HEATER,
                "target_sensor": common.ENT_SENSOR,
                "initial_hvac_mode": HVACMode.HEAT,
                PRESET_AWAY: {"temperature": 16},
                PRESET_ACTIVITY: {"temperature": 21},
                PRESET_COMFORT: {"temperature": 20},
                PRESET_ECO: {"temperature": 18},
                PRESET_HOME: {"temperature": 19},
                PRESET_SLEEP: {"temperature": 17},
                PRESET_BOOST: {"temperature": 24},
                "anti_freeze": {"temperature": 5},
            }
        },
    )
    await hass.async_block_till_done()


@pytest.fixture
async def setup_comp_cool(hass):
    """Initialize components."""
    hass.config.units = METRIC_SYSTEM
    assert await async_setup_component(
        hass,
        CLIMATE,
        {
            "climate": {
                "platform": DOMAIN,
                "name": "test",
                "cold_tolerance": 2,
                "hot_tolerance": 4,
                "cooler": common.ENT_COOLER,
                "target_sensor": common.ENT_SENSOR,
                "initial_hvac_mode": HVACMode.COOL,
            }
        },
    )
    await hass.async_block_till_done()


@pytest.fixture
async def setup_comp_dual(hass):
    """Initialize components."""
    hass.config.units = METRIC_SYSTEM
    assert await async_setup_component(
        hass,
        CLIMATE,
        {
            "climate": {
                "platform": DOMAIN,
                "name": "test",
                "cold_tolerance": 2,
                "hot_tolerance": 4,
                "heat_cool_mode": True,
                "heater": common.ENT_HEATER,
                "cooler": common.ENT_COOLER,
                "target_sensor": common.ENT_SENSOR,
                "initial_hvac_mode": HVACMode.HEAT_COOL,
            }
        },
    )
    await hass.async_block_till_done()


@pytest.fixture
async def setup_comp_dual_presets(hass):
    """Initialize components."""
    hass.config.units = METRIC_SYSTEM
    assert await async_setup_component(
        hass,
        CLIMATE,
        {
            "climate": {
                "platform": DOMAIN,
                "name": "test",
                "cold_tolerance": 2,
                "hot_tolerance": 4,
                "heat_cool_mode": True,
                "heater": common.ENT_HEATER,
                "cooler": common.ENT_COOLER,
                "target_sensor": common.ENT_SENSOR,
                "initial_hvac_mode": HVACMode.HEAT_COOL,
                PRESET_AWAY: {
                    "temperature": 16,
                    "target_temp_low": 16,
                    "target_temp_high": 30,
                },
                PRESET_COMFORT: {
                    "temperature": 20,
                    "target_temp_low": 20,
                    "target_temp_high": 27,
                },
                PRESET_ECO: {
                    "temperature": 18,
                    "target_temp_low": 18,
                    "target_temp_high": 29,
                },
                PRESET_HOME: {
                    "temperature": 19,
                    "target_temp_low": 19,
                    "target_temp_high": 23,
                },
                PRESET_SLEEP: {
                    "temperature": 17,
                    "target_temp_low": 17,
                    "target_temp_high": 24,
                },
                PRESET_ACTIVITY: {
                    "temperature": 21,
                    "target_temp_low": 21,
                    "target_temp_high": 28,
                },
                "anti_freeze": {
                    "temperature": 5,
                    "target_temp_low": 5,
                    "target_temp_high": 32,
                },
            }
        },
    )
    await hass.async_block_till_done()


async def setup_component(hass: HomeAssistant, mock_config: dict) -> MockConfigEntry:
    """Initialize knmi for tests."""
    config_entry = MockConfigEntry(domain=DOMAIN, data=mock_config, entry_id="test")
    config_entry.add_to_hass(hass)

    assert await async_setup_component(hass=hass, domain=DOMAIN, config=mock_config)
    await hass.async_block_till_done()

    return config_entry


def setup_sensor(hass: HomeAssistant, temp):
    """Set up the test sensor."""
    hass.states.async_set(common.ENT_SENSOR, temp)


def setup_floor_sensor(hass: HomeAssistant, temp):
    """Set up the test sensor."""
    hass.states.async_set(common.ENT_FLOOR_SENSOR, temp)


def setup_boolean(hass: HomeAssistant, entity, state):
    """Set up the test sensor."""
    hass.states.async_set(entity, state)


def setup_switch(hass, is_on):
    """Set up the test switch."""
    hass.states.async_set(common.ENT_SWITCH, STATE_ON if is_on else STATE_OFF)
    calls = []

    @callback
    def log_call(call):
        """Log service calls."""
        calls.append(call)

    hass.services.async_register(ha.DOMAIN, SERVICE_TURN_ON, log_call)
    hass.services.async_register(ha.DOMAIN, SERVICE_TURN_OFF, log_call)

    return calls
