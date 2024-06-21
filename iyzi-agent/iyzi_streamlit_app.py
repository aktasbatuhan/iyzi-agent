import json
import json
import requests
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from openai import OpenAI
import streamlit as st
import os
import time
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

serper_api_key = os.getenv('SERPER_API_KEY')

search_query = "apple inc"
search_location = "Turkey"
search_gl = "tr"
search_hl = "tr"


merchant_list = """
karaca.com,
nike.com,
guess.eu,
decathlon.com.tr,
neobebek.com,
modamizbir.com,
krc.com.tr,
esteelauder.com.tr,
puma.com,
dior.com,
atasay.com,
camper.com,
lesbenjamins.com,
calzedonia.com,
bkmkitap.com,
milagron.com,
maccosmetics.com.tr,
yvesrocher.com.tr,
bsl.com.tr,
flavus.com,
gaming.gen.tr,
samsung.com,
journey.com.tr,
keyifbebesi.com.tr,
kraftbaby.com,
makyajtrendi.com,
operaistanbul.com,
pckolik.com,
petzzshop.com,
shopigo.com,
sportive.com.tr,
slazenger.com.tr,
sportime.com.tr,
suwen.com.tr,
sutore.com,
toucheprive.com,
barcin.com,
havos.com.tr,
korendy.com.tr,
joinus.com.tr,
hazelanna.com,
modacelikler.com,
yargici.com,
petburada.com,
tamertanca.com.tr,
viadellerose.com,
eperde.com,
blackspade.com.tr,
hsagaza.com,
pelinsenoglu.com,
enplus.com.tr,
normod.com,
ebrulibutikmoda.com,
cafemarkt.com,
otello.com.tr,
adoremobilya.com,
cilek.com,
goldenrose.com.tr,
silkandcashmere.com,
cyrene.com.tr,
naosstars.com,
avon.com.tr,
clinique.com.tr,
bobbibrown.com.tr,
origins.com.tr,
aveda.com.tr,
justinbeauty.net,
uraw.com.tr,
shreddedbrothers.com,
karcikozmetik.com,
badecanlar.com,
elsesilver.com,
farmareyon.com,
limonian.com,
miseca.com,
ozonlabs.com,
sevil.com.tr,
soflycosmetics.com,
intimissimi.com,
suudcollection.com,
lidyana.com,
sarar.com,
eceninbutigi.com,
bybasicman.com,
raffaello-network.com,
tudors.com,
terziademaltun.com,
exxeselection.com,
kayra.com,
roman.com.tr,
terzidukkani.com,
e-tesettur.com.tr,
markastok.com,
gulsahintakitezgahi.com.tr,
yamunakorse.com,
sentetiksezar.com,
askinisantasi.com,
modasena.com,
mervellion.com,
efbutik.com,
badebutik.com,
beyyoglu.com,
bircancil.com,
happytowear.co,
hollylolly.net,
iamnotbasic.com,
jeanslab.com,
katiaandbony.com,
kiyafetsepeti.com.tr,
libas.com.tr,
love-onfriday.com,
loya.com.tr,
meliketatar.com,
mooibutik.com,
mybestfriends.com.tr,
no11butik.com,
ontrailstore.com,
ozgeozgenc.com,
rodijeans.com.tr,
scsarvin.com.tr,
deriden.com.tr,
bver.store,
tildamugs.com,
markapark.com,
saillakers.com.tr,
burcuokut.com,
getchostore.com,
happy-nes.com,
jump.com.tr,
lastikpabuc.com,
mers.com.tr,
neslihancanpolat.com,
prev.shop,
reiskuyumculuk.com,
samuraysport.com,
SneaksUp.com,
swarovski.com.tr,
vicco.com.tr,
vitruta.com,
deichmann.com,
northwild.com.tr,
limoya.com,
bilgekarga.com.tr,
pumpsup.com,
shulebags.com,
columbia.com.tr,
sporjinal.com,
ecgspor.com,
newbalance.com.tr,
lescon.com.tr,
naveksport.com.tr,
anafarta.com.tr,
fenerium.com,
kutupayisi.com,
qp.com.tr,
laptop.com.tr,
chakra.com.tr,
tefal.com.tr,
rowenta.com.tr,
wmf.com.tr,
dogtas.com,
jumbo.com.tr,
zwilling.com,
yurudesign.com.tr,
cookplus.com.tr,
lavashops.com,
shop.nurus.com,
hecha.com.tr,
mutlubiev.com,
muyusleep.com,
hivdakarakoc.com,
sezerlerperde.com,
nalburcuk.com,
juahome.com,
gurmechef.com,
chefandco.com,
toprakvesu.com,
ruumstore.com,
perde.com,
gallerycrystal.com.tr,
ecocotton.com.tr,
finish.com.tr,
illy.barista.com.tr,
kahhve.com,
fitchef.com.tr,
taftcoffee.com,
namligurmeonline.com,
livashop.com,
dukkan.dilarakocak.com.tr,
ulysseszeytinyagi.com.tr,
kahve.com,
boxxcoffee.com,
etineniyisi.com,
coffeedepartment.co,
isabelabbey.com.tr,
ilkadimlarim.com,
shop.nuk.com.tr,
bebekekspres.com,
tirtilkids.com,
dopinghafiza.com,
ilkuzem.com,
trtmarket.net,
benimhocam.com,
mindset.com.tr,
tasarionlinegitim.com,
hukukmarket.com,
inkas.com.tr,
trengeducation.com,
mektepyayinlari.com.tr,
kitantik.com,
kitapsepeti.com,
nesinyayinevi.com,
kitap.solaunitas.com,
unicourse.co,
betastore.com.tr,
grupanya.com,
kolaymama.com,
daraaksesuar.com,
acev.org,
deercase.com,
hizlimama.com,
vespastoreturkey.com,
shellypopart.com,
kolayoto.com,
woohoobox.com,
unipak.com.tr,
miamano.com,
bizevdeyokuz.store,
doggoapp.com,
eofis.com.tr,
hediyesepeti.com,
heryerbitki.com,
istanbulcicekleri.com,
leaffloweristanbul.com,
momeprint.com,
muzikaletleri.com.tr,
rosanigrum.com,
yapaycicekdeposu.com,
zoo.com.tr,
galenleather.com,
phaksesuar.com,
osevio.com,
bodo.com"""

