"""
Private Resource implementation for MCP server resources.

This module provides resource classes for accessing internal MCP server resources.
"""

from typing import Any, Dict, Optional
from .base import Resource, ResourceConfig


class ExamplePrivateResources(Resource):
    """Resource class for accessing private MCP server resources."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize ExamplePrivateResources with configuration parameters."""
        # Convert dict config to ResourceConfig if needed
        if isinstance(config, dict):
            # Extract resource configurations from the class config
            params = config.get("params") or {}
            self.resources_config = params.get("resources", [])
            self.class_name = config.get("name", "example_private_resources")
            self.class_description = config.get("description", "Example private resource types")
            
            # We'll store multiple resource configs for this class
            self.resource_instances = []
            for resource_config in self.resources_config:
                # Create ResourceConfig instance
                from .base import ResourceConfig, ResourceParameter, ResourceAccessType
                
                # Convert resource_parameters if they exist
                resource_params = []
                for param in resource_config.get("resource_parameters", []):
                    resource_params.append(ResourceParameter(**param))
                
                res_config = ResourceConfig(
                    name=resource_config["name"],
                    description=resource_config["description"],
                    type=resource_config["type"],
                    access=ResourceAccessType(resource_config["access"]),
                    uri=resource_config["uri"],
                    function=resource_config.get("function"),
                    resource_parameters=resource_params
                )
                self.resource_instances.append(res_config)
        else:
            # Single resource configuration
            super().__init__(config)
            self.resource_instances = [config]
    
    async def get_content(self, parameters: Optional[Dict[str, Any]] = None) -> str:
        """Get content for the resource."""
        # This method works for single resource instance
        if len(self.resource_instances) == 1:
            return await self._get_mcp_content(self.resource_instances[0], parameters)
        else:
            # For multi-resource classes, this would need resource name parameter
            raise ValueError("Multi-resource classes need specific resource selection")
    
    async def get_resource_content(self, resource_name: str, parameters: Optional[Dict[str, Any]] = None) -> str:
        """Get content for a specific named resource."""
        resource_config = None
        for res in self.resource_instances:
            if res.name == resource_name:
                resource_config = res
                break
        
        if not resource_config:
            raise ValueError(f"Resource '{resource_name}' not found")
        
        return await self._get_mcp_content(resource_config, parameters)
    
    async def _get_mcp_content(self, resource_config: ResourceConfig, parameters: Optional[Dict[str, Any]] = None) -> str:
        """Internal method to get MCP server content."""
        if not resource_config.function:
            raise ValueError(f"No function specified for mcp_server resource '{resource_config.name}'")
        
        # Get the function method
        function_name = resource_config.function
        if hasattr(self, function_name):
            function_method = getattr(self, function_name)
            return await function_method(parameters or {})
        else:
            raise ValueError(f"Function '{function_name}' not found in resource class")
    
    async def _sample_parameterized_resource(self, parameters: Dict[str, Any]) -> str:
        """
        Sample parameterized resource function.
        Returns different text based on the client parameter.
        
        Args:
            parameters: Dictionary containing the 'client' parameter
            
        Returns:
            str: Different text based on client value
        """
        client = parameters.get("client", "").lower()
        
        if client == "acme":
            return "This is the roadrunner client"
        elif client == "bigrock":
            return "We make tools to smash birds"
        else:
            return f"Unknown client: {client}. Available clients: acme, bigrock"
    
    def get_resources(self) -> list:
        """Get list of all resources managed by this class."""
        return [res.to_mcp_def() for res in self.resource_instances]