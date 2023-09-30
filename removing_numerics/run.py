import csv

# Nome do arquivo CSV de entrada
input_file = "The Collection Set.csv"

# Nome do arquivo de saída para as instâncias com a tag "numeric"
output_file = "../ignore/numerics.txt"

# Abre o arquivo de saída para escrita
with open(output_file, "w") as output:
    # Cria um objeto leitor de CSV
    with open(input_file, "r") as csv_file:
        reader = csv.reader(csv_file)
        
        # Lê o cabeçalho
        header = next(reader)
        
        # Encontra o índice da coluna "Tags  Tag."
        tag_index = header.index("Tags  Tag.")
        
        # Itera pelas linhas do CSV
        for row in reader:
            # Verifica se a instância tem a tag "numeric"
            if "numeric" in row[tag_index]:
                # Obtém o valor da coluna "Instance  Ins."
                instance_name = row[0]
                
                # Escreve o nome da instância no arquivo de saída
                output.write(instance_name + ".mps.gz\n")

print("Instâncias com a tag 'numeric' foram salvas em", output_file)
