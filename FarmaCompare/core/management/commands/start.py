import os
import csv
import logging
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Roda os crawlers e atualiza os arquivos CSV semanalmente"

    def handle(self, *args, **kwargs):
        data_folder = 'data'
        crawlers = ['ultrafarma.py', 'drogaria_lecer.py']

        for crawler in crawlers:
            csv_file = os.path.join(data_folder, f'{crawler[:-3]}.csv')
            report_file = os.path.join(data_folder, 'report.csv')

            try:
                open(csv_file, 'w').close()
                os.system(f'python {os.path.join(data_folder, crawler)}')
            except Exception as e:
                logging.error(f"Erro ao rodar {crawler}: {str(e)}")
                with open(report_file, 'a', newline='') as report_csv:
                    writer = csv.writer(report_csv)
                    writer.writerow([crawler, str(e)])
            
            self.stdout.write(f"{crawler} executado com sucesso.")
