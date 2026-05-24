from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from apps.users.models import UserProfile
from apps.energy.models import EnergySource, EnergyReading
from datetime import timedelta
import random

class Command(BaseCommand):
    help = 'Seed database with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding database...')

        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser('admin', 'admin@greenai.com', 'admin1234')
            UserProfile.objects.create(user=admin, role='admin', company='GreenAI Corp')
            self.stdout.write(self.style.SUCCESS('  Admin: admin / admin1234'))

        if not User.objects.filter(username='demo').exists():
            demo = User.objects.create_user('demo', 'demo@greenai.com', 'demo1234')
            UserProfile.objects.create(user=demo, role='user', company='Eco Solutions')
            self.stdout.write(self.style.SUCCESS('  Demo:  demo / demo1234'))
        else:
            demo = User.objects.get(username='demo')

        sources_data = [
            {'name': 'Solar Farm Alpha', 'source_type': 'solar', 'capacity_kw': 500.0, 'location': 'Tashkent Region', 'status': 'active', 'installation_date': '2022-03-15'},
            {'name': 'Wind Park Steppe', 'source_type': 'wind', 'capacity_kw': 1200.0, 'location': 'Navoi Region', 'status': 'active', 'installation_date': '2021-07-20'},
            {'name': 'Hydro Station Charvak', 'source_type': 'hydro', 'capacity_kw': 3000.0, 'location': 'Tashkent Oblast', 'status': 'active', 'installation_date': '2019-11-01'},
            {'name': 'Biomass Plant East', 'source_type': 'biomass', 'capacity_kw': 250.0, 'location': 'Fergana Valley', 'status': 'maintenance', 'installation_date': '2023-02-10'},
        ]

        for sdata in sources_data:
            if not EnergySource.objects.filter(name=sdata['name']).exists():
                source = EnergySource.objects.create(owner=demo, **sdata)
                if sdata['status'] == 'active':
                    now = timezone.now()
                    for i in range(20):
                        ts = now - timedelta(hours=i * 6)
                        base = sdata['capacity_kw'] * random.uniform(0.4, 0.9)
                        EnergyReading.objects.create(
                            source=source,
                            timestamp=ts,
                            output_kwh=round(base * random.uniform(0.85, 1.1), 2),
                            efficiency_percent=round(random.uniform(55.0, 92.0), 1),
                            temperature_c=round(random.uniform(15.0, 38.0), 1),
                            wind_speed_ms=round(random.uniform(2.0, 12.0), 1) if sdata['source_type'] == 'wind' else None,
                            recorded_by=demo,
                        )
                self.stdout.write(f'  Created: {sdata["name"]}')

        self.stdout.write(self.style.SUCCESS('\nDone! Visit http://127.0.0.1:8000/'))
