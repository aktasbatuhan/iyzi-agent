import json
import json
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from openai import OpenAI
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

serper_api_key = os.getenv('SERPER_API_KEY')

search_query = "apple inc"
search_location = "Turkey"
search_gl = "tr"
search_hl = "tr"


merchant_list = """
www.nike.com/tr/,www.guess.eu/tr-tr/home,www.decathlon.com.tr,www.neobebek.com,www.modamizbir.com,www.krc.com.tr,www.esteelauder.com.tr,tr.puma.com,tr.dior.com,www.atasay.com,www.camper.com/tr_TR,lesbenjamins.com,www.calzedonia.com/tr,www.bkmkitap.com,www.milagron.com,www.maccosmetics.com.tr,www.yvesrocher.com.tr,www.bsl.com.tr,www.atasay.com,tr.dior.com,www.flavus.com,www.gaming.gen.tr,www.samsung.com/tr/,www.journey.com.tr,www.keyifbebesi.com.tr,www.kraftbaby.com,www.makyajtrendi.com,www.operaistanbul.com,www.pckolik.com,www.petzzshop.com,shopigo.com,www.sportive.com.tr,www.slazenger.com.tr,www.sportime.com.tr,www.suwen.com.tr,sutore.com,toucheprive.com,www.barcin.com,www.havos.com.tr,www.korendy.com.tr,joinus.com.tr,www.hazelanna.com,www.modacelikler.com/,www.yargici.com,www.petburada.com,www.tamertanca.com.tr,www.viadellerose.com,www.eperde.com,www.blackspade.com.tr/,hsagaza.com/tr/,www.pelinsenoglu.com/,www.enplus.com.tr/,www.normod.com/,www.ebrulibutikmoda.com/,www.cafemarkt.com/,www.otello.com.tr/,www.adoremobilya.com/,cilek.com/,shop.goldenrose.com.tr/,www.silkandcashmere.com,https://cyrene.com.tr/,naosstars.com,kozmetik.avon.com.tr,www.maccosmetics.com.tr,www.yvesrocher.com.tr,tr.dior.com,www.clinique.com.tr,www.bobbibrown.com.tr,www.origins.com.tr,www.aveda.com.tr,www.makyajtrendi.com,www.justinbeauty.net,www.korendy.com.tr,www.flavus.com,www.uraw.com.tr,shreddedbrothers.com,www.karcikozmetik.com,shop.goldenrose.com.tr/,badecanlar.com,https://cyrene.com.tr/,elsesilver.com,farmareyon.com,limonian.com,miseca.com,naosstars.com,narecza.com,ozonlabs.com,sevil.com.tr,soflycosmetics.com,www.guess.eu/tr-tr/home,www.intimissimi.com/tr,www.suwen.com.tr,www.modamizbir.com,suudcollection.com,lesbenjamins.com,www.calzedonia.com/tr,www.yargici.com,www.lidyana.com,shop.sarar.com,www.eceninbutigi.com,toucheprive.com,shopigo.com,www.havos.com.tr,joinus.com.tr,www.bybasicman.com,www.hazelanna.com,www.raffaello-network.com/turkce,www.tudors.com,milagron.com,www.viadellerose.com,www.terziademaltun.com,exxeselection.com,www.kayra.com,www.bsl.com.tr,www.roman.com.tr,www.terzidukkani.com,e-tesettur.com.tr,markastok.com,www.gulsahintakitezgahi.com.tr,www.yamunakorse.com,www.sentetiksezar.com,www.askinisantasi.com,www.modasena.com,www.journey.com.tr,mervellion.com,www.efbutik.com,badebutik.com,www.modacelikler.com/,www.blackspade.com.tr/,sagaza.com/tr/,www.pelinsenoglu.com/,www.ebrulibutikmoda.com/,silkandcashmere.com,beyyoglu.com,bircancil.com,happytowear.co,hollylolly.net,iamnotbasic.com,^jeanslab.com^,katiaandbony.com,kiyafetsepeti.com.tr,libas.com.tr,love-onfriday.com,loya.com.tr,meliketatar.com,mooibutik.com,mybestfriends.com.tr,no11butik.com,ontrailstore.com,ozgeozgenc.com,rodijeans.com.tr,scsarvin.com.tr,www.camper.com/tr_TR,www.tamertanca.com.tr,www.deriden.com.tr,www.bver.store,www.tildamugs.com,sutore.com,www.markapark.com,www.saillakers.com.tr,www.atasay.com,www.burcuokut.com,www.barcin.com,getchostore.com,happy-nes.com,jump.com.tr,lastikpabuc.com,mers.com.tr,muya.com,www.neslihancanpolat.com,prev.shop,reiskuyumculuk.com,salomon.com.tr,samuraysport.com,SneaksUp.com,swarovski.com.tr,vicco.com.tr,vitruta.com,deichmann.com,northwild.com.tr,limoya.com,bilgekarga.com.tr,pumpsup.com,shulebags.com,www.nike.com/tr/,www.columbia.com.tr,www.decathlon.com.tr,www.sporjinal.com.,www.slazenger.com.tr,www.ecgspor.com,www.sportive.com.tr,tr.puma.com,www.newbalance.com.tr,www.lescon.com.tr,www.sportime.com.tr,www.naveksport.com.tr,www.anafarta.com.tr,fenerium.com,kutupayisi.com,www.gaming.gen.tr,www.pckolik.com,www.samsung.com/tr/,www.qp.com.tr,www.laptop.com.tr,www.krc.com.tr,www.chakra.com.tr/,www.tefal.com.tr,rowenta.com.tr,wmf.com.tr,www.dogtas.com,www.jumbo.com.tr,www.zwilling.com,www.yurudesign.com.tr/,www.cookplus.com.tr,www.lavashops.com,shop.nurus.com,hecha.com.tr,www.mutlubiev.com,www.eperde.com,www.muyusleep.com,www.hivdakarakoc.com,www.sezerlerperde.com,www.nalburcuk.com,www.juahome.com,gurmechef.com,www.chefandco.com,www.enplus.com.tr/,www.normod.com/,www.cafemarkt.com/,www.otello.com.tr/,www.adoremobilya.com/,cilek.com/,toprakvesu.com,ruumstore.com,perde.com,gallerycrystal.com.tr,ecocotton.com.tr,shop.finish.com.tr,illy.barista.com.tr,www.kahhve.com,www.fitchef.com.tr,www.taftcoffee.com,www.namligurmeonline.com,www.livashop.com,dukkan.dilarakocak.com.tr,www.ulysseszeytinyagi.com.tr/,www.kahve.com,boxxcoffee.com,etineniyisi.com,coffeedepartment.co,www.neobebek.com,www.kraftbaby.com,www.operaistanbul.com,www.isabelabbey.com.tr,www.keyifbebesi.com.tr,ilkadimlarim.com,shop.nuk.com.tr,bebekekspres.com,tirtilkids.com,www.bkmkitap.com,www.dopinghafiza.com,www.ilkuzem.com,www.trtmarket.net,www.benimhocam.com,www.mindset.com.tr,www.tasarionlinegitim.com,www.hukukmarket.com,inkas.com.tr,trengeducation.com,www.mektepyayinlari.com.tr,www.kitantik.com,kitapsepeti.com,nesinyayinevi.com,kitap.solaunitas.com,unicourse.co,betastore.com.tr,www.grupanya.com,www.kolaymama.com,www.petburada.com,daraaksesuar.com,www.acev.org/destek-ol/alisveris-yap,www.deercase.com,www.petzzshop.com,www.hizlimama.com,vespastoreturkey.com,www.shellypopart.com,kolayoto.com,woohoobox.com,www.unipak.com.tr,miamano.com,bizevdeyokuz.store,doggoapp.com,www.eofis.com.tr,hediyesepeti.com,heryerbitki.com,istanbulcicekleri.com,leaffloweristanbul.com,momeprint.com,muzikaletleri.com.tr,rosanigrum.com,yapaycicekdeposu.com,zoo.com.tr,galenleather.com,phaksesuar.com,osevio.com,bodo.com"""

