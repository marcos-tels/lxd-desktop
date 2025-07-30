from dataclasses import dataclass
import yaml


@dataclass
class ProfileDevice:
    """
    Represents a device attached to a LXD profile.

    Attributes:
        name (str): The device's name.
        type (str): The type of the device (e.g., 'nic', 'disk').
        extra (dict): Additional configuration fields for the device.
    """
    name: str
    type: str
    extra: dict

@dataclass
class CreateProfileDTO:
    """
    Data Transfer Object for creating an LXD profile.

    Attributes:
        name (str): The name of the profile.
        description (str): A brief description of the profile.
        config (dict): Configuration options for the profile.
        devices (dict): A dictionary of profile devices, where each key is a device name and the value is a ProfileDevice object.
        used_by (list): A list of resource URIs that are using this profile.
    """
    name: str
    description: str
    config: dict
    devices: list
    used_by: list
    
    @classmethod
    def from_yaml(cls, yaml_str: str):
        data = yaml.safe_load(yaml_str)
        devices = [
            ProfileDevice(
                name=dev_name,
                type=dev_data.pop("type"),
                extra=dev_data
            )
            
            for dev_name, dev_data in data["devices"].items()
        ]
        return cls(
            name=data["name"],
            description=data["description"],
            config=data["config"],
            devices=devices,
            used_by=data["used_by"]
        )

    def to_yaml(self) -> str:
        devices_dict = {
            dev.name: {"type": dev.type, **dev.extra}
            for dev in self.devices
        }
        return yaml.dump({
            "name": self.name,
            "description": self.description,
            "config": self.config,
            "devices": devices_dict,
            "used_by": self.used_by
        }, sort_keys=False)

@dataclass
class UpdateProfileDTO:
    """
    Data Transfer Object (DTO) for updating an existing LXD profile.

    Attributes:
        name (str): The updated name of the profile.
        description (str): The updated description of the profile.
        config (dict): A dictionary containing updated configuration options.
        devices (list): A list of updated devices,
            where each key is a device name and the value is a ProfileDevice instance.
        used_by (list): A list of instance URIs that are using this profile.
            This field is generally optional during updates, but may be relevant for internal tracking.
    """
    name: str
    description: str
    config: dict
    devices: list
    used_by: list

    @classmethod
    def from_yaml(cls, yaml_str: str):
        data = yaml.safe_load(yaml_str)
        devices = [
            ProfileDevice(
                name=dev_name,
                type=dev_data.pop("type"),
                extra=dev_data
            )
            for dev_name, dev_data in data["devices"].items()
        ]
        return cls(
            name=data["name"],
            description=data["description"],
            config=data["config"],
            devices=devices,
            used_by=data["used_by"]
        )

    def to_yaml(self) -> str:
        devices_dict = {
            dev.name: {"type": dev.type}
            for dev in self.devices
        }
        return yaml.dump({
            "name": self.name,
            "description": self.description,
            "config": self.config,
            "devices": devices_dict,
            "used_by": self.used_by
        }, sort_keys=False)

@dataclass
class DetailedProfileDTO:
    """
    Data Transfer Object (DTO) representing detailed information about an LXD profile.

    Attributes:
        name (str): The name of the profile.
        description (str): A human-readable description of the profile.
        config (dict): A dictionary containing the profile's configuration options.
        devices (list): A list of devices associated with the profile,
            where each key is the device name and the value is a ProfileDevice instance.
        used_by (list): A list of instance URIs that are using this profile.
        """
    name: str
    description: str
    config: dict
    devices: list
    used_by: list


@dataclass
class ProfileDTO:
    """
    Base Data Transfer Object (DTO) representing common attributes of an LXD profile.

    This class serves as a base structure to be reused by other more specific profile DTOs.

    Attributes:
        name (str): The name of the profile.
        description (str): A human-readable description of the profile.
        used_by (int): A entire of instance URIs that are using this profile.
    """
    name: str
    description: str
    used_by: int
