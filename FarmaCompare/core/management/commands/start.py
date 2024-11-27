import os
import importlib
import traceback
from django.core.management.base import BaseCommand

CSV_FOLDER = r'C:\Users\piiet\OneDrive\Documentos\Faculdade\PI\FarmaCompare\FarmaCompare\core\data'
REPORT_FILE = os.path.join(CSV_FOLDER, 'report.log')

def clear_csv_files(folder):
    for file in os.listdir(folder):
        if file.endswith('.csv'):
            file_path = os.path.join(folder, file)
            os.remove(file_path)  
            print(f'Arquivo removido: {file}')

def run_crawlers(folder):
    with open(REPORT_FILE, 'w') as report:
        for file in os.listdir(folder):
            if file.endswith('.py') and not file.startswith('class_'):
                module_name = file[:-3] 
                try:
                    print(f'Iniciando crawler: {module_name}')
                    module = importlib.import_module(f'core.data.{module_name}')
                    
                    class_name = module_name.capitalize() + "Vtex"
                    if hasattr(module, class_name):
                        obj = getattr(module, class_name)()
                        if hasattr(obj, 'get_products'):
                            obj.get_products() 
                            print(f'Crawler {module_name} executado com sucesso.')
                        else:
                            error_message = f'Crawler {module_name} não possui o método "get_products".\n'
                            print(error_message)
                            report.write(error_message)
                    else:
                        error_message = f'Crawler {module_name} não possui a classe esperada "{class_name}".\n'
                        print(error_message)
                        report.write(error_message)
                except Exception as e:
                    error_message = f'Erro no crawler {module_name}: {str(e)}\n'
                    print(error_message)
                    report.write(error_message)
                    report.write(traceback.format_exc() + '\n')
class Command(BaseCommand):
    help = 'Limpa arquivos CSV e inicia todos os crawlers.'

    def handle(self, *args, **kwargs):
        print('Limpando arquivos CSV...')
        clear_csv_files(CSV_FOLDER)
        print('Iniciando crawlers...')
        run_crawlers(CSV_FOLDER)
        print('Processo concluído. Verifique o arquivo report.log para detalhes.')