system_prompt_agent = """You are a helpful e-commerce assistant for iyzico users. Your task is to generate concise answers for product discovery queries for them to find best fit products across all iyzico merchants. 
Each time you will get a search query of user and search results. Try to adopt your summary regarding users' query for product discovery. 
Ensure that you give references to the relevant URLs in your answers after your statements are influenced by any of the resources.
You should provide an overall answer to user queries, remember users are seeking products, 
and they need to understand their features, prices and various information about them to decide whether to buy or not. 
Therefore, first, start with an overall answer for the query by using information from all sources, 
then pick only the best-fit products for the query and break your answer down into sections 
where you highlight the most relevant parts from each source. Remember you are working for iyzico, try to motivate users for shopping without misleading them.
Your responses will be directly shown to the users. You must return your answers in Turkish."""

system_prompt_checker = """You are a helpful assistant for iyzico agentic workflows.
Your task is to check whether the urls you receive are belong to any iyzico merchants or not by comparing the url domain with the merchant list.
First read the urls you receive.
Then compare their domain names with the merchant list you receive. 
If the domain name of a url matches with the merchant list you receive, then put that url into a list.
You must only compare the domain names but not the path while filtering the merchant urls.
Domain name is the text between "https://" and the first / sign in a url.
For example, for below url "ucuzbudur" is the domain name, "karaca-air-pro-cook-koz-xl-airfryer-space-gray-black" is the path. Therefore, this url is not an iyzico merchant url.
"https://www.ucuzbudur.com/karaca-air-pro-cook-koz-xl-airfryer-space-gray-black" 
Do not ever include urls that belongs to n11.com, hepsiburada.com, trendyol.com, boyner.com, and pazarama.com.
Once you detected the iyzico merchant urls, then pick the top 5 of them by using only position,rating and price values. If there are less than 3 iyzico merchant urls then just return them but do not try to add up until you reach 5.
Finally return the top 5 urls in a json object as in the below format:
{
"urls": [
"[url1]",
"[url2]",
"[url3]",
"[url4]",
"[url5]"
]
}
Remember you should return urls that are existing in the initial list by filtering the ones who does not belong to any merchant. 
Your response will be used as an input for another agent therefore only return the json but not any other text.
"""


