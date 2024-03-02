import dataclasses


@dataclasses.dataclass
class DancePic:
    dance_J: str = dataclasses.field(default_factory=str)
    dance_K: str = dataclasses.field(default_factory=str)
    dance_L: str = dataclasses.field(default_factory=str)
    dance_Down: str = dataclasses.field(default_factory=str)
    dance_Up: str = dataclasses.field(default_factory=str)
    dance_Left: str = dataclasses.field(default_factory=str)
    dance_Right: str = dataclasses.field(default_factory=str)


@dataclasses.dataclass
class WhzDancePic:
    dance_Down: str = dataclasses.field(default_factory=str)
    dance_Up: str = dataclasses.field(default_factory=str)
    dance_Left: str = dataclasses.field(default_factory=str)
    dance_Right: str = dataclasses.field(default_factory=str)


@dataclasses.dataclass
class DmDll:
    dll_dm: str = dataclasses.field(default_factory=str)
    dll_dm_reg: str = dataclasses.field(default_factory=str)


@dataclasses.dataclass
class GhostDll:
    dll_ghost: str = dataclasses.field(default_factory=str)
