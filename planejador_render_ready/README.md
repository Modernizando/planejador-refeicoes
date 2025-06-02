# Planejador de Refeições Semanais

Este é um site gerador de cardápios saudáveis e balanceados para uma semana inteira. O usuário seleciona tipo de dieta, número de pessoas e refeições desejadas. O site gera receitas com modo de preparo, calorias e lista de compras automática.

## Funcionalidades

- Geração de cardápio semanal com base em preferências
- Receitas com ingredientes, preparo, calorias e medidas por pessoa
- Botão para baixar lista de compras
- Interface responsiva (funciona bem no celular)
- Pronto para deploy no Render

## Como rodar localmente

```bash
pip install -r requirements.txt
python main.py
```

## Deploy no Render

- Configure como Web Service
- Build command: `pip install -r requirements.txt`
- Start command: `python main.py`
- Porta: `5001`