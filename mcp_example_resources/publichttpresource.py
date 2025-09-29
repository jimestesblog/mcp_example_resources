"""
HTTP Resource implementation for public resources.

This module provides resource classes for accessing public HTTP/HTTPS resources.
"""

import httpx
import asyncio
from typing import Any, Dict, Optional
from .base import Resource, ResourceConfig


class HttpResource(Resource):
    """Resource class for accessing public HTTP/HTTPS resources."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize HttpResource with configuration parameters."""
        # Convert dict config to ResourceConfig if needed
        if isinstance(config, dict):
            # Extract resource configurations from the class config
            params = config.get("params") or {}
            self.resources_config = params.get("resources", [])
            self.class_name = config.get("name", "http_resources")
            self.class_description = config.get("description", "Public HTTP resource types")
            
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
        """Fetch content from HTTP/HTTPS URL."""
        # This method works for single resource instance
        if len(self.resource_instances) == 1:
            return await self._fetch_http_content(self.resource_instances[0], parameters)
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
        
        return await self._fetch_http_content(resource_config, parameters)
    
    async def _fetch_http_content(self, resource_config: ResourceConfig, parameters: Optional[Dict[str, Any]] = None) -> str:
        """Internal method to fetch HTTP content."""
        url = resource_config.uri
        
        # Substitute parameters in URL if provided
        if parameters:
            validated_params = self.validate_parameters(parameters)
            url = self.substitute_parameters(url, validated_params)
        
        # Validate URL scheme
        if not url.startswith(('http://', 'https://')):
            raise ValueError(f"Invalid URL scheme for public resource: {url}")
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                if response.status_code == 200:
                    content = response.text
                    return content
                else:
                    raise ValueError(f"HTTP error {response.status_code} when fetching {url}")
        except httpx.RequestError as e:
            raise ValueError(f"Failed to fetch resource from {url}: {str(e)}")
        except Exception as e:
            raise ValueError(f"Unexpected error fetching {url}: {str(e)}")
    
    def get_resources(self) -> list:
        """Get list of all resources managed by this class."""
        return [res.to_mcp_def() for res in self.resource_instances]