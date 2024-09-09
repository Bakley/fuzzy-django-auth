import json
from rest_framework.renderers import JSONRenderer

class UserJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):
        # Ensure data is a dictionary before proceeding
        if isinstance(data, dict):
            errors = data.get('errors', None) or data.get('non_field_errors', None)
            
            # Let the default JSONRenderer handle error responses
            if errors is not None:
                return super(UserJSONRenderer, self).render(data)
        
        # Return the data wrapped in the 'user' key for successful responses
        return json.dumps({
            'user': data
        }, ensure_ascii=False).encode(self.charset)
