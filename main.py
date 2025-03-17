from resources.Downloads import Downloads

if __name__ == '__main__':
    downloads = Downloads()
    
    downloads.iniciar_processo(lambda: downloads.download_notas(municipio='PORTO ALEGRE'))
    downloads.iniciar_processo(lambda: downloads.download_notas(municipio='CACHOEIRINHA'))
    downloads.iniciar_processo(lambda: downloads.download_notas(municipio='NACIONAL'))
