import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from api.models import LoanApplication

try:
    loan = LoanApplication.objects.get(id=4)
    print(json.dumps(loan.data, indent=2, ensure_ascii=False))
except Exception as e:
    print(f"Error: {e}")
