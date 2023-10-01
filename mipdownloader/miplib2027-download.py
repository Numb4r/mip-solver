import json
import csv
import threading
import urllib.request
import os
import os.path
from telegram import Update
from telegram.ext import Application,ApplicationBuilder, CommandHandler, ContextTypes,CallbackContext
    
# Auxiliary function to get a value or its default
def get_value(o, keys, default):
    success = True
    for k in keys:
        if o is not None:
            o = o.get(k, None)
        else:
            success = False
            break
    return o if success else default
    

# Function for filtering instances
def filter(instance):

    forbidden_status = ['open', 'hard']
    if instance['status'] in forbidden_status:
        return False

    if instance['is_infeasible']:
        return False
    
    if instance['is_unbounded']:
        return False
    
    if not instance['is_optimal']:
        return False
    
    n_binaries = instance['size']['binaries']['original']
    n_integers = instance['size']['integers']['original']
        
    if n_binaries + n_integers < 1:
        return False
    
    # tags:
    # 'aggregations', 'benchmark', 'benchmark_suitable', 'binary', 
    # 'binpacking', 'cardinality', 'decomposition', 'equation_knapsack', 
    # 'feasibility', 'general_linear', 'indicator', 'infeasible', 
    # 'integer_knapsack', 'invariant_knapsack', 'knapsack', 'mixed_binary', 
    # 'no_solution', 'numerics', 'precedence', 'set_covering', 'set_packing', 
    # 'set_partitioning', 'variable_bound'
    forbidden_tags = {'decomposition', 'feasibility', 'indicator',
      'infeasible', 'no_solution', 'numerics'}
    
    if instance['tags'] is not None and len(instance['tags']) > 0:
        for tag in instance['tags']:
            if tag in forbidden_tags:
                return False
    
    return True
# miplib2017-selected
def run():
  
    # Load JSON file with MIPLIB 2017 instances' data
    with open('./miplib2017.json') as f:
        instances = json.load(f)

    # Get the list of instances after filtering
    selected_instances = [i for i in instances if filter(i)]

    # Write CSV file with selected instances' attributes
    with open('miplib2017-selected.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['NAME', 'STATUS', 'OBJECTIVE', 'VARIABLES', 'BINARIES', 'INTEGERS', 
                        'CONTINUOUS', 'CONSTRAINTS', 'DENSITY', 'CONSTR.EMPTY', 'CONSTR.FREE', 
                        'CONSTR.SINGLETON', 'CONSTR.AGGREGATION', 'CONSTR.PRECEDENCE', 
                        'CONSTR.VARIABLE.BOUND', 'CONSTR.SET.PARTITIONING', 'CONSTR.SET.PACKING', 
                        'CONSTR.SET.COVERING', 'CONSTR.BINPACKING', 'CONSTR.KNAPSACK', 
                        'CONSTR.INTEGER.KNAPSACK', 'CONSTR.CARDINALITY', 'CONSTR.INVARIANT.KNAPSACK', 
                        'CONSTR.EQUATION.KNAPSACK', 'CONSTR.MIXED.BINARY', 'CONSTR.GENERAL.LINEAR'])
        
        for instance in selected_instances:
            info = [instance['name'],
                instance['status'],
                instance['objective'],
                instance['size']['variables']['original'],
                instance['size']['binaries']['original'],
                instance['size']['integers']['original'],
                instance['size']['continuous']['original'],
                instance['size']['constraints']['original'],
                instance['size']['nonzero_density']['original'],
                get_value(instance, ['constraints', 'empty', 'original'], 0),
                get_value(instance, ['constraints', 'free', 'original'], 0),
                get_value(instance, ['constraints', 'singleton', 'original'], 0),
                get_value(instance, ['constraints', 'aggregations', 'original'], 0),
                get_value(instance, ['constraints', 'precedence', 'original'], 0),
                get_value(instance, ['constraints', 'variable_bound', 'original'], 0),
                get_value(instance, ['constraints', 'set_partitioning', 'original'], 0),
                get_value(instance, ['constraints', 'set_packing', 'original'], 0),
                get_value(instance, ['constraints', 'set_covering', 'original'], 0),
                get_value(instance, ['constraints', 'bin_packing', 'original'], 0),
                get_value(instance, ['constraints', 'knapsack', 'original'], 0),
                get_value(instance, ['constraints', 'integer_knapsack', 'original'], 0),
                get_value(instance, ['constraints', 'cardinality', 'original'], 0),
                get_value(instance, ['constraints', 'invariant_knapsack', 'original'], 0),
                get_value(instance, ['constraints', 'equation_knapsack', 'original'], 0),
                get_value(instance, ['constraints', 'mixed_binary', 'original'], 0),
                get_value(instance, ['constraints', 'general_linear', 'original'], 0)]
            writer.writerow(info)

    # Download MPS.GZ file from each selected instance
    base_output = os.path.join('.', 'miplib2017-selected')
    if not os.path.exists(base_output):
        os.makedirs(base_output, exist_ok=True)
        
    count = 0
    for instance in selected_instances:
        count = count + 1
        print(f'Downloading file {instance["name"]}.mps.gz ({count} of {len(selected_instances)})')
        filename = os.path.join(base_output, f'{instance["name"]}.mps.gz')
        response = urllib.request.urlretrieve(instance['url_download'], filename=filename)


async def ping_server(update: Update, context: CallbackContext):
    await update.message.reply_text(f"Situacao do download {tr.is_alive()}")

async def help(update:Update,context:CallbackContext):
    await update.message.reply_text(f"""
                                    /help - Exibe essa mensagem
                                    /ping - Verifica situacao do donwload
                                    """)
if "__main__" == __name__:
    global end
    end = False 
    bot_token = "6698519042:AAGq-CFtKic24bIiepUd8emCLgbXlAMQ84I"  # Substitua pelo token do seu bot
    app = ApplicationBuilder().token(bot_token).build()
    app.add_handler(CommandHandler("ping", ping_server))
    app.add_handler(CommandHandler(["help","start"],help))
    global tr
    tr = threading.Thread(target=run)
    tr.start()
    
    print("cu")
    

    app.run_polling()
