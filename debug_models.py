import inspect
import os

try:
    # Get all models in registry
    all_models = list(env.registry.keys())
    print(f"TOTAL_MODELS: {len(all_models)}")
    
    if 'crm.lead' in env:
        model = env['crm.lead']
        try:
            file_path = inspect.getfile(model.__class__)
            print(f"CRM_LEAD_FILE: {file_path}")
        except Exception as e:
            print(f"COULD_NOT_GET_FILE: {e}")
            
        # Try to find the module name
        module_name = model._module
        print(f"CRM_LEAD_MODULE: {module_name}")
    else:
        print("CRM_LEAD_NOT_IN_ENV")
        # List first 10 models for context
        print(f"FIRST_10_MODELS: {all_models[:10]}")

except Exception as e:
    print(f"ERROR: {e}")
