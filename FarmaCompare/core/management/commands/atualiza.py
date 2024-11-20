
import csv
from decimal import Decimal, InvalidOperation
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand
from core.models import Produto
import os

class Command(BaseCommand):
    help = "Atualiza o banco de dados com os dados dos CSVs"

    def handle(self, *args, **kwargs):
        data_folder = r'C:\Users\piiet\OneDrive\Documentos\GitHub\FATEC_PI_2SEM_2024\FarmaCompare\core\data'
        csv_files = [
            'farma_ultrafarma.csv', 
            'drogariasaopaulo.csv', 
            'paguemenos.csv', 
            'precopopular.csv'
        ]
        for csv_file in csv_files:
            with open(os.path.join(data_folder, csv_file), newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Limpa o valor de 'price' para ser processado corretamente
                    price_raw = row.get('price', '0').replace("R$", "").replace(".", "").replace(",", ".").strip()
                    try:
                        price = Decimal(price_raw)
                    except (ValueError, InvalidOperation):
                        raise ValidationError(f"Preço inválido: {row.get('price')}")

                    # Limpa o valor de 'price_old' se existir
                    price_old_raw = row.get('price_old', '0').replace("R$", "").replace(".", "").replace(",", ".").strip()
                    try:
                        price_old = Decimal(price_old_raw)
                    except (ValueError, InvalidOperation):
                        price_old = None
                    print(row.keys())
                    produto, created = Produto.objects.update_or_create(
                        ean=row['ean'],
                        nome_farmacia=row['nome_farmacia'],
                        defaults={
                            'product_url': row.get('product_url', str()),
                            'sku': row.get('sku', str()),
                            'name': row.get('name', str()),
                            'price': price,
                            'price_old': price_old,
                            'description': row.get('description', str()),
                            'substance': row.get('substance', str()),
                            'brand': row.get('brand', str()),
                            'category': row.get('category', str()),
                            'images': row.get('images', str()),
                        }
                    )
                    if created:
                        self.stdout.write(f'{produto.name} adicionado.')
                    else:
                        self.stdout.write(f'{produto.name} atualizado.')