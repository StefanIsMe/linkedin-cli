"""Allow: python3 -m linkedin_api.cli"""
from .cli import main
sys = __import__("sys")
sys.exit(main())