system_prompt_final_answer = """
YYou are a helpful e-commerce assistant for iyzico users.  iyzico is a Turkish fintech company.
Your task is to generate concise answers for their product discovery queries. 
Each time you will get a search query of user and search results. Do not ever include urls that belongs to n11.com, hepsiburada.com, trendyol.com, boyner.com, and pazarama.com.
Try to adopt your answers regarding users' query for product discovery. 
Ensure that you give references to the relevant URLs in your answers after your statements are influenced by any of the resources.
You should provide an overall answer to user queries, remember users are seeking products, and they need to understand their features, prices and various information about them to decide whether to buy or not. Therefore, break your answer down into sections where you highlight the most relevant parts from each source. After each product give a reference for the product with "Ürüne Git:" text with the actual product hyperlink.
Make your responses concise but comprehensive. Do not try to make your answers conversational and engaging. There won't be any conversation, your answers are the final response to user query.
If you receive any information about any campaign, state them too for the relevant product. Your responses will be directly shown to the users. Only use the information you receive but do not ever make up anything on your own.
Remember you are serving to iyzico users, so ensure that your answers are in Turkish and motivating users to complete shopping without misleading them.
Use only the data you receive.
If you don't receive any data please kindly ask for user to try searching for another product.
"""

def get_search_results(initial_query, search_location, search_gl, search_hl, serper_api_key):
    url = "https://google.serper.dev/shopping"

    payload = json.dumps({
        "q": initial_query,
        "location": search_location,
        "gl": search_gl,
        "hl": search_hl,
        "num": 50
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
            url = item['link']
            domain = extract_domain(url)
            results[domain] = {
                'url': url,
                'price': item.get('price'),
                'rating': item.get('rating'),
                'position': item.get('position')
            }
        print("#########")
        print(results)
        return results
    else:
        print(f"Request failed with status code {response.status_code}")
        return {}

def extract_domain(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    
    if domain.startswith('www.'):
        domain = domain[4:]
    
    domain = domain.split('/')[0]
    print("#########")
    print(domain)
    return domain

def compare_domains(extracted_domains, merchant_list):
    print("Extracted domains:", extracted_domains)
    print("Merchant list:", merchant_list)
    
    # Clean and normalize the merchant list
    cleaned_merchant_list = [domain.strip().lower() for domain in merchant_list if domain.strip()]
    
    # Convert both lists to sets of lowercase domains for case-insensitive comparison
    extracted_set = set(domain.lower() for domain in extracted_domains)
    merchant_set = set(cleaned_merchant_list)
    
    final_url_list = extracted_set.intersection(merchant_set)
    
    print("Matching domains:", final_url_list)
    
    return list(final_url_list)

def sort_and_limit_urls(merged_data, limit=5):
    # Sort the items based on position (assuming lower position is better)
    sorted_items = sorted(merged_data.items(), key=lambda x: x[1].get('position', float('inf')))
    
    # Take the top 'limit' items
    limited_items = sorted_items[:limit]
    
    # Convert back to dictionary
    return dict(limited_items)

def get_url_data(url: str) -> dict:
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {os.getenv('JINA_BEARER_TOKEN')}" 
    }
    response = requests.get(f"https://r.jina.ai/{url}", headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()

def merge_data(search_data, url_data):
    for domain, item in search_data.items():
        if domain in url_data:
            item.update(url_data[domain])
    return search_data

def shopping_assistant(system_prompt_final_answer, initial_query, search_results):
    stream = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt_final_answer},
            {"role": "user", "content": f"User query: {initial_query}.\n\nWeb Search Results: {search_results}"}
        ],
        stream=True
    )
    
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            yield chunk.choices[0].delta.content



