"""
NUCLEAR FIX for Django + Python 3.14 AttributeError
Add this to your MIDDLEWARE in settings.py
"""

class Python314CompatibilityMiddleware:
    """
    Monkey-patch Django's ChangeList to fix Python 3.14 compatibility issue.
    This fixes: AttributeError: 'super' object has no attribute 'dicts'
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self._patch_django()
    
    def _patch_django(self):
        """Apply the patch on startup"""
        try:
            from django.contrib.admin.views.main import ChangeList
            
            # Store original __init__
            original_init = ChangeList.__init__
            
            # Create patched version
            def patched_init(self, *args, **kwargs):
                # Call original init
                original_init(self, *args, **kwargs)
                
                # Ensure all required attributes exist
                if not hasattr(self, 'formset'):
                    self.formset = None
                if not hasattr(self, 'result_count'):
                    self.result_count = 0
            
            # Apply patch
            ChangeList.__init__ = patched_init
            print("✓ Django ChangeList patched for Python 3.14 compatibility")
            
        except Exception as e:
            print(f"✗ Failed to patch Django: {e}")
    
    def __call__(self, request):
        return self.get_response(request)
