# Redis IOC

## Utilização
Modificar a tabela `Redes e Beaglebones.xlsx`, caminho `scripts\spreadsheet`.

Cada linha representa uma nova PV.

Parâmetros obrigatórios:
- Enabled: `True` habilita a PV, `False` desabilita.
- IP: IP do servidor Redis (servidor deve usar a porta 6379). Caso exista interesse em usar redundância de endereços, separe cada endereço com uma vírgula (,)
- Key: Chave Redis
- PV: Nome da PV
- Precision: Casas de precisão (para float)
- Unit: EGU
- Scanrate: Taxa de scan das PVs (para valores < 1, omita o 0. Exemplo: .1, .01, .001)
- Type: Tipo de variável (float, float_put, int, int_put, string, string_put)
    - Variáveis "put" criam duas PVs, uma para setpoint (-SP) e uma para readback (-RB). Para exigir um readback "real", a chave Redis de readback é a chave especificada com o sufixo ":RB"

Parâmetros opcionais: 
- Rack: Não afeta o IOC
- ADDR: Não afeta o IOC (Pode ser usado no futuro)
- Location: Localização, usado como descrição (DESC) da PV.
- HIHI/HIGH/LOW/LOLO: Valores de alarme. Afeta os respectivos campos da PV.

A cada deploy do stack, o container puxa novas versões da spreadsheet desse repositório. Basta forçar um update para atualizar com novas PVs.

## Logs

Localizados em `/opt/redis-ioc/log`

## Performance
Benchmarks disponíveis no repositório [general-benchmarks](https://gitlab.cnpem.br/guilherme.freitas/raw-ethernet-benchmark)