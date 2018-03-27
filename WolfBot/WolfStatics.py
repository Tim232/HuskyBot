from enum import Enum, IntEnum


class Colors(IntEnum):
    PRIMARY = 0x007BFF
    SECONDARY = 0x6C757D
    SUCCESS = 0x28A745
    DANGER = 0xDC3545
    WARNING = 0xFFC107
    INFO = 0x17A2B8

    # Shortcuts
    ERROR = DANGER


class ChannelKeys(str, Enum):
    STAFF_LOG = "logs"
    STAFF_HUB = "modChannel"
    STAFF_ALERTS = "staffAlerts"
    PUBLIC_LOG = "audit"


class Emojis:
    NO_ENTRY = "\uD83D\uDEAB"
    TRIANGLE = "\u26A0\uFE0F"
    DOOR = "\uD83D\uDEAA"
    SUNRISE = "\uD83C\uDF04"
    WOLF = "\uD83D\uDC3A"
    PARTY = "\uD83C\uDF89"
    BOMB = "\uD83D\uDCA3"
    UNLOCK = "\uD83D\uDD13"

    # Mod shortcuts
    BAN = NO_ENTRY
    WARNING = TRIANGLE
    UNBAN = UNLOCK