system_prompt_final_answer = """
You are a helpful e-commerce assistant for iyzico users.  iyzico is a Turkish fintech company.
Your task is to generate concise answers for their product discovery queries. 
Each time you will get a search query of user and search results. Do not ever include urls that belongs to n11.com, hepsiburada.com, trendyol.com, boyner.com, and pazarama.com.
Try to adopt your answers regarding users' query for product discovery. 
Ensure that you give references to the relevant URLs in your answers after your statements are influenced by any of the resources.
You should provide an overall answer to user queries, remember users are seeking products, and they need to understand their features, prices and various information about them to decide whether to buy or not. Therefore, break your answer down into sections where you highlight the most relevant parts from each source. After each product give a reference for the product with "Ürüne Git" text with the actual product hyperlink.
Make your responses concise but comprehensive. Do not try to make your answers conversational and engaging. There won't be any conversation, your answers are the final response to user query.
If you receive any information about any campaign, state them separately for more clear understanding. Your responses will be directly shown to the users. Only use the information you receive but do not ever make up anything on your own.
Remember you are serving to iyzico users, so ensure that your answers are in Turkish and motivating users to complete shopping without misleading them.
Use only the data you receive.
"""

def get_search_results(initial_query, search_location, search_gl, search_hl, serper_api_key):
    url = "https://google.serper.dev/shopping"

    payload = json.dumps({
        "q": initial_query,
        "location": search_location,
        "gl": search_gl,
        "hl": search_hl,
        "num": 20
    })
    headers = {
        'X-API-KEY': serper_api_key,
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, data=payload)
    if response.status_code == 200:
        data = response.json()
        results = {}
        for item in data.get('shopping', []):
            results[item['link']] = {
                'price': item.get('price'),
                'rating': item.get('rating'),
                'position': item.get('position')
            }
        return data, results 
    else:
        print(f"Request failed with status code {response.status_code}")
        return {}
    

def iyzi_check(system_prompt_checker, merchant_list, results):
    # Initialize the OpenAI client
    # Call the OpenAI API to get the completion
    completion = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": system_prompt_checker },
            {"role": "user", "content": f"""Merchant list: {merchant_list}. /n/n
                                            Web Search Results:  {results}"""}
        ]
    )

    # Get the workflow from the response
    #print(completion)
    response = completion.choices[0].message.content
    print( f"""Initial list of urls": {results}, "Filtered url list": {response}""")
    return response


def get_url_data(url: str) -> dict:
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {os.getenv('JINA_BEARER_TOKEN')}" 
    }

    # Log the URL to be requested
    response = requests.get(f"https://r.jina.ai/{url}", headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()


def merge_data(search_data, url_data):
    for item in search_data.get('shopping', []):
        if item['link'] in url_data:
            item.update(url_data[item['link']])
    return search_data


def shopping_assistant(system_prompt_final_answer, initial_query, search_results):
    response = ""
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt_final_answer},
            {"role": "user", "content": f"User query: {initial_query}.\n\nWeb Search Results: {search_results}"}
        ],
        stream=True
    )

    for chunk in completion:
        if chunk.choices[0].delta.content is not None:
            response += chunk.choices[0].delta.content

    return response


# Streamlit app
def main():
    st.title("iyzico Alışveriş Asistanı")

    # User input
    initial_query = st.text_input("iyzico Geçerli Mağazalarda Ürün Arayın:")

    if st.button("Ara"):
        with st.spinner("Ürünler bulunuyor..."):
            search_data, results = get_search_results(initial_query, search_location, search_gl, search_hl, serper_api_key)
            
            json_response = iyzi_check(system_prompt_checker, merchant_list, results)
            try:
                filtered_urls = json.loads(json_response)['urls']
                st.write(f"Ürün linkleri bulundu, cevap hazırlanıyor...")
            except (json.JSONDecodeError, KeyError) as e:
                st.error(f"JSON işleme hatası veya 'urls' anahtarı eksik: {e}")
                return

            url_data = {}
            with ThreadPoolExecutor() as executor:
                future_to_url = {executor.submit(get_url_data, url): url for url in filtered_urls}
                for future in as_completed(future_to_url):
                    url = future_to_url[future]
                    try:
                        data = future.result()
                        if data:
                            url_data[url] = data
                    except Exception as exc:
                        st.error(f"{url} için bir hata oluştu: {exc}")

            merged_data = {url: url_data.get(url, {}) for url in filtered_urls}
            
            # Get the assistant's response
            response = shopping_assistant(system_prompt_final_answer, initial_query, merged_data)
            
            # Display the response
            st.subheader("Sonuçlar:")
            st.write(response)

if __name__ == "__main__":
    main()