# Streamlit app
def main():
    st.title("iyzico Alışveriş Asistanı")

    initial_query = st.text_input("iyzico Geçerli Mağazalarda Ürün Arayın:")

    if st.button("Ara"):
        # Create two columns for the progress indicators
        col1, col2 = st.columns(2)

        # First progress indicator
        with col1:
            with st.spinner("Mağazalar aranıyor..."):
                search_results = get_search_results(initial_query, search_location, search_gl, search_hl, serper_api_key)
                extracted_domains = list(search_results.keys())
                if isinstance(merchant_list, str):
                    merchant_domains = [domain.strip() for domain in merchant_list.split(',') if domain.strip()]
                else:
                    merchant_domains = merchant_list
                final_url_list = compare_domains(extracted_domains, merchant_domains)

            st.success("✅ Mağazalar bulundu")

        # Second progress indicator
        with col2:
            with st.spinner("Ürünler inceleniyor..."):
                merged_data = {domain: search_results[domain] for domain in final_url_list}
                limited_data = sort_and_limit_urls(merged_data, limit=5)

            st.success("✅ En uygun seçenekler bulundu")

        # Create expandable sections for both lists
        with st.expander("Bulunan iyzico mağazaları"):
            for domain in final_url_list:
                st.write(f"- {domain}")

        st.subheader("Sonuçlar:")
        # Create a placeholder for the streaming content
        results_placeholder = st.empty()
        
        # Stream the results
        with results_placeholder:
            st.write_stream(shopping_assistant(system_prompt_final_answer, initial_query, limited_data))

if __name__ == "__main__":
    main()