"""
MCP Example Resources Package

This package provides example resource implementations for MCP Server applications,
including public HTTP resources and private MCP server resources with parameterization.
"""

from .base import Resource, ResourceConfig, ResourceParameter, ResourceAccessType
from .publichttpresource import HttpResource
from .privateresourceexample import ExamplePrivateResources

__version__ = "0.1.0"
__all__ = [
    "Resource", 
    "ResourceConfig", 
    "ResourceParameter", 
    "ResourceAccessType",
    "HttpResource", 
    "ExamplePrivateResources"
]