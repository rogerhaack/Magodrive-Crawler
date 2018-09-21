from bs4 import BeautifulSoup
import requests
import csv

csv_out = open('output.csv', 'w',newline='',encoding = "utf8")
mywriter = csv.writer(csv_out)

for i in range(29,42):
    url = "https://www.magodrive.com.br/sitemap/products/"+str(i)
    xml = requests.get(url)

    print(url)

    if(xml.status_code == 200): 
        xmlBeauti = BeautifulSoup(xml.content,"xml")
        urls = xmlBeauti.find_all('url')

        for i in range(0, len(urls)):  
            urlImage = None
            title = None
            descricao = None
            marca = None
            preco = None

            urlProduto = urls[i].find("loc")   
            urlImage = urls[i].find("image:loc")    
            retornourl = requests.get(urlProduto.get_text())

            if(retornourl.status_code == 200):
                produto = BeautifulSoup(retornourl.content,"lxml")               

                data = []

                #Nome Produto
                try:
                    title = produto.find("meta",{"property":"og:title"})['content']
                except:
                    pass
                #Marca Produto
                try:
                    marcadiv = produto.find("div",{"class":"information"})
                    marcasmall = marcadiv.find("small")
                    marca = marcasmall.get_text()   
                except:
                    pass           
                #Preço Produto
                try:
                    precostrong = produto.find("strong",{"class":"sale-price"})            
                    precospan = precostrong.find("span")
                    preco = precospan.get_text()
                    preco = preco.replace("R$ ","")
                except:
                    pass
                #Descrição Produto
                try:
                    descricaodiv = produto.find("div",{"class":"wd-descriptions-text"})
                    descricaospan = descricaodiv.find("span")
                    descricao = descricaospan.get_text()
                except:
                    pass

                data.append(title)
                data.append(marca) 
                data.append(preco) 
                data.append(descricao)              
                if urlImage != None:                        
                    data.append(urlImage.get_text())
                else:
                    data.append(urlImage)
                data.append(urlProduto.get_text())     
            
                mywriter.writerow(data)
            
                #print("Nome: "+title)
                #print("Marca: "+marca)
                #print("Preço: "+preco)
                #print("Descrição: "+descricao)

csv_out.close()