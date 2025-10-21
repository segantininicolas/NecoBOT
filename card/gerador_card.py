import json
import requests
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
import io

caminhoAtual = os.path.dirname(__file__)
caminhoTemplate = os.path.join(caminhoAtual, 'template.json')
caminhoFonte = os.path.join(caminhoAtual, 'fonts')
caminhoData = os.path.join(caminhoAtual, "data.json")
caminhoAssets = os.path.join(caminhoAtual, "assets")

def criar_imagem_base():

    try:
        with open(caminhoTemplate, 'r', encoding='utf-8') as f:
            configImagem = json.load(f)
        with open(caminhoData, 'r', encoding='utf-8') as f:
            configUsuario = json.load(f)    

        configBase = configImagem['baseImagem']
        imagem = Image.new('RGBA', tuple(configBase['tamanhoImagem']), configBase['corImagem'])
        draw = ImageDraw.Draw(imagem)
        elementoDimensao = {}

        for elementoNome, config in configImagem['elementos'].items():
           # print(f"verificando o elemento: '{elementoNome}' tipo: '{config.get('tipo')}'")
            elementoTipo = config.get("tipo", "texto")

            if elementoTipo == "imagem_url":
                chaveURL = config['dado']
                imagemURL = configUsuario.get(chaveURL)

                if imagemURL:
                    try:
                        baixarImagem = requests.get(imagemURL)
                        baixarImagem.raise_for_status()
                        imagemBytes = io.BytesIO(baixarImagem.content)
                        imagemColar = Image.open(imagemBytes)

                        nivelDesfoque = config.get("desfoque")
                        if nivelDesfoque is not None and isinstance(nivelDesfoque, (int, float)):
                            imagemColar = imagemColar.filter(ImageFilter.GaussianBlur(nivelDesfoque))

                        nivelEscurecer = config.get("escurecer")
                        if nivelEscurecer is not None and isinstance(nivelEscurecer, (int,float)):
                            imagemColar = imagemColar.convert('RGBA')

                            alpha = int(255 * nivelEscurecer)
                            overlay = Image.new('RGBA', imagemColar.size, (0, 0, 0, alpha))
                            
                            imagemColar = Image.alpha_composite(imagemColar, overlay)

                        imagemColar = imagemColar.resize(tuple(config['tamanho']))
                        imagem.paste(imagemColar, tuple(config['posicao']), imagemColar.convert('RGBA'))

                        posicaoFinal = tuple(config['posicao'])
                        tamanhoFinal = imagemColar.size
                        elementoDimensao[elementoNome] = {
                        'x': posicaoFinal[0],
                        'y': posicaoFinal[1],
                        'largura': tamanhoFinal[0],
                        'altura': tamanhoFinal[1]
                    }
                   
                    except Exception as erro:
                        print(f"Erro ao processar a imagem '{elementoNome}': {erro}")

            elif elementoTipo == "imagem_local":
                try:
                    caminhoImagemLocal = os.path.join(caminhoAssets, config['caminho'])

                    imagemColar = Image.open(caminhoImagemLocal)
                    imagemColar = imagemColar.resize(tuple(config['tamanho']))
                    imagem.paste(imagemColar, tuple(config['posicao']), imagemColar.convert('RGBA'))

                    posicaoFinal = tuple(config['posicao'])
                    tamanhoFinal = imagemColar.size
                    elementoDimensao[elementoNome] = {
                        'x': posicaoFinal[0],
                        'y': posicaoFinal[1],
                        'largura': tamanhoFinal[0],
                        'altura': tamanhoFinal[1]
                    }

                except Exception as erro:
                    print("erro na imagem de rank")

            elif elementoTipo == "imagem_local_dinamica":
                try:
                    chaveDado = config['dado']
                    arquivoSufixo = config.get('sufixo', '.png')
                    subpasta = config.get('subpasta')

                    valorDado = configUsuario.get(chaveDado)

                    if valorDado:

                        arquivoNome = str(valorDado) + arquivoSufixo

                        caminhoBandeira = os.path.join(caminhoAssets, subpasta, arquivoNome)

                        imagemColar = Image.open(caminhoBandeira)
                        imagemColar = imagemColar.resize(tuple(config['tamanho']))
                        imagem.paste(imagemColar, tuple(config['posicao']), imagemColar.convert('RGBA'))

                        posicaoFinal = tuple(config['posicao'])
                        tamanhoFinal = imagemColar.size
                        elementoDimensao[elementoNome] = {
                        'x': posicaoFinal[0],
                        'y': posicaoFinal[1],
                        'largura': tamanhoFinal[0],
                        'altura': tamanhoFinal[1]
                    }
                except Exception as erro:
                    print("Erro na bandeira")
                
            elif elementoTipo == "texto":

                configTexto = os.path.join(caminhoFonte, config['fonte'])
                fonte = ImageFont.truetype(configTexto, config['tamanho_fonte'])
                cor = config['cor']

                inserirTexto = str(configUsuario.get(config.get('dado', '')) or config.get('texto_fixo', ''))

                prefixo = config.get("prefixo", "")
                sufixo = config.get("sufixo", "")
                textoFinal = f"{prefixo}{inserirTexto}{sufixo}" if inserirTexto else ""

                posicaoTexto = [0, 0]
                alinhamentoRef = config.get("alinhamento")
                alinhamentoDireitaRef = config.get("alinharDireita")

                if alinhamentoRef and alinhamentoRef in elementoDimensao:

                    refBbox = elementoDimensao[alinhamentoRef]
                    refX, refY, refLar, refAlt = refBbox['x'], refBbox['y'], refBbox['largura'], refBbox['altura']

                    caixaTexto = draw.textbbox((0,0), textoFinal, font=fonte)
                    larguraTexto = caixaTexto[2] - caixaTexto[0]

                    posX = (refX + refLar // 2) - (larguraTexto // 2)

                    deslocamentoY = config.get("deslocamentoY", 5)
                    posY = refY + refAlt + deslocamentoY

                    posicaoTexto = (posX, posY)

                elif alinhamentoDireitaRef and alinhamentoDireitaRef in elementoDimensao:

                    refBbox = elementoDimensao[alinhamentoDireitaRef]
                    refX, refY, refLar, refAlt = refBbox['x'], refBbox['y'], refBbox['largura'], refBbox['altura']

                    caixaTexto = draw.textbbox((0,0), textoFinal, font=fonte)
                    larguraTexto = caixaTexto[2] - caixaTexto[0]

                    deslocamentoX = config.get("deslocamentoX", 5)
                    posX = (refX + refLar) - larguraTexto - deslocamentoX

                    alturaTexto = caixaTexto[3] - caixaTexto[1]
                    deslocamentoYacima = config.get("deslocamentoYacima", 5)
                    posY = refY - alturaTexto - deslocamentoYacima

                    posicaoTexto = (posX, posY)

                else:
                    posicaoTexto = tuple(config.get('posicao', (0, 0)))

                draw.text(posicaoTexto, textoFinal, font=fonte, fill=cor)
        

        arredondarImagemRaio = configBase.get("cantoArredondado", 0)

        if arredondarImagemRaio > 0:

            circulo = Image.new('L', (arredondarImagemRaio * 2, arredondarImagemRaio * 2), 0)
            mascara = ImageDraw.Draw(circulo)
            mascara.ellipse((0, 0, arredondarImagemRaio * 2, arredondarImagemRaio * 2), fill=255)

            mascara = Image.new('L', imagem.size, 255)
            largura, altura = imagem.size

            mascara.paste(circulo.crop((0, 0, arredondarImagemRaio, arredondarImagemRaio)), (0, 0))
            mascara.paste(circulo.crop((arredondarImagemRaio, 0, arredondarImagemRaio * 2, arredondarImagemRaio)), (largura - arredondarImagemRaio, 0))
            mascara.paste(circulo.crop((arredondarImagemRaio, arredondarImagemRaio, arredondarImagemRaio * 2, arredondarImagemRaio * 2)), (largura - arredondarImagemRaio, altura - arredondarImagemRaio))
            mascara.paste(circulo.crop((0, arredondarImagemRaio, arredondarImagemRaio, arredondarImagemRaio * 2)), (0, altura - arredondarImagemRaio))

            imagem.putalpha(mascara)

        return imagem
    
    except Exception as erro:
        print(f"Ocorreu um erro geral a criar a imagem: {erro}")
        return